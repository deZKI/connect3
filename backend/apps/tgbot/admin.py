from django.contrib import admin

from apps.tgbot.models import Siteconfig


@admin.register(Siteconfig)
class TelegramBotConfigAdmin(admin.ModelAdmin):
    pass
