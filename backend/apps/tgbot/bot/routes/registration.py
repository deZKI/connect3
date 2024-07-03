from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from asgiref.sync import sync_to_async

from apps.users.models import UserExtended
from ..consts import TEXT_REGISTER
from ..forms import RegistrationForm
from ..keyboards import share_phone_number_keyboard, main_keyboard

registration_router = Router()


@registration_router.message(F.text == TEXT_REGISTER)
async def register(message: types.Message, state: FSMContext):
    await message.answer("Пожалуйста, укажите ваше имя:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationForm.waiting_for_first_name)


@registration_router.message(RegistrationForm.waiting_for_first_name)
async def process_first_name(message: types.Message, state: FSMContext):
    first_name = message.text
    await state.update_data(first_name=first_name)
    await message.answer("Пожалуйста, укажите вашу фамилию:")
    await state.set_state(RegistrationForm.waiting_for_last_name)


@registration_router.message(RegistrationForm.waiting_for_last_name)
async def process_last_name(message: types.Message, state: FSMContext):
    last_name = message.text
    await state.update_data(last_name=last_name)
    await message.answer("Пожалуйста, поделитесь вашим номером телефона:", reply_markup=share_phone_number_keyboard)
    await state.set_state(RegistrationForm.waiting_for_phone_number)


@registration_router.message(RegistrationForm.waiting_for_phone_number, F.contact)
async def process_phone_number(message: types.Message, state: FSMContext):
    if not message.contact:
        await message.answer("Пожалуйста, используйте кнопку для отправки вашего контакта.")
        return

    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await message.answer("Пожалуйста, укажите название вашей церкви:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationForm.waiting_for_church)


@registration_router.message(RegistrationForm.waiting_for_church)
async def process_church(message: types.Message, state: FSMContext):
    church = message.text
    await state.update_data(church=church)
    await message.answer("Откуда вы узнали о нашем мероприятии?")
    await state.set_state(RegistrationForm.waiting_for_know_from)


@registration_router.message(RegistrationForm.waiting_for_know_from)
async def process_know_from(message: types.Message, state: FSMContext):
    know_from = message.text
    user_data = await state.get_data()

    user = await sync_to_async(UserExtended.objects.get)(tg_chat_id=message.from_user.id)
    user.first_name = user_data['first_name']
    user.last_name = user_data['last_name']
    user.phone_number = user_data['phone_number']
    user.church = user_data['church']
    user.know_from = know_from
    user.is_registered = True
    await sync_to_async(user.save)()

    await message.answer("Вы успешно зарегистрированы на мероприятие!", reply_markup=main_keyboard)

    await state.clear()
