from aiogram import types, Router, F
from aiogram.filters import Command
from asgiref.sync import sync_to_async

from ..consts import TEXT_PRODUCT_ORDER, TEXT_WHAT_IS_CONNECT
from ..keyboards import products_keyboard_reply, main_keyboard
from ...models import Siteconfig

menu_router = Router()


@menu_router.message(Command("start"))
async def send_welcome(message: types.Message):
    config = await sync_to_async(Siteconfig.objects.first)()
    text = config.welcome_text if config else "Welcome!"
    await message.answer(text, reply_markup=await main_keyboard(message))


@menu_router.message(F.text == TEXT_PRODUCT_ORDER)
async def send_product_menu(message: types.Message):
    await message.answer('Ты можешь заказать?', reply_markup=await products_keyboard_reply())


@menu_router.message(F.text == TEXT_WHAT_IS_CONNECT)
async def send_what_is_connect(message: types.Message):
    config = await sync_to_async(Siteconfig.objects.first)()
    await message.answer(config.what_is_connect, reply_markup=await main_keyboard(message))
