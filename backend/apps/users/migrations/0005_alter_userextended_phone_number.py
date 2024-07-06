# Generated by Django 5.0.6 on 2024-07-06 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_userextended_tg_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextended',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Telegram Phone Number'),
        ),
    ]