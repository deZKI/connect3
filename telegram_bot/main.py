import asyncio
import logging
import os
import sys
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import aio_pika

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


async def send_post_with_images(user_id, message, images):
    await bot.send_message(chat_id=user_id, text=message)
    for image_url in images:
        await bot.send_photo(chat_id=user_id, photo=image_url)


def callback(ch, method, properties, body):
    post_data = json.loads(body)
    title = post_data['title']
    description = post_data['description']
    images = post_data.get('images', [])
    telegram_ids = post_data.get('telegram_ids', [])  # Получаем список ID

    message = f"{title}\n\n{description}"

    for user_id in telegram_ids:
        asyncio.create_task(send_post_with_images(user_id, message, images))


async def setup_rabbitmq_listener(loop):
    # Подключение к RabbitMQ
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/", loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue('posts_queue', durable=False)
    await queue.consume(callback=callback)


@dp.message(Command("start"))
async def echo_message(msg: types.Message):
    await msg.answer(msg.text)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    loop = asyncio.get_running_loop()
    await setup_rabbitmq_listener(loop)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
