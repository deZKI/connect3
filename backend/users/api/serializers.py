from rest_framework.serializers import ModelSerializer

from users.models import UserExtended


class UsersSerializer(ModelSerializer):
    """ Сериализатор пользователя """

    class Meta:
        model = UserExtended
        fields = ('id', 'username', 'email', 'password')
