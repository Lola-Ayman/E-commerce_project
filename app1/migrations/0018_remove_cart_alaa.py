# Generated by Django 4.2.2 on 2024-03-01 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0017_rename_cart_cartitem_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='alaa',
        ),
    ]
