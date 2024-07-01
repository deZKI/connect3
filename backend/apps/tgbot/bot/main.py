from django.conf import settings
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from .messages import router

TOKEN = settings.TELEGRAM_BOT_API_TOKEN

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
dp.include_router(router)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запустить"),
    ]
    await bot.set_my_commands(commands)


async def start_bot():
    await set_commands(bot)
    await dp.start_polling(bot)
