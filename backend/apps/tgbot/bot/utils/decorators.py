from typing import Callable, Any
from asgiref.sync import sync_to_async

from aiogram import types

from apps.tgbot.bot.consts import TEXT_BANNED
from apps.users.models import UserExtended


async def send_ban_message(event: types.Message | types.CallbackQuery) -> None:
    from apps.tgbot.bot.main import bot
    if isinstance(event, types.CallbackQuery):
        await bot.edit_message_text(chat_id=event.message.chat.id, message_id=event.message.message_id,
                                    text=TEXT_BANNED)
    else:
        await bot.send_message(event.chat.id, TEXT_BANNED)


def telegram_user_validation(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
    async def wrapper(event: types.Message) -> None:
        tg_user = event.from_user
        user, created = await sync_to_async(UserExtended.objects.get_or_create)(
            username=tg_user.username,
            tg_chat_id=tg_user.id,
            defaults={
                'first_name': tg_user.first_name if tg_user.first_name else 'Неизвестно',
                'last_name': tg_user.last_name if tg_user.last_name else 'Неизвестно',
            }
        )
        if user.is_banned:
            await send_ban_message(event)
        else:
            await handler(event)

    return wrapper
