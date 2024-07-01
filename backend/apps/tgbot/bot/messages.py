from aiogram import types, Router
from aiogram.filters import Command
from asgiref.sync import sync_to_async

from ..models import Siteconfig

router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    config = await sync_to_async(Siteconfig.objects.first)()
    text = config.welcome_text if config else "Welcome!"
    await message.answer(text)
