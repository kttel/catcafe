import os

from django.core.files.storage import get_storage_class
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse_lazy, reverse


class OverwriteStorage(get_storage_class()):
    def _save(self, name, content):
        self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name


def content_file_name(instance, filename):
    ext = 'jpg'
    filename = "%s.%s" % (instance.user.id, ext)
    return os.path.join('avatars', filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ship_address = models.CharField('Default ship address', max_length=350, blank=True)
    image = models.ImageField(upload_to=content_file_name, storage=OverwriteStorage(),
                              default='avatars/default.png', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'


class Category(models.Model):
    slug = models.SlugField('Category slug', unique=True)
    title = models.CharField('Category name', max_length=150)
    description = models.TextField('Category description', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cafe:category', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'dish_category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class Dish(models.Model):
    name = models.CharField('Dish name', max_length=150)
    description = models.TextField('Description', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField('Price per one unit', max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='dishes/', default='dishes/default.png', blank=True)
    availability = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cafe:dish', kwargs={'dish_pk': self.pk})

    class Meta:
        verbose_name = 'dish'
        verbose_name_plural = 'dishes'


class Comment(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, help_text='Enter title for your comment')
    content = models.TextField(help_text='Enter your comment')
    mark = models.SmallIntegerField(help_text='Rate this dish from 1 to 5',
                                    validators=[MinValueValidator(1), MaxValueValidator(5)])
    data_created = models.DateTimeField(help_text="Time commented", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'dish comments'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'


class Promocode(models.Model):
    text = models.CharField('Promocode value', max_length=15)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    discount_percentage = models.SmallIntegerField(blank=True, default=0)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.text


class Order(models.Model):
    ORDER_STATUS = [
        ('FRM', 'Forming'),
        ('PRC', 'Processed'),
        ('CNC', 'Canceled'),
        ('PRP', 'Preparing'),
        ('DLV', 'Delivering'),
        ('FNS', 'Finished')
    ]

    user = models.ForeignKey(User, on_delete=models.SET("deleted"))
    promocode = models.ForeignKey(Promocode, on_delete=models.SET_NULL, null=True, blank=True,
                                  default='')
    datetime_created = models.DateTimeField('Creation time', auto_now_add=True)
    datetime_updated = models.DateTimeField('Updated', auto_now=True)
    ship_address = models.CharField(max_length=350, help_text="Enter your address for shipping",
                                    default='')
    ship_required = models.DateTimeField('Estimated shipping time', blank=True, null=True)
    status = models.CharField(max_length=3, choices=ORDER_STATUS, default='FRM')
    comment = models.TextField(help_text='Enter your comment if you want to add details to your order', blank=True,
                               default='')

    def __str__(self):
        return f'Order {self.datetime_created.strftime("%Y-%m-%d %H:%M:%S")}'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    dish = models.ForeignKey(Dish, on_delete=models.SET('deleted'))
    quantity = models.SmallIntegerField('Dish amount', default=1, help_text='Enter dish quantity')


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    date_added = models.DateTimeField("Date added", auto_now_add=True)

    class Meta:
        unique_together = ('user', 'dish',)

    def save(self, *args, **kwargs):
        if Wishlist.objects.filter(user=self.user, dish=self.dish).exists():
            return reverse_lazy('cafe:wishlist')
        else:
            super().save(self, *args, **kwargs)


class MailingList(models.Model):
    email = models.EmailField(help_text='Enter your email to get news about our cafe', unique=True)
    status = models.BooleanField(default=False)
