# Generated by Django 5.0.2 on 2024-03-06 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_app', '0006_remove_item_discount_remove_item_tax_order_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='tax',
        ),
        migrations.RemoveField(
            model_name='item',
            name='currency',
        ),
        migrations.DeleteModel(
            name='Discount',
        ),
        migrations.DeleteModel(
            name='Tax',
        ),
    ]
