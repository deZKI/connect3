from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.users.models import UserExtended, Teammate, Speakers

from apps.users.api.serializers import TeammateSerializer, UserSerializer, UserExtendedSerializer, SpeakersSerializer


class UsersListView(ReadOnlyModelViewSet):
    queryset = UserExtended.objects.filter(is_payed=True, is_banned=False)
    serializer_class = UserSerializer

    def get_serializer_class(self):
        return UserExtendedSerializer

    def retrieve(self, request, *args, **kwargs):
        # Переопределяем метод retrieve для поиска по tg_chat_id
        tg_chat_id = kwargs.get('pk')  # Используем параметр pk как tg_chat_id

        # Пытаемся найти пользователя по tg_chat_id
        user = get_object_or_404(UserExtended, tg_chat_id=tg_chat_id)

        # Сериализуем данные пользователя и возвращаем ответ
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class TeammateListView(ReadOnlyModelViewSet):
    queryset = Teammate.objects.all()
    serializer_class = TeammateSerializer


class SpeakersListView(ReadOnlyModelViewSet):
    queryset = Speakers.objects.all()
    serializer_class = SpeakersSerializer
