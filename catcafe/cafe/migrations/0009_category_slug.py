# Generated by Django 4.1.2 on 2022-10-18 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0008_alter_orderdetail_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]