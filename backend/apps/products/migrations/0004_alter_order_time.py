# Generated by Django 5.0.6 on 2024-07-04 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время'),
        ),
    ]
