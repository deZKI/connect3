from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.products.admin import OrderInlineAdmin
from apps.users.models import UserExtended, Teammate, Speakers


@admin.action(description="Создать qrcode")
def generate_qrcode(model_admin, request, queryset: list[UserExtended]):
    for user in queryset:
        user.generate_qrcode()


@admin.register(UserExtended)
class UserExtendedAdmin(UserAdmin):
    """ Админка пользователя """
    actions = (generate_qrcode,)

    list_display = ('id', 'first_name', 'last_name', 'balance', 'is_active', 'is_banned', 'is_payed', 'birth_date')
    list_filter = ('is_active', 'is_banned', 'church', 'city', 'gender', 'is_payed',)
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    sortable_by = ('birth_date', 'balance',)

    inlines = [OrderInlineAdmin]
    fieldsets = (
        (None, {'fields': ('username', 'password', 'tg_chat_id')}),
        (_('Personal info'), {
            'fields': (
                'first_name', 'last_name', 'photo'
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
                ('balance', 'qrcode', 'know_from', 'phone_number',),
                ('about_me', 'city', 'church', 'gender', 'birth_date')
            )},
         ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(Teammate)
class TeammateAdmin(admin.ModelAdmin):
    pass


@admin.register(Speakers)
class SpeakersAdmin(admin.ModelAdmin):
    pass
