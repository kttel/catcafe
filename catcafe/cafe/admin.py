from django.contrib import admin
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'ship_address')
    fields = ('user', 'ship_address', 'image')


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'availability')
    list_editable = ('availability',)
    fieldsets = (
        (None, {
            'fields': ('name', 'category', 'availability')
        }),
        ('Information', {
            'fields': ('price', 'description', 'image')
        })
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title')
    fields = ('title', 'slug', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('dish', 'user', 'title', 'mark')
    fieldsets = (
        (None, {
            'fields': ('dish', 'user')
        }),
        ('Information', {
            'fields': ('mark', 'title', 'content')
        })
    )


@admin.register(Promocode)
class PromocodeAdmin(admin.ModelAdmin):
    list_display = ('text', 'status')
    list_editable = ('status',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime_created', 'datetime_updated', 'status')
    list_editable = ('status',)
    readonly_fields = ('datetime_created', 'datetime_updated')
    fieldsets = (
        (None, {
            'fields': ('user', ('datetime_created', 'datetime_updated'))
        }),
        ('Information', {
            'fields': ('status', 'promocode', 'comment')
        }),
        ('Shipping', {
            'fields': ('ship_address', 'ship_required')
        })
    )


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'dish', 'quantity')


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish', 'date_added')


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('email', 'status')
    list_editable = ('status', )