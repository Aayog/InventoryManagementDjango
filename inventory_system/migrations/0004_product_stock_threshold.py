# Generated by Django 4.1.5 on 2023-02-08 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_system', '0003_alter_address_options_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock_threshold',
            field=models.PositiveIntegerField(default=3),
        ),
    ]
