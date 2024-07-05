from aiogram import types, Router, F
from asgiref.sync import sync_to_async

from apps.posts.models import Posts, PostsFiles
from ..consts import TEXT_POST
from ..keyboards import posts_inline_keyboard

posts_router = Router()


@posts_router.message(F.text == TEXT_POST)
async def show_posts(message: types.Message):
    await message.answer(TEXT_POST, reply_markup=await posts_inline_keyboard())


@posts_router.callback_query(F.data.startswith('post_'))
async def handle_post_callback(callback_query: types.CallbackQuery):
    from ..main import bot
    post_id = callback_query.data.split("_")[1]
    post = await sync_to_async(Posts.objects.get)(id=post_id)
    post_files = await sync_to_async(list)(PostsFiles.objects.filter(post=post))

    message_text = (
        f"Заголовок: {post.title}\n"
        f"Описание: {post.description}\n"
        f"Дата создания: {post.created}"
    )

    # Отправляем текстовое сообщение
    await callback_query.message.answer(message_text)

    # Отправляем каждое изображение
    for post_file in post_files:
        await bot.send_photo(chat_id=callback_query.message.chat.id, photo=post_file.image.url)

    await callback_query.answer()
