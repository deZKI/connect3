from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.products.admin import OrderInlineAdmin
from apps.users.models import UserExtended, Participant


@admin.action(description="Создать qrcode")
def generate_qrcode(model_admin, request, queryset: list[UserExtended]):
    for user in queryset:
        user.generate_qrcode()


@admin.register(UserExtended)
class UserExtendedAdmin(UserAdmin):
    """ Админка пользователя """
    actions = (generate_qrcode,)

    list_display = ('username', 'balance', 'is_active', 'is_banned', 'is_payed')
    inlines = [OrderInlineAdmin]
    fieldsets = (
        (None, {'fields': ('username', 'password', 'tg_chat_id')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name',
            )}
         ),
        (_("Permissions"), {
            "fields": (
                'is_banned', 'is_registered', 'is_payed',
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


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass