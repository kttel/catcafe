from django.contrib.auth.mixins import AccessMixin
from django.db.models import Count
from django.shortcuts import redirect

from .models import Category


class CheckerLoginMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('cafe:index')
        return super(CheckerLoginMixin, self).dispatch(request, *args, **kwargs)


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['categories'] = Category.objects.all().annotate(count=Count('dish')).order_by('-count', 'title')
        return context
