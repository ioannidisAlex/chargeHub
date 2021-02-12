from django.contrib.auth import authenticate
from rest_framework import serializers

from common.models import Session, User


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['username', 'password']
        fields = "__all__"

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "email", 'is_staff', 'is_superuser')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(username=validated_data["username"], email=validated_data['email'] ,is_staff=validated_data['is_staff'], is_superuser=validated_data['is_superuser'])
        user.set_password(validated_data["password"])
        user.save()
        return user

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ('file',)