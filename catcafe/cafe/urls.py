from django.urls import path

from .views import MainView, RegisterView, AuthView, CategoryView, DishView, WishlistView, WishlistDeleteView, \
    WishlistAdd, ProfileView, DeleteCommentView, OrdersView, OrderDishView, OrderDetailDelete, OrderCancelView, \
    OrderCurrentView, OrdersManagementPanel, OrderCancelByWorkerView, OrderApplyByWorkerView
from django.contrib.auth.views import LogoutView

app_name = 'cafe'
urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('login/', AuthView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dish/<int:dish_pk>', DishView.as_view(), name='dish'),
    path('category/<slug:slug>', CategoryView.as_view(), name='category'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('wishlist/delete/<int:dish_pk>', WishlistDeleteView.as_view(), name='delete_from_wishlist'),
    path('wishlist/add/<int:dish_pk>', WishlistAdd.as_view(), name="add_to_wishlist"),
    path('profile', ProfileView.as_view(), name='profile'),
    path('delete/comment/<int:dish_pk>/<int:comment_pk>', DeleteCommentView.as_view(), name='delete_comment'),
    path('orders', OrdersView.as_view(), name='orders'),
    path('orders/cancel/<int:order_pk>', OrderCancelView.as_view(), name='cancel_order'),
    path('order', OrderCurrentView.as_view(), name='order_all'),
    path('order/<int:dish_pk>', OrderDishView.as_view(), name='order'),
    path('order/delete/<int:detail_pk>', OrderDetailDelete.as_view(), name='delete_from_order'),
    path('management/', OrdersManagementPanel.as_view(), name='management'),
    path('management/cancel/<int:order_pk>', OrderCancelByWorkerView.as_view(), name='cancel_by_worker'),
    path('management/apply/<int:order_pk>', OrderApplyByWorkerView.as_view(), name='apply_by_worker')
]