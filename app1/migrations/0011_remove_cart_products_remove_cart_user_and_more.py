# Generated by Django 4.2.2 on 2024-03-01 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_catrpro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='catrpro',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
