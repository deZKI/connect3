import logging
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from django.core.management.base import BaseCommand
from django.conf import settings

from users.models import UserExtended

logging.basicConfig(level=logging.INFO)

API_TOKEN = settings.TELEGRAM_BOT_API_TOKEN

# Инициализация бота и диспетчера с использованием хранилища состояний в памяти
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

class RegistrationStates(StatesGroup):
    church = State()
    know_from = State()

@dp.message_handler(commands=['start', 'register'])
async def register_start(message: types.Message):
    user_id = message.from_user.id
    user, created = UserExtended.objects.get_or_create(username=user_id)
    if created:
        await message.reply("Добро пожаловать! Введите название вашей церкви:")
        await RegistrationStates.church.set()
    else:
        await message.reply(f"Вы уже зарегистрированы, {user.username}!")

@dp.message_handler(state=RegistrationStates.church)
async def process_church(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['church'] = message.text

    await message.reply("Откуда вы узнали о нас?")
    await RegistrationStates.next()

@dp.message_handler(state=RegistrationStates.know_from)
async def process_know_from(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['know_from'] = message.text

        # Сохранение данных в базу данных
        user = UserExtended.objects.get(username=user_id)
        user.church = data['church']
        user.know_from = data['know_from']
        user.save()

        # Генерация QR-кода
        user.generate_qrcode()
        user.save()

    await message.reply("Регистрация завершена! Спасибо!")

    await state.finish()  # Очистка состояния

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting bot...")
        executor.start_polling(dp, skip_updates=True)
