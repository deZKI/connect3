from django.db import models

from django.contrib.auth.models import AbstractUser


class UserExtended(AbstractUser):
    """ Пользователь (расширенная модель) """
    username = models.CharField(max_length=50, unique=True, verbose_name='Telegram ID')
    qrcode = models.ImageField(upload_to='qrcodes/', verbose_name='Qrcode пользователя ')
    church = models.CharField(max_length=256, verbose_name='Название церкви', blank=True, null=True)
    know_from = models.CharField(max_length=256, verbose_name='Откуда узнал', blank=True, null=True)
    balance = models.PositiveIntegerField(default=1500, verbose_name='Баланс пользователя')

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id", ]
