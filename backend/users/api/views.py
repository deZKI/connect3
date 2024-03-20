from rest_framework.viewsets import ModelViewSet

from users.api.serializers import UsersSerializer
from users.models import UserExtended


class UsersViewSet(ModelViewSet):
    """ API endpoint пользователей """
    queryset = UserExtended.objects.all()
    serializer_class = UsersSerializer


