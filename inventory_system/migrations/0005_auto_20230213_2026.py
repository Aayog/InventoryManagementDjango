# Generated by Django 3.2 on 2023-02-14 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory_system', '0004_product_stock_threshold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AddField(
            model_name='customer',
            name='password',
            field=models.CharField(default='4315', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
