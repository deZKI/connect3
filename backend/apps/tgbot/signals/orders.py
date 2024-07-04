import asyncio
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.products.models import Order
from apps.tgbot.models import Siteconfig
from apps.tgbot.bot.messages import send_notification_to_kitchen_admin


@receiver(post_save, sender=Order)
def notify_kitchen_admin(sender, instance, created, **kwargs):
    if created:
        site_config = Siteconfig.objects.first()
        if site_config:
            kitchen_admin = site_config.kitchen_admin
            main_admin = site_config.main_admin
            if kitchen_admin:
                async_to_sync(asyncio.create_task)(send_notification_to_kitchen_admin(kitchen_admin, instance))
            elif main_admin:
                async_to_sync(asyncio.create_task)(send_notification_to_kitchen_admin(main_admin, instance))
        else:
            print("Ошибка: Настройки сайта не найдены.")
