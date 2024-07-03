from aiogram.types import Message

from apps.users.models import UserExtended

class UserService:

    def __init__(self, message: Message):
        user = message.from_user.id