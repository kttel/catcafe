# Generated by Django 4.1.2 on 2022-10-16 20:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0003_alter_mailinglist_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='category_id',
            new_name='category',
        ),
    ]
