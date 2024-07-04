from aiogram import types, Router, F
from aiogram.filters import Command
from asgiref.sync import sync_to_async

from ..consts import TEXT_WHAT_IS_CONNECT, TEXT_MENU
from ..keyboards import main_keyboard
from ...models import Siteconfig

menu_router = Router()


@menu_router.message(Command("start"))
async def send_welcome(message: types.Message):
    config = await sync_to_async(Siteconfig.objects.first)()
    text = config.welcome_text if config else "Welcome!"
    await message.answer(text, reply_markup=await main_keyboard(message=message))


@menu_router.message(Command("menu"))
async def send_welcome(message: types.Message):
    await message.answer(TEXT_MENU, reply_markup=await main_keyboard(message=message))


@menu_router.message(F.text == TEXT_WHAT_IS_CONNECT)
async def send_what_is_connect(message: types.Message):
    config = await sync_to_async(Siteconfig.objects.first)()
    await message.answer(config.what_is_connect, reply_markup=await main_keyboard(message=message))
