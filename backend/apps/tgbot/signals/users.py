import asyncio
from django.db.models.signals import pre_save
from django.dispatch import receiver

from aiogram import exceptions as tg_exceptions

from apps.users.models import UserExtended
from apps.tgbot.bot.messages import send_is_payed_message


@receiver(pre_save, sender=UserExtended)
def send_payment_confirmation(sender, instance, **kwargs):
    if instance.is_payed and not UserExtended.objects.get(pk=instance.pk).is_payed:
        try:
            asyncio.run(send_is_payed_message(user=instance))
        except tg_exceptions.BotBlocked:
            print(f"Ошибка: Пользователь {instance.username} заблокировал бота.")
        except tg_exceptions.ChatNotFound:
            print(f"Ошибка: Чат с пользователем {instance.username} не найден.")
        except tg_exceptions.RetryAfter as e:
            print(f"Ошибка: Доступ к боту временно заблокирован на {e.timeout} секунд.")
        except tg_exceptions.TelegramAPIError:
            print(f"Ошибка: Ошибка Telegram API при отправке сообщения пользователю {instance.username}.")
