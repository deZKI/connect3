from django.utils import timezone

from apps.users.models import UserExtended

from .main import bot
from .keyboards import main_keyboard
from ...products.models import Order


async def send_is_payed_message(user: UserExtended):
    await bot.send_message(chat_id=user.tg_chat_id, text="Вы успешно оплатили участие в мероприятии!",
                           reply_markup=await main_keyboard(user=user))


async def send_notification_to_kitchen_admin(admin_user: UserExtended, order_instance: Order):
    # Преобразование времени заказа в локальное время
    local_time = order_instance.time.astimezone(timezone.get_current_timezone())
    formatted_time = local_time.strftime('%Y-%m-%d %H:%M:%S %Z')

    message_text = (
        f"Новый заказ!\n"
        f"Пользователь: {order_instance.user.username}\n"
        f"Имя: {order_instance.user.first_name}\n"
        f"Фамилия: {order_instance.user.last_name}\n"
        f"Товар: {order_instance.product.name}\n"
        f"Дата и время: {formatted_time}"
    )
    await bot.send_message(chat_id=admin_user.tg_chat_id, text=message_text)
