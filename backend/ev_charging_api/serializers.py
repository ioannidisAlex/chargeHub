from rest_framework import serializers

class UserTokenSerializer(serializers.Serializer):
    """get token for user"""
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, style={'input_type': 'password'})