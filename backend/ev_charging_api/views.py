from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import logout
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import UserTokenSerializer
from common.models import User

class UserLogin(APIView):
    """return user token if user credetials are correct"""
    serializer_class = UserTokenSerializer

    def get(self, request, format=None):
        """user sign in form"""
        serializer = UserTokenSerializer()
        return Response(status=status.HTTP_200_OK)

    def post(self, request, format=None):
        """post user request"""
        serializer = UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.data.get('username'),
                password=serializer.data.get('password'))
            if user is not None:
                token, create_or_fetch = Token.objects.get_or_create(
                    user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            msg = 'Wrong credentials. Please try again'
            return Response({'message': msg}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def home(request):
    return render(request, 'ev_charging_api/api.html')

'''
class LoginAPI(KnoxLoginView):
	permission_classes = (permissions.AllowAny,)
	renderer_classes = [TemplateHTMLRenderer]
	template_name='ev_charging_api/rest_login.html'

	def post(self, request, format=None):
		serializer = AuthTokenSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		login(request, user)
		return super(LoginAPI, self).post(request, format=None)
'''

class Logout(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'ev_charging_api/rest_logout.html'
    
	def get(self, request, format=None):
		# simply delete the token to force a login
		request.user.auth_token.delete()
		logout(request)
		return Response(status=status.HTTP_200_OK)