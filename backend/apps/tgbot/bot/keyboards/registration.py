from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

share_phone_number_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Поделиться контактом", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
