# Generated by Django 4.1.2 on 2022-10-15 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_alter_order_managers_alter_comment_mark_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailinglist',
            name='email',
            field=models.EmailField(help_text='Enter your email to get news about our cafe', max_length=254, unique=True),
        ),
    ]
