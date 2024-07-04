from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def confirm_purchase_keyboard():
    buttons = [
        [KeyboardButton(text="Подтвердить покупку"), KeyboardButton(text="Отменить")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
