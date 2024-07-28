from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from apps.users.models import UserExtended, Participant

from apps.users.api.serializers import UserRegistrationSerializer, UserDetailWithBalanceSerializer, \
    UserDetailsSerializer, ParticipantSerializer


class UserRegistrationView(CreateAPIView):
    queryset = UserExtended.objects.all()
    serializer_class = UserRegistrationSerializer


class UserDetailView(RetrieveAPIView):
    queryset = UserExtended.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_superuser or user == self.get_object():
            # Only superuser of user himself can seed balance
            return UserDetailWithBalanceSerializer

        return UserDetailsSerializer


class ParticipationListView(ReadOnlyModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
