from django.contrib import admin

from products.models import Product, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'time']


class OrderInlineAdmin(admin.TabularInline):
    model = Order
    verbose_name = 'Заказ пользователя'
    verbose_name_plural = 'Заказы пользователя'

