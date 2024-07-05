from asgiref.sync import sync_to_async
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from apps.posts.models import Posts

async def posts_inline_keyboard():
    keyboard = InlineKeyboardBuilder()

    # Получаем все посты асинхронно
    posts = await sync_to_async(list)(Posts.objects.filter(is_ready=True))

    # Добавляем кнопку для каждого поста
    for post in posts:
        keyboard.add(InlineKeyboardButton(text=post.title, callback_data=f"post_{post.id}"))

    # Возвращаем клавиатуру
    return keyboard.as_markup()

