from rest_framework import serializers
#from django.contrib.auth.models import User
from common.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    #old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserPasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'password'
        ]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ['username', 'password']
        fields = '__all__'
        
    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

class CreateUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('username', 'password')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_data):
    user = User(
        username=validated_data['username']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user