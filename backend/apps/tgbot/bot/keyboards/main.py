from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.db.models import Q

from apps.tgbot.bot.consts import *
from apps.users.models import UserExtended


async def main_keyboard(message: Message = None, user: UserExtended = None) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=TEXT_WHAT_IS_CONNECT)
    )
    keyboard.add(
        KeyboardButton(text=TEXT_POST)
    )
    user = await UserExtended.objects.filter(
        Q(tg_chat_id=message.from_user.id) | Q(username=message.from_user.id)).afirst() if user is None else user

    # Если пользователь не зареган
    if not user.is_registered:
        keyboard.add(KeyboardButton(text=TEXT_REGISTER))

    # Если пользователь оплатил => он может заказывать
    if user.is_payed:
        keyboard.add(
            KeyboardButton(text=TEXT_PRODUCT_ORDER)
        )
        keyboard.add(
            KeyboardButton(text=TEXT_MY_ORDERS)
        )

    return keyboard.adjust(1).as_markup(input_field_placeholder=TEXT_MENU, resize_keyboard=True)