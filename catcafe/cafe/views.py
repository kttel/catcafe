from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import F, Sum, Count
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import AuthForm, RegisterForm, ProfileForm, CommentForm
from .utils import CheckerLoginMixin, DataMixin
from .models import Dish, Wishlist, Profile, OrderDetail, Comment, Order
from .usecases import check_search_field


class MainView(DataMixin, ListView):
    paginate_by = 3
    model = Dish
    template_name = 'cafe/main_page.html'
    context_object_name = 'dishes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        new_data = self.get_user_context(title='Cat Cafe | Main page')
        return dict(list(context.items()) + list(new_data.items()))


class CategoryView(DataMixin, ListView):
    paginate_by = 3
    model = Dish
    template_name = 'cafe/category_page.html'
    context_object_name = 'dishes'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = context["dishes"][0].category
        new_data = self.get_user_context(title=f'Cat Cafe | {category}', category=f'{category}')
        return dict(list(context.items()) + list(new_data.items()))

    def get_queryset(self):
        return Dish.objects.filter(category__slug=self.kwargs['slug']).select_related('category')


class DishView(DataMixin, DetailView):
    model = Dish
    template_name = 'cafe/dish_page.html'
    pk_url_kwarg = 'dish_pk'
    success_url = 'cafe:wishlist'
    context_object_name = 'dish'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        new_data = self.get_user_context(title=f'Cat Cafe | {context["dish"].name}',
                                         comment=f'{context["dish"].comment_set}')
        return dict(list(context.items()) + list(new_data.items()))


class AuthView(CheckerLoginMixin, LoginView):
    form_class = AuthForm
    template_name = 'cafe/login.html'

    def dispatch(self, *args, **kwargs):
        return super(AuthView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**dict(list(context.items())), **{'title': 'Cat Cafe | Login'}}

    def get_success_url(self):
        return reverse_lazy('cafe:index')


class RegisterView(CheckerLoginMixin, CreateView):
    form_class = RegisterForm
    template_name = 'cafe/register.html'

    def dispatch(self, *args, **kwargs):
        return super(RegisterView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**dict(list(context.items())), **{'title': 'Cat Cafe | Register'}}

    def get_success_url(self):
        return reverse_lazy('cafe:login')


class WishlistView(LoginRequiredMixin, DataMixin, ListView):
    model = Wishlist
    template_name = 'cafe/wishlist.html'
    context_object_name = 'wishlist'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        new_data = self.get_user_context(title=f'Cat Cafe | Wishlist')
        return dict(list(context.items()) + list(new_data.items()))

    def get_queryset(self):
        objects = Wishlist.objects.filter(user=self.request.user.pk).order_by('-date_added')
        if check_search_field(self.request):
            return objects.filter(dish__name__icontains=self.request.GET.get("search-dish"))
        return objects


class WishlistDeleteView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Wishlist
    pk_url_kwarg = 'dish_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        new_data = self.get_user_context(title=f'Cat Cafe | Deleting...')
        return dict(list(context.items()) + list(new_data.items()))

    def get_object(self, queryset=None):
        return get_object_or_404(Wishlist, dish__pk=self.kwargs.get('dish_pk'))

    def get_success_url(self):
        return reverse_lazy('cafe:wishlist')


class WishlistAdd(LoginRequiredMixin, DataMixin, CreateView):
    model = Wishlist
    fields = ('user', 'dish')
    pk_url_kwarg = 'dish_pk'

    def get_success_url(self):
        return reverse_lazy('cafe:wishlist')

    def form_invalid(self, form):
        return redirect('cafe:wishlist')


