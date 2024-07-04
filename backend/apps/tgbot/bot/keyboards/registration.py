from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from apps.tgbot.bot.consts import TEXT_SHARE_CONTACT

share_phone_number_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=TEXT_SHARE_CONTACT, request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Предположим, у нас есть список вариантов, откуда пользователь узнал о мероприятии
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
