from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )
        return user


class UserCreateWithoutPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]
