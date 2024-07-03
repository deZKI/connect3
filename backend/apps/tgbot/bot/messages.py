from apps.users.models import UserExtended

from .main import bot
from .keyboards import main_keyboard


async def send_is_payed_message(user: UserExtended):
    await bot.send_message(chat_id=user.tg_chat_id, text="Вы успешно оплатили участие в мероприятии!",
                           reply_markup=await main_keyboard(user=user))
