from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ['username', 'password']
        fields = '__all__'
        '''
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }
        '''

class UpdateUserPassSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'username': {'required': True},
            'password': {'required': True},
        }
    '''
    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value
	'''

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        #instance.first_name = validated_data['first_name']
        #instance.last_name = validated_data['last_name']
        #instance.email = validated_data['email']
        #instance.username = validated_data['username']
        instance.password = validated_data['password']
        instance.save()

        return instance