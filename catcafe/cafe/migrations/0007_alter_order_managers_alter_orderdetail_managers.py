# Generated by Django 4.1.2 on 2022-10-16 20:58

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0006_alter_promocode_discount_percentage'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='order',
            managers=[
            ],
        ),
        migrations.AlterModelManagers(
            name='orderdetail',
            managers=[
                ('popular_dishes', django.db.models.manager.Manager()),
            ],
        ),
    ]
