import qrcode
from io import BytesIO

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.conf import settings


class UserExtended(AbstractUser):
    """ Пользователь (расширенная модель) """
    username = models.CharField(max_length=50, unique=True, verbose_name='Telegram ID')
    qrcode = models.ImageField(upload_to='qrcodes/', verbose_name='Qrcode пользователя ', blank=True, null=True)
    church = models.CharField(max_length=256, verbose_name='Название церкви', blank=True, null=True)
    know_from = models.CharField(max_length=256, verbose_name='Откуда узнал', blank=True, null=True)
    balance = models.PositiveIntegerField(default=1500, verbose_name='Баланс пользователя')

    REQUIRED_FIELDS = []

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )
        qr.add_data(f'{settings.SITE_URL}/users/{self.pk}')
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'qrcode_{self.pk}.png'
        file_buffer = ContentFile(buffer.getvalue())
        self.qrcode.save(filename, file_buffer)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id", ]
