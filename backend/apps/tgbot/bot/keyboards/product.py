from asgiref.sync import sync_to_async

from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

from apps.products.models import Product
from ..consts import TEXT_BACK


async def products_keyboard_reply():
    keyboard = ReplyKeyboardBuilder()

    products = await sync_to_async(list)(Product.objects.filter(available=True))

    for product in products:
        keyboard.add(KeyboardButton(text=f"{product.name} - {product.price}"))

    keyboard.add(KeyboardButton(text=TEXT_BACK))

    return keyboard.adjust(2).as_markup(resize_keyboard=True)
