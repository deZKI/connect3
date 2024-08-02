from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.users.models import UserExtended
from apps.tgbot.bot.messages import send_is_payed_message


@receiver(pre_save, sender=UserExtended)
async def send_payment_confirmation(sender, instance, **kwargs):
    if not instance.pk:  # Новый пользователь
        return
    new_user = await UserExtended.objects.aget(pk=instance.pk)
    if instance.is_payed and not new_user.is_payed:
        try:
            await send_is_payed_message(user=instance)
        except Exception as e:
            print(f"Ошибка: Пользователь {instance.username} {e}.")
