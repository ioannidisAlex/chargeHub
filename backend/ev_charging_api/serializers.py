from rest_framework import serializers
from django.contrib.auth.models import User as AuthUser
from common.models import User, Session
from rest_framework import serializers
from django.contrib.auth import authenticate

class SessionSerializer(serializers.ModelSerializer):
    class Meta:    
        model = Session
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    class Meta:    
        model = User

        """
        Serializer for password change endpoint.
        """
        #old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)

class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        #fields = ['username', 'password']
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ['username', 'password']
        fields = '__all__'

'''
class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=128, write_only=True)
    #token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password is not found.'
            )
        try:
            #payload = JWT_PAYLOAD_HANDLER(user)
            token = Token.objects.get_or_create(user=user)
            #update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with this username and password does not exist'
            )
        return {
            'username':user.username,
            'token': token
        }
'''
    
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