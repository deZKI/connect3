import pika
import json

from django.contrib import admin
from django.conf import settings

from posts.models import Posts, PostsFiles, PostsDelivered
from users.models import UserExtended


def send_posts_to_mq(modeladmin, request, queryset):
    rabbitmq_settings = settings.RABBITMQ
    credentials = pika.PlainCredentials(
        rabbitmq_settings["USER"],
        rabbitmq_settings["PASSWORD"]
    )

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_settings["HOST"],
            port=rabbitmq_settings["PORT"],
            virtual_host='/',
            credentials=credentials
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='posts_queue', durable=False)

    for post in queryset:
        post_files = post.postsfiles_set.all()
        images = [post_file.image.url for post_file in post_files]
        telegram_ids = list(UserExtended.objects.all().values_list('username', flat=True))

        post_data = {
            'title': post.title,
            'description': post.description,
            'images': images,
            'telegram_ids': telegram_ids,
        }

        channel.basic_publish(
            exchange='',
            routing_key='posts_queue',
            body=json.dumps(post_data)
        )

    connection.close()


send_posts_to_mq.short_description = 'Отправить выбранные посты в RabbitMQ для рассылки'


class PostsFilesInlineAdmin(admin.TabularInline):
    model = PostsFiles


class PostsDeliveredInlineAdmin(admin.TabularInline):
    model = PostsDelivered


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title']
    inlines = [PostsFilesInlineAdmin, PostsDeliveredInlineAdmin]
    actions = [send_posts_to_mq]
