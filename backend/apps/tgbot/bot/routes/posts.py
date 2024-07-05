from aiogram import types, Router, F

from ..consts import TEXT_POST
from ..keyboards import posts_inline_keyboard

posts_router = Router()


@posts_router.message(F.text == TEXT_POST)
async def show_posts(message: types.Message):
    await message.answer(TEXT_POST, reply_markup=await posts_inline_keyboard())


@posts_router.callback_query(F.data.startswith('post_'))
async def handle_post_callback(callback_query: types.CallbackQuery):
    from ..messages import send_post_to_user
    post_id = int(callback_query.data.split("_")[1])
    await send_post_to_user(post_id, callback_query.message.chat.id)
    await callback_query.answer()
