from rest_framework import serializers
from apps.users.models import UserExtended, Participant


class UserRegistrationSerializer(serializers.ModelSerializer):
    """ Serializer for user registration """

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserExtended
        fields = ['tg_chat_id', 'password', 'password2', 'first_name', 'last_name', 'church', 'know_from']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data.pop('password2', None)
        user = UserExtended.objects.create_user(**validated_data)
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    """ Serializer for user details """

    class Meta:
        model = UserExtended
        fields = ['tg_chat_id', 'qrcode', 'first_name', 'last_name', 'church', 'know_from']


class UserDetailWithBalanceSerializer(UserDetailsSerializer):
    """ Serializer for user data with balance """

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ['balance']


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ('pk', 'name', 'surname', 'inspiration', 'photo')
