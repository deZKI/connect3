import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File
from apps.posts.models import Posts, PostsFiles
from apps.products.models import Product

# Примерные данные для генерации
PRODUCT_NAMES = [
    "Кофе Espresso",
    "Капучино с корицей",
    "Чай с мятой",
    "Свежесваренный горячий шоколад",
    "Ароматный чёрный чай",
    "Пирожки с мясом",
    "Пицца Маргарита",
    "Сырники с вареньем",
    "Фруктовый салат",
    "Салат Цезарь",
]
IMAGES_DIRECTORY = "C:/Users/kiril/Desktop/картинки"
PRODUCT_DESCRIPTIONS = [
    "Ароматный кофе с насыщенным вкусом и приятным ароматом.",
    "Капучино с добавлением корицы для пикантного вкуса.",
    "Чай с мятой - отличный выбор для освежения в любое время дня.",
    "Нежный шоколад с топингом и взбитыми сливками.",
    "Классический чёрный чай с приятным ароматом и насыщенным вкусом.",
    "Сочные пирожки с мясом, приготовленные по традиционному рецепту.",
    "Пицца с томатным соусом, сыром Моцарелла и свежими травами.",
    "Сырники с творогом и ароматным вареньем - отличный выбор для завтрака или полдника.",
    "Свежие фрукты, нарезанные и поданые с добавлением мёда и орехов.",
    "Классический салат с сочными листьями салата, курицей, сухариками и соусом Цезарь.",
]


class Command(BaseCommand):
    help = 'Generate sample data for Posts and Products'

    def handle(self, *args, **kwargs):
        # Генерация постов
        for _ in range(10):
            title = random.choice(PRODUCT_NAMES)
            description = random.choice(PRODUCT_DESCRIPTIONS)
            post = Posts.objects.create(
                title=title,
                description=description,
                is_ready=True  # Пример значения для is_ready
            )

            # Загрузка изображения для каждого поста
            self.upload_random_image(post)

            # Генерация товаров
            for _ in range(10):
                product_name = f"{random.choice(PRODUCT_NAMES)} {random.choice(PRODUCT_NAMES)}"
                product = Product.objects.create(
                    name=product_name,
                    price=random.randint(10, 1000),  # Пример случайной цены
                    available=True  # Пример значения для available
                )

        self.stdout.write(self.style.SUCCESS('Sample data has been generated successfully'))

    def upload_random_image(self, post):
        # Загрузка случайного изображения для поста
        if os.path.isdir(IMAGES_DIRECTORY):
            image_files = os.listdir(IMAGES_DIRECTORY)
            if image_files:
                image_filename = random.choice(image_files)
                image_path = os.path.join(IMAGES_DIRECTORY, image_filename)
                with open(image_path, 'rb') as image_file:
                    post_file = PostsFiles.objects.create(
                        post=post,
                        image=File(image_file, name=image_filename)
                    )
