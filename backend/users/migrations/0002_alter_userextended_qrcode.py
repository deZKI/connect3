# Generated by Django 5.0.3 on 2024-03-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextended',
            name='qrcode',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/', verbose_name='Qrcode пользователя '),
        ),
    ]
