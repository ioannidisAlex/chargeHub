import json
from datetime import datetime
from json import JSONEncoder

from django.contrib.auth.models import User as AuthUser
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connections
from django.db.utils import OperationalError
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, mixins, permissions, serializers, status, viewsets
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Session, User

from ..serializers import (
    AuthUserSerializer,
    ChangePasswordSerializer,
    CreateUserSerializer,
    SessionSerializer,
    UserSerializer,
)


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            "user": str(request.user),  # `django.contrib.auth.User` instance.
            "auth": str(request.auth),  # None
        }
        return Response(content)


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
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:  # Ignore empty fields.
                filter[field] = self.kwargs[field]
        obj = get_object_or_404(queryset, **filter)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj


class UsermodAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "ev_charging_api/detail.html"
    lookup_fields = [
        "username",
        "password",
    ]
    # lookup_field = 'id'

    def post(self, request, username=None, password=None):
        try:
            self.object = User.objects.get(username=username)
            serializer = ChangePasswordSerializer(data={"new_password": password})

            if serializer.is_valid():
                #### Check old password
                # if not self.object.check_password(serializer.data.get("old_password")):
                #    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                #### set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    "status": "success",
                    "code": status.HTTP_200_OK,
                    "message": "Password updated successfully",
                    "data": [],
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except:
            data = {"username": username, "password": password}
            serializer = CreateUserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
    ):
        response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Logged out succesfully",
            "data": [],
        }
        return Response(response)


class RetrieveUserViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = "username"
    serializer_class = AuthUserSerializer
    queryset = AuthUser.objects.all()

    def retrieve(self, request, username=None):
        user = get_object_or_404(self.queryset, username=username)
        serializer = AuthUserSerializer(user)
        return Response(serializer.data)

    def list(self, request):
        print("This is the query set :", self.queryset.__dict__, "HIIIII!!!!!\n")
        serializer = AuthUserSerializer(self.queryset, many=True)
        return Response(serializer.data)


class SessionsPerPointView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id=None, date_from=None, date_to=None):
        year_from = int(date_from[:4])
        month_from = int(date_from[4:6])
        day_from = int(date_from[6:8])
        year_to = int(date_to[:4])
        month_to = int(date_to[4:6])
        day_to = int(date_to[6:8])
        range_left = datetime(
            year_from, month_from, day_from, 12, 0, 0, 0, tzinfo=timezone.utc
        )
        range_right = datetime(
            year_to, month_to, day_to, 12, 0, 0, 0, tzinfo=timezone.utc
        )
        sessions = self.queryset.filter(charging_point__id=id).filter(
            connect_time__range=[range_left, range_right]
        )
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)


class SessionsPerStationView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id=None, date_from=None, date_to=None):
        year_from = int(date_from[:4])
        month_from = int(date_from[4:6])
        day_from = int(date_from[6:8])
        year_to = int(date_to[:4])
        month_to = int(date_to[4:6])
        day_to = int(date_to[6:8])
        range_left = datetime(
            year_from, month_from, day_from, 12, 0, 0, 0, tzinfo=timezone.utc
        )
        range_right = datetime(
            year_to, month_to, day_to, 12, 0, 0, 0, tzinfo=timezone.utc
        )
        sessions = self.queryset.filter(charging_point__charging_station=id).filter(
            connect_time__range=[range_left, range_right]
        )
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)


class SessionsPerVehicleView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id=None, date_from=None, date_to=None):
        year_from = int(date_from[:4])
        month_from = int(date_from[4:6])
        day_from = int(date_from[6:8])
        year_to = int(date_to[:4])
        month_to = int(date_to[4:6])
        day_to = int(date_to[6:8])
        range_left = datetime(
            year_from, month_from, day_from, 12, 0, 0, 0, tzinfo=timezone.utc
        )
        range_right = datetime(
            year_to, month_to, day_to, 12, 0, 0, 0, tzinfo=timezone.utc
        )
        sessions = self.queryset.filter(vehicle__id=id).filter(
            connect_time__range=[range_left, range_right]
        )
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)


class SessionsPerProviderView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id=None, date_from=None, date_to=None):
        year_from = int(date_from[:4])
        month_from = int(date_from[4:6])
        day_from = int(date_from[6:8])
        year_to = int(date_to[:4])
        month_to = int(date_to[4:6])
        day_to = int(date_to[6:8])
        range_left = datetime(
            year_from, month_from, day_from, 12, 0, 0, 0, tzinfo=timezone.utc
        )
        range_right = datetime(
            year_to, month_to, day_to, 12, 0, 0, 0, tzinfo=timezone.utc
        )
        sessions = self.queryset.filter(provider__id=id).filter(
            connect_time__range=[range_left, range_right]
        )
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)


class HealthcheckView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        db_conn = connections["default"]
        try:
            c = db_conn.cursor()
            response = {"status": "OK"}
            return Response(response)

        except:
            response = {"status": "failed"}
            return Response(response)


class ResetSessionsView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def post(self, request):
        try:
            self.queryset.delete()
            admin_user = {
                "username": "admin",
                "password": "petrol4ever",
                "is_superuser": True,
                "is_staff": True,
            }
            response = {
                "status": "OK",
            }
            serializer = UserSerializer(data=admin_user)
            if serializer.is_valid():
                serializer.save()
            return Response(response)

        except:
            response = {"status": "failed"}
            return Response(response)


class CustomAuthToken(ObtainAuthToken):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "ev_charging_api/detail.html"

    def get(self, request):
        serializer = UserLoginSerializer()
        return Response(
            {
                "serializer": serializer,
            }
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})
