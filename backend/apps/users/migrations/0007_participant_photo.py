# Generated by Django 5.0.6 on 2024-07-28 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='participant/', verbose_name='Фото участника'),
        ),
    ]