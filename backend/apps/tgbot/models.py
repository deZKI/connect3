from django.core.exceptions import ValidationError
from django.db import models

from apps.users.models import UserExtended


class Siteconfig(models.Model):
    is_available = models.BooleanField(default=True)
    welcome_text = models.TextField(verbose_name="Приветственное письмо в тг боте", max_length=255)
    what_is_connect = models.TextField(verbose_name="Что такое connect3?", max_length=255)
    kitchen_admin = models.ForeignKey(to=UserExtended, verbose_name="Главный на кухне", on_delete=models.CASCADE,
                                      related_name='kitchen_admin_siteconfigs')
    main_admin = models.ForeignKey(to=UserExtended, verbose_name="Главный админ", on_delete=models.CASCADE,
                                   related_name='main_admin_siteconfigs')

    def save(self, *args, **kwargs):
        if not self.pk and Siteconfig.objects.exists():
            raise ValidationError('Одни настройки')
        return super(Siteconfig, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"
