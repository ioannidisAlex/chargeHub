from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, permissions, generics, mixins, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import UserSerializers, UpdateUserPassSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from rest_framework.views import APIView

'''
class ChangePasswordView(UpdateAPIView):
        """
        An endpoint for changing password.
        """
        #lookup_fields = ['username', 'password']  
        lookup_field = 'username'
        serializer_class = ChangePasswordSerializer
        model = User
        authentication_classes = [TokenAuthentication]
        queryset = User.objects.all()
        permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None, username=None):
            obj = self.queryset.get(username=username)
            return obj

        def update(self, request, username, *args, **kwargs):
            self.object = self.get_object(self.queryset, username)
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
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
'''

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    lookup_fields = ['username', 'password']  
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UpdateUserPassSerializer

    @action(detail=True, methods=['post'])
    def set_password(self, request, username=None, password=None):
        user=self.queryset.get(username=username)
        serializer = UpdateUserPassSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False)
    def recent_users(self, request):
        recent_users = User.objects.all().order_by('-last_login')

        page = self.paginate_queryset(recent_users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(recent_users, many=True)
        return Response(serializer.data)

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
    serializer_class = UserSerializers
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_fields = ['username', 'password']  
    #lookup_field = 'username'  
    '''
    def create(self, request):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request):
        user=self.request.user
        serializer=UserSerializers(user)
        serializer.data['password']=request.user.password        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''
    
    def post(self, request, username=None, password=None):
        try:
            user=self.queryset.get(username=username)
            request.user=user
            request.user.password=password
            print("hi!!!!!!\n")
            return self.update(request)
        except:
            request.data['username']=username
            request.data['password']=password
            return self.create(request)

    def put(self, request):
        serializer = UserSerializers(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    '''
    def put(self, request, id=None, username=None, password=None):
        user=self.queryset.get(username=username)
        #id=user.id
        request.user=user
        request.user.password=password
        return self.update(request, id)
    
    def delete(self, request, username):
        return self.destroy(request, username)

    class CreateOrUpdateUserViewSet(viewsets.ModelViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.UpdateModelMixin, mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin, MultipleFieldLookupMixin):
        serializer_class = UserSerializer
        queryset = User.objects.all()
        #lookup_fields = ['username', 'password']  
        lookup_field = 'username' 
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        
        def post(self, request, username):
            if User.objects.filter(username=username).exists():
                if serializer_class.is_valid():
                    return self.update(request, password)
            else:
                return self.create(request)
    '''

class LoginView(APIView):

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UsersViewSet(viewsets.ViewSet):
    '''
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    '''
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'  
    
    def retrieve(self, request, username):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializers(user)
        return Response(serializer.data)