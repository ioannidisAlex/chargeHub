from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, permissions, generics, mixins, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from .serializers import UserSerializers
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token

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
    lookup_fields = ['username', 'password']  
    #lookup_field = 'pk'  
    serializer_class = UserSerializers
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    '''
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
            #print(username,'!!!!!!!!!!!!!!!!!!!\n')
            user=self.queryset.get(username=username)
            request.user=user
            request.user.password=password
            return self.update(request)
        except:
            request.data['username']=username
            request.data['password']=password
            return self.create(request)
        
    
    '''
    def put(self, request, pk=None):
        return self.update(request, pk)

    def delete(self, request, username):
        return self.destroy(request, username)
    '''

'''
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