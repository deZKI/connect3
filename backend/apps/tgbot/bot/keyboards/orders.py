from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from apps.tgbot.bot.consts import TEXT_AGREE, TEXT_DISAGREE


def confirm_purchase_keyboard():
    buttons = [
        [KeyboardButton(text=TEXT_AGREE), KeyboardButton(text=TEXT_DISAGREE)]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
