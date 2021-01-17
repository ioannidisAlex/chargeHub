from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, permissions, generics, mixins, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializer, CreateUserSerializer, ChangePasswordSerializer
#from django.contrib.auth.models import User
from common.models import User
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, UpdateAPIView
'''
import hashlib
def encrypt_string(hash_string):
    sha_signature = \
        hashlib.sha256(hash_string.encode()).hexdigest()
    return sha_signature
'''

class ChangePasswordView(UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsAuthenticated,)

        def update(self, request, username, password, *args, **kwargs):
            self.object = User.objects.get(username=username)
            serializer = self.get_serializer(data={'new_password': password})

            if serializer.is_valid():
                # Check old password
                #if not self.object.check_password(serializer.data.get("old_password")):
                #    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CSRFGeneratorView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response(csrf_token)

class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]: # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

class UsermodAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, MultipleFieldLookupMixin):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    #lookup_fields = ['username', 'password', 'id']  
    #lookup_field = 'id'  
    
    def post(self, request, username=None, password=None):
        try:
            #print("HEREEEE!!!",request.values(),"\n")
            self.object = User.objects.get(username=username)
            serializer = ChangePasswordSerializer(data={'new_password': password})

            if serializer.is_valid():
                # Check old password
                #if not self.object.check_password(serializer.data.get("old_password")):
                #    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            data = {
            'username': username,
            'password': password
            }
            serializer = CreateUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        return self.update(request, pk)

class LoginView(APIView):

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class RetrieveUserViewSet(viewsets.ViewSet):
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    lookup_field = 'username'  
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    def retrieve(self, request, username=None):
        user = get_object_or_404(self.queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)
