from datetime import datetime

from aiogram import types, Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove, LabeledPrice
from django.conf import settings

from apps.users.models import UserExtended

from ..consts import TEXT_REGISTER
from ..forms import RegistrationForm
from ..keyboards import (
    share_phone_number_keyboard,
    know_from_keyboard,
    gender_keyboard,
    retry_payment_keyboard
)
from ..decorators import user_is_not_registered

registration_router = Router()


@registration_router.message(F.text == TEXT_REGISTER)
@user_is_not_registered
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


@registration_router.message(RegistrationForm.waiting_for_phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    if not message.contact or not message.contact.phone_number:
        await message.answer(
            "Пожалуйста, используйте кнопку для отправки вашего контакта и убедитесь, что номер телефона доступен."
        )
        return

    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await message.answer("Пожалуйста, укажите название вашей церкви:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationForm.waiting_for_church)


@registration_router.message(RegistrationForm.waiting_for_church)
async def process_church(message: types.Message, state: FSMContext):
    church = message.text
    await state.update_data(church=church)
    await message.answer("Откуда вы узнали о нашем мероприятии?", reply_markup=know_from_keyboard)
    await state.set_state(RegistrationForm.waiting_for_know_from)


@registration_router.message(RegistrationForm.waiting_for_know_from)
async def process_know_from(message: types.Message, state: FSMContext):
    know_from = message.text
    await state.update_data(know_from=know_from)
    await message.answer("Пожалуйста, укажите вашу дату рождения (дд.мм.гггг):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationForm.waiting_for_birth_date)


@registration_router.message(RegistrationForm.waiting_for_birth_date)
async def process_birth_date(message: types.Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, '%d.%m.%Y').date()
        await state.update_data(birth_date=birth_date)
    except ValueError:
        await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате дд.мм.гггг:")
        return

    await message.answer("Пожалуйста, укажите ваш пол:", reply_markup=gender_keyboard)
    await state.set_state(RegistrationForm.waiting_for_gender)


@registration_router.message(RegistrationForm.waiting_for_gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()
    if gender not in ['мужской', 'женский']:
        await message.answer("Пожалуйста, выберите пол из предложенных вариантов.")
        return

    await state.update_data(gender=gender)
    await message.answer("Пожалуйста, укажите ваш город:")
    await state.set_state(RegistrationForm.waiting_for_city)


@registration_router.message(RegistrationForm.waiting_for_city)
async def process_city(message: types.Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)
    await message.answer("Расскажите немного о себе:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationForm.waiting_for_about_me)


@registration_router.message(RegistrationForm.waiting_for_about_me)
async def process_about_me(message: types.Message, state: FSMContext):
    about_me = message.text
    user_data = await state.get_data()

    user = await UserExtended.objects.aget(tg_chat_id=message.from_user.id)
    user.first_name = user_data['first_name']
    user.last_name = user_data['last_name']
    user.phone_number = user_data['phone_number']
    user.church = user_data['church']
    user.know_from = user_data['know_from']
    user.birth_date = user_data['birth_date']
    user.gender = user_data['gender']
    user.city = user_data['city']
    user.about_me = about_me
    user.is_registered = True
    await user.asave()

    await message.answer("Вы успешно зарегистрированы на мероприятие!")

    # Генерация инвойса
    prices = [
        LabeledPrice(label="Участие в мероприятии", amount=1500 * 100)  # 1500 RUB
    ]

    try:
        await message.bot.send_invoice(
            chat_id=message.chat.id,
            title="Оплата за участие в мероприятии",
            description="Пожалуйста, оплатите участие в мероприятии, чтобы завершить регистрацию.",
            payload="registration_payment",
            provider_token=settings.INVOICE_BOT_API_TOKEN,
            currency="RUB",
            prices=prices,
            start_parameter="registration-payment",
        )
    except Exception as e:
        await message.answer(
            f"Произошла ошибка при создании счета: {str(e)}. Пожалуйста, попробуйте снова или свяжитесь с поддержкой.",
            reply_markup=retry_payment_keyboard()
        )
    finally:
        await state.clear()


@registration_router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await pre_checkout_q.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@registration_router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    user = await UserExtended.objects.aget(tg_chat_id=message.from_user.id)
    user.is_payed = True
    await user.asave(update_fields=['is_payed'])