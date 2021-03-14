from django.contrib.auth import authenticate
from rest_framework import serializers

from common.models import ChargingStation, Location, Payment, Session, User, Vehicle


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"


class KWSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "kwh_delivered"


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

        fields = ("username", "password", "is_staff", "is_superuser")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            is_staff=validated_data["is_staff"],
            is_superuser=validated_data["is_superuser"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ("file",)


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingStation

        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location

        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment

        fields = "__all__"


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle

        fields = "__all__"
