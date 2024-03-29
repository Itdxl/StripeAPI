# Generated by Django 5.0.2 on 2024-03-06 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_app', '0004_discount_tax_alter_order_options_item_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.ManyToManyField(blank=True, to='stripe_app.discount'),
        ),
        migrations.AlterField(
            model_name='item',
            name='tax',
            field=models.ManyToManyField(blank=True, to='stripe_app.tax'),
        ),
    ]
