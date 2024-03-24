from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import UserExtended


@admin.action(description="Создать qrcode")
def generate_qrcode(model_admin, request, queryset: list[UserExtended]):
    for user in queryset:
        user.generate_qrcode()


@admin.register(UserExtended)
class UserExtendedAdmin(UserAdmin):
    """ Админка пользователя """
    actions = (generate_qrcode, )

    list_display = ('username', 'balance', 'is_active',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name',
            )}
         ),
        (_("Permissions"), {
            "fields": (
                "is_active", "is_superuser",
            )},
         ),
        (_("Дополнительная информация"), {
            'fields': (
                'balance', 'qrcode', 'church', 'know_from'
            )},
         ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
