# Generated by Django 4.1.5 on 2023-02-06 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stock', models.PositiveIntegerField()),
                ('is_empty', models.BooleanField(default=False)),
            ],
        ),
    ]
