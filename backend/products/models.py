from django.db import models

from users.models import UserExtended


class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')

    def __str__(self):
        return f'{self.name} - {self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='товар')
    user = models.ForeignKey(to=UserExtended, on_delete=models.CASCADE, verbose_name='пользователь')
    time = models.DateTimeField(auto_created=True, verbose_name='время')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'