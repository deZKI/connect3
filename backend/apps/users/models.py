import qrcode
from io import BytesIO

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.conf import settings


class UserExtended(AbstractUser):
    """ Пользователь (расширенная модель) """
    tg_chat_id = models.CharField(max_length=50, unique=True, verbose_name='Telegram ID', blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, verbose_name='Telegram Username', blank=True, null=True)

    phone_number = models.CharField(max_length=50, unique=True, verbose_name='Номер телефона', blank=True, null=True)
    birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    gender = models.CharField(max_length=20, choices=[('male', 'Мужской'), ('female', 'Женский')], verbose_name='Пол',
                              blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True, null=True)
    church = models.CharField(max_length=256, verbose_name='Название церкви', blank=True, null=True)
    know_from = models.TextField(max_length=256, verbose_name='Откуда узнал', blank=True, null=True)
    about_me = models.TextField(verbose_name='О себе', blank=True, null=True)

    qrcode = models.ImageField(upload_to='qrcodes/', verbose_name='QR-код пользователя', blank=True, null=True)

    is_payed = models.BooleanField(verbose_name='Оплачен', default=False)
    is_registered = models.BooleanField(verbose_name='Зарегистрирован', default=False)
    balance = models.PositiveIntegerField(default=1500, verbose_name='Баланс пользователя')

    is_banned = models.BooleanField(verbose_name='забанен', default=False)
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.is_payed and not self.is_registered:
            raise ValueError("Пользователь не может быть оплачен, если он не зарегистрирован")
        super().save(*args, **kwargs)

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

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id", ]


class Participant(models.Model):
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    inspiration = models.CharField(max_length=124)
    photo = models.ImageField(upload_to='participant/', verbose_name='Фото участника', blank=True, null=True)
