from rest_framework import serializers
from apps.users.models import UserExtended, Teammate, Speakers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = ('pk', 'first_name', 'last_name', 'photo')


class UserExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = ('pk', 'first_name', 'last_name', 'photo', 'about_me', 'church', 'birth_date')


class TeammateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teammate
        fields = ('pk', 'name', 'surname', 'inspiration', 'photo')


class SpeakersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speakers
        fields = ('pk', 'name', 'surname', 'inspiration', 'photo')
