from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from apps.tgbot.bot.consts import TEXT_SHARE_CONTACT

share_phone_number_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=TEXT_SHARE_CONTACT, request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

know_from_options = [
    "От друзей",
    "Из интернета",
    "Социальные сети",
    "Реклама",
    "Другое"
]

know_from_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=_)] for _ in know_from_options
    ],
    resize_keyboard=True, one_time_keyboard=True
)

genders = [
    "Мужской",
    "Женский"
]

gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=_)] for _ in genders
    ],
    resize_keyboard=True, one_time_keyboard=True
)


def retry_payment_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    retry_button = InlineKeyboardButton(text="Попробовать снова", callback_data="retry_payment")
    support_button = InlineKeyboardButton(text="Связаться с поддержкой", callback_data="contact_support")
    keyboard.add(retry_button, support_button)
    return keyboard
