from aiogram import types, Router
from aiogram.filters import Command
from asgiref.sync import sync_to_async

from .utils.decorators import telegram_user_validation
from ..models import Siteconfig

router = Router()


@router.message(Command("start"))
@telegram_user_validation
async def send_welcome(message: types.Message):
    config = await sync_to_async(Siteconfig.objects.first)()
    text = config.welcome_text if config else "Welcome!"
    await message.answer(text)
