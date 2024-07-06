from typing import Any, Callable

from aiogram import types

from apps.users.models import UserExtended
from aiogram.fsm.context import FSMContext


def user_is_payed(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
    async def wrapper(event: types.Message) -> None:
        tg_user = event.from_user
        user = await UserExtended.objects.aget(tg_chat_id=tg_user.id, username=tg_user.username)
        if user.is_payed:
            await handler(event)

    return wrapper


def user_is_registered(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
    async def wrapper(event: types.Message) -> None:
        tg_user = event.from_user
        user = await UserExtended.objects.aget(tg_chat_id=tg_user.id, username=tg_user.username)
        if user.is_registered:
            await handler(event)

    return wrapper


def user_is_not_payed(handler: Callable[[Any], Any]) -> Callable[[Any], Any]:
    async def wrapper(event: types.Message) -> None:
        tg_user = event.from_user
        user = await UserExtended.objects.aget(tg_chat_id=tg_user.id, username=tg_user.username)
        if not user.is_payed:
            await handler(event)

    return wrapper


def user_is_not_registered(handler: Callable[[Any, Any], Any]) -> Callable[[Any], Any]:
    async def wrapper(event: types.Message, state: FSMContext) -> None:
        tg_user = event.from_user
        user = await UserExtended.objects.aget(tg_chat_id=tg_user.id, username=tg_user.username)
        if not user.is_registered:
            await handler(event, state)

    return wrapper
