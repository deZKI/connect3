from django.db import models

from apps.users.models import UserExtended


class Posts(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_ready = models.BooleanField(default=False, verbose_name='Готово')

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ["-id", ]


class PostsFiles(models.Model):
    post = models.ForeignKey(to=Posts, on_delete=models.CASCADE)
    image = models.FileField(upload_to='posts/files')


class PostsDelivered(models.Model):
    post = models.ForeignKey(to=Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserExtended, on_delete=models.CASCADE)
    is_delivered = models.BooleanField(default=False)
    time = models.DateTimeField(verbose_name='Receiving time')