class ProfileView(LoginRequiredMixin, DataMixin, TemplateView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'cafe/user_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_form = ProfileForm(initial={'ship_address': self.request.user.profile.ship_address,
                                         'image': self.request.user.profile.image})
        comment_form = CommentForm(
            initial={'dish': OrderDetail.objects.values_list('dish').filter(order__user=self.request.user,
                                                                            order__status='FNS')})
        new_data = self.get_user_context(title=f'Cat Cafe | {self.request.user.username}',
                                         total=self.request.user.order_set.count(),
                                         completed=self.request.user.order_set.filter(status='FNS').count(),
                                         processing=self.request.user.order_set.filter(
                                             status__in=['PRC', 'PRP', 'DLV']).count(),
                                         dishes=OrderDetail.objects.values_list('dish').filter(
                                             order__user=self.request.user,
                                             order__status='FNS'),
                                         user_form=user_form, comment_form=comment_form)
        return dict(list(context.items()) + list(new_data.items()))

    def post(self, request, *args, **kwargs):
        if request.POST.get('form_type') == 'user_form':
            form = ProfileForm(request.POST, request.FILES,
                               instance=Profile.objects.get(user=request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()
            return redirect('cafe:profile')
        elif request.POST.get('form_type') == 'comment_form':
            comment = Comment(user=request.user, dish=Dish.objects.get(pk=request.POST.get('dish')),
                              mark=request.POST.get('mark'), title=request.POST.get('title'),
                              content=request.POST.get('content'))
            comment.save()
            return redirect('cafe:dish', dish_pk=request.POST.get('dish'))
        return redirect('cafe:index')


class DeleteCommentView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Comment

    def post(self, request, *args, **kwargs):
        comment = Comment.objects.get(pk=self.kwargs.get('comment_pk'))
        author = User.objects.get(pk=comment.user.pk)

        if author == self.request.user:
            return super().post(self, request, *args, **kwargs)
        else:
            return redirect('cafe:dish', dish_pk=self.kwargs['dish_pk'])

    def get_object(self, queryset=None):
        return get_object_or_404(Comment, pk=self.kwargs.get('comment_pk'))

    def get_success_url(self):
        return reverse_lazy('cafe:dish', kwargs={'dish_pk': self.kwargs['dish_pk']})


class OrdersView(LoginRequiredMixin, DataMixin, ListView):
    model = Order
    template_name = 'cafe/orders.html'
    context_object_name = 'details'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        subquery = OrderDetail.objects.filter(order__user=self.request.user, order__status__in=['PRC', 'PRP'])
        new_data = self.get_user_context(title=f'Cat Cafe | Orders',
                                         amount=OrderDetail.objects.filter(order__user=self.request.user,
                                                                          order__status='FRM').
                                         aggregate(Count('pk'))['pk__count'],
                                         total_price=OrderDetail.objects.filter(order__user=self.request.user,
                                                                          order__status='FRM').
                                         aggregate(summ=Sum(
                                                    F('quantity') *
                                                    F('dish__price')))['summ'],
                                         last_order=Order.objects.filter(user=self.request.user,
                                                                         status__in=['PRC', 'PRP']).
                                         order_by('datetime_updated').first(),
                                         address=Profile.objects.values('ship_address').get(user=self.request.user)['ship_address'])
        return dict(list(context.items()) + list(new_data.items()))

    def get_queryset(self):
        Order.objects.get_or_create(user=self.request.user, status='FRM')
        details = OrderDetail.objects.filter(order__user=self.request.user, order__status='FRM').annotate(
            total_price=Sum(
                F('quantity') *
                F('dish__price'))).order_by('-pk')

        return details


class OrderDishView(LoginRequiredMixin, DataMixin, CreateView):
    model = OrderDetail
    pk_url_kwarg = 'dish_pk'
    fields = ('dish', 'quantity')

    def post(self, request, *args, **kwargs):
        Order.objects.get_or_create(user=self.request.user, status='FRM')
        order = Order.objects.get(user=self.request.user, status='FRM')
        dish = Dish.objects.get(pk=request.POST.get('dish'))
        if not OrderDetail.objects.filter(order=order, dish=dish).exists():
            order_detail = OrderDetail.objects.create(order=order, dish=dish, quantity=request.POST.get('quantity'))
        else:
            order_detail = OrderDetail.objects.get(order=order, dish=dish)
            order_detail.quantity += int(request.POST.get('quantity'))
        order_detail.save()
        return redirect('cafe:orders')

    def get_success_url(self):
        return reverse_lazy('cafe:orders')


class OrderDetailDelete(LoginRequiredMixin, DataMixin, DeleteView):
    model = OrderDetail
    pk_url_kwarg = 'detail_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        new_data = self.get_user_context(title=f'Cat Cafe | Deleting...')
        return dict(list(context.items()) + list(new_data.items()))

    def get_object(self, queryset=None):
        return get_object_or_404(OrderDetail, pk=self.kwargs.get('detail_pk'))

    def get_success_url(self):
        return reverse_lazy('cafe:orders')


class OrderCancelView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Order
    pk_url_kwarg = 'order_pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        new_data = self.get_user_context(title=f'Cat Cafe | Deleting...')
        return dict(list(context.items()) + list(new_data.items()))

    def get_object(self, queryset=None):
        return get_object_or_404(Order, pk=self.kwargs.get('order_pk'))

    def get_success_url(self):
        return reverse_lazy('cafe:orders')


class OrderCurrentView(LoginRequiredMixin, DataMixin, UpdateView):
    model = Order

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, status='FRM')
        order.status = 'PRC'
        order.ship_address = self.request.POST.get('address')
        order.save()

        return redirect('cafe:orders')


class OrdersManagementPanel(LoginRequiredMixin, DataMixin, TemplateView):
    template_name = 'cafe/management-panel.html'

    def get_context_data(self, **kwargs):
        orders = {'Processing orders': Order.objects.filter(status='PRC').order_by('-datetime_updated').all(),
                  'Preparing orders': Order.objects.filter(status='PRP').order_by('-datetime_updated').all(),
                  'Delivering': Order.objects.filter(status='DLV').order_by('-datetime_updated').all()}

        context = super().get_context_data(**kwargs)
        new_data = self.get_user_context(title='Cat Cafe | Management panel',
                                         orders=orders)
        return dict(list(context.items()) + list(new_data.items()))

    def get(self, request, *args, **kwargs):
        if Group.objects.get(name='worker') in request.user.groups.all():
            return super().get(request, *args, **kwargs)
        else:
            return redirect('cafe:index')


class OrderCancelByWorkerView(LoginRequiredMixin, DataMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        if Group.objects.get(name='worker') in request.user.groups.all():
            return super().get(request, *args, **kwargs)
        else:
            return redirect('cafe:index')

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs.get('order_pk'))
        order.status = 'CNC'
        order.save()

        return redirect('cafe:management')


class OrderApplyByWorkerView(LoginView, DataMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        if Group.objects.get(name='worker') in request.user.groups.all():
            return super().get(request, *args, **kwargs)
        else:
            return redirect('cafe:index')

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=self.kwargs.get('order_pk'))
        if order.status == 'PRC':
            order.status = 'PRP'
        elif order.status == 'PRP':
            order.status = 'DLV'
        else:
            order.status = 'FNS'
        order.save()

        return redirect('cafe:management')