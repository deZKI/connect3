from asgiref.sync import sync_to_async
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.db.models import Q

from apps.products.models import Product
from apps.tgbot.bot.consts import TEXT_PRODUCT_ORDER, TEXT_WHAT_IS_CONNECT, TEXT_REGISTER, TEXT_MENU
from apps.users.models import UserExtended


async def main_keyboard(message: Message = None, user: UserExtended = None) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.add(
        KeyboardButton(text=TEXT_WHAT_IS_CONNECT)
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

    return keyboard.adjust(1).as_markup(input_field_placeholder=TEXT_MENU, resize_keyboard=True)


async def products_keyboard_reply():
    keyboard = ReplyKeyboardBuilder()

    products = await sync_to_async(list)(Product.objects.filter(available=True))

    for product in products:
        keyboard.add(KeyboardButton(text=f"{product.name} - {product.price}"))

    return keyboard.adjust(2).as_markup(resize_keyboard=True)