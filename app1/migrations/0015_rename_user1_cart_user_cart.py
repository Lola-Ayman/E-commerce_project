# Generated by Django 4.2.2 on 2024-03-01 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_rename_user_cart_user1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user1',
            new_name='user_cart',
        ),
    ]
