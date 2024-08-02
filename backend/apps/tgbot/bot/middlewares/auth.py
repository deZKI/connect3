from typing import Callable, Any, Awaitable

from django.db.models import Q
from django.db.utils import IntegrityError

from aiogram.dispatcher.event.bases import CancelHandler

from aiogram import types
from aiogram import BaseMiddleware

from apps.tgbot.bot.consts import TEXT_BANNED
from apps.users.models import UserExtended


class AuthMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[types.TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: types.TelegramObject | types.Message,
                       data: dict[str, Any]) -> Any:
        tg_user = event.from_user if event.message_id else event.callback_query.from_user
        try:
            user, created = await UserExtended.objects.aget_or_create(
                username=tg_user.username if tg_user.username else None,
                tg_chat_id=tg_user.id,
                defaults={
                    'first_name': tg_user.first_name if tg_user.first_name else 'Неизвестно',
                    'last_name': tg_user.last_name if tg_user.last_name else 'Неизвестно',
                }
            )

            if not created:
                # Обновляем поля, если пользователь уже существует
                user.first_name = tg_user.first_name if tg_user.first_name else 'Неизвестно'
                user.last_name = tg_user.last_name if tg_user.last_name else 'Неизвестно'
                await user.asave()
        except IntegrityError:
            user = await UserExtended.objects.filter(Q(tg_chat_id=tg_user.id) | Q(username=tg_user.username)).afirst()
            user.tg_chat_id = tg_user.id
            user.username = tg_user.username
            user.first_name = tg_user.first_name if tg_user.first_name else 'Неизвестно'
            user.last_name = tg_user.last_name if tg_user.last_name else 'Неизвестно'
            await user.asave(update_fields=['tg_chat_id', 'username', 'first_name', 'last_name'])

        data['user'] = user  # Сохраняем пользователя в data

        if not user.is_banned:
            return await handler(event, data)
        if event.message:
            await self.__send_ban_message(event.message)
        elif event.callback_query:
            await self.__send_ban_message(event.callback_query)
        raise CancelHandler()

    async def __send_ban_message(self, event: types.Message | types.CallbackQuery) -> None:
        from apps.tgbot.bot.main import bot
        if isinstance(event, types.CallbackQuery):
            await bot.edit_message_text(chat_id=event.message.chat.id, message_id=event.message.message_id,
                                        text=TEXT_BANNED)
        else:
            await bot.send_message(event.chat.id, TEXT_BANNED)
