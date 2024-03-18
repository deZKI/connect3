from django.contrib import admin


class UserExtendedAdmin(admin.ModelAdmin):
    """ Админка пользователя """
    list_display = ('telegram_id', 'name', 'surname', 'balance', 'is_confirmed',)
