# Generated by Django 4.1.2 on 2022-10-15 18:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Category name')),
                ('description', models.TextField(blank=True, verbose_name='Category description')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
                'db_table': 'dish_category',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Dish name')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Price per one unit')),
                ('image', models.ImageField(blank=True, default='dishes/default.png', upload_to='dishes/')),
                ('availability', models.BooleanField(default=False)),
                ('category_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe.category')),
            ],
            options={
                'verbose_name': 'dish',
                'verbose_name_plural': 'dishes',
            },
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Enter your email to get news about our cafe', max_length=254)),
                ('status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation time')),
                ('datetime_updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('ship_address', models.CharField(help_text='Enter your address for shipping', max_length=350)),
                ('ship_required', models.DateTimeField(blank=True, verbose_name='Estimated shipping time')),
                ('status', models.CharField(choices=[('FRM', 'Forming'), ('PRC', 'Processed'), ('CNC', 'Canceled'), ('PRP', 'Preparing'), ('DLV', 'Delivering'), ('FNS', 'Finished')], default='FRM', max_length=3)),
                ('comment', models.TextField(blank=True, help_text='Enter your comment if you want to add details to your order')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.dish')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=15, verbose_name='Promocode value')),
                ('discount_percentage', models.SmallIntegerField(blank=True, max_length=3)),
                ('status', models.BooleanField(default=True)),
                ('dish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe.dish')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ship_address', models.CharField(blank=True, max_length=350, verbose_name='Default ship address')),
                ('image', models.ImageField(blank=True, default='avatars/default.png', upload_to='avatars/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.SmallIntegerField(default=1, help_text='Enter dish quantity', verbose_name='Dish amount')),
                ('dish', models.ForeignKey(on_delete=models.SET('deleted'), to='cafe.dish')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='promocode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cafe.promocode'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=models.SET('deleted'), to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Enter title for your comment', max_length=150)),
                ('content', models.TextField(help_text='Enter your comment')),
                ('mark', models.SmallIntegerField(help_text='Rate this dish from 1 to 5', max_length=1)),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafe.dish')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'db_table': 'dish comments',
            },
        ),
    ]