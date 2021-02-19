import csv
import io
import json
from datetime import datetime
from json import JSONEncoder

import pysnooper
from django.core.serializers.json import DjangoJSONEncoder
from django.db import connections
from django.db.models import Sum
from django.db.utils import OperationalError
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import (
    filters,
    generics,
    mixins,
    permissions,
    serializers,
    status,
    viewsets,
)
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
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_csv import renderers as r

from common.models import ChargingPoint, Session, User
from ev_charging_api.authentication import CustomTokenAuthentication

from ..serializers import (
    AdminUserSerializer,
    CreateUserSerializer,
    FileUploadSerializer,
    SessionSerializer,
    UserSerializer,
)

"""
class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class CSRFGeneratorView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response(csrf_token)
"""


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
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    lookup_fields = [
        "username",
        "password",
    ]

    def post(self, request, username, password):
        form = request.GET.get("form", "")
        try:
            self.object = User.objects.get(username=username)
            self.object.set_password(password)
            self.object.save()

            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
            if form == "csv":
                renderer = r.CSVRenderer()
                return Response(renderer.render(data=response))
            return Response(response)

        except:
            data = {"username": username, "password": password}
            serializer = CreateUserSerializer(data=data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                if form == "csv":
                    renderer = r.CSVRenderer()
                    return Response(renderer.render(data=serializer.data))
                else:
                    return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(
        self,
        request,
    ):
        form = request.GET.get("form", "")
        response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Logged out succesfully",
            "data": [],
        }
        if form == "csv":
            renderer = r.CSVRenderer()
            return Response(renderer.render(data=response))
        else:
            return Response(response)


class RetrieveUserViewSet(viewsets.ViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = "username"
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, username=None):
        form = request.query_params.get("form", None)
        user = get_object_or_404(self.queryset, username=username)
        serializer = UserSerializer(user)
        if form == "csv":
            renderer = r.CSVRenderer()
            return Response(renderer.render(data=serializer.data))
        else:
            return Response(serializer.data)

    def list(self, request):
        form = request.query_params.get("form", None)
        serializer = UserSerializer(self.queryset, many=True)
        if form == "csv":
            renderer = r.CSVRenderer()
            return Response(renderer.render(data=serializer.data))
        else:
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
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id, date_from, date_to):
        form = request.GET.get("form", "")
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
        # serializer = SessionSerializer(sessions, many=True)
        sessions_list = []
        session_index = 0
        for s in sessions:
            sessions_list.append({})
            sessions_list[session_index]["SessionIndex"] = session_index
            sessions_list[session_index]["SessionID"] = s.id
            sessions_list[session_index]["StartedOn"] = s.connect_time
            sessions_list[session_index]["FinishedOn"] = s.done_charging_time
            sessions_list[session_index]["Protocol"] = s.protocol
            sessions_list[session_index]["EnergyDelivered"] = s.kwh_delivered
            sessions_list[session_index]["Payment"] = s.payment.payment_method
            sessions_list[session_index]["VehicleType"] = s.vehicle.model.engine_type
            session_index += 1

        response = {
            "Point": id,
            "PointOperator": sessions.first().charging_point.charging_station.owner.id,
            "RequestTimestamp": datetime.now(),
            "PeriodFrom": range_left,
            "PeriodTo": range_right,
            "NumberOfChargingSessions": sessions.count(),
            "ChargingSessionsList": sessions_list,
            # sessions need more fields!!!
        }
        if form == "csv":
            renderer = r.CSVRenderer()
            return Response(renderer.render(data=response))
        else:
            return Response(response)


class SessionsPerStationView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id, date_from, date_to):
        form = request.GET.get("form", "")
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
        sessions = self.queryset.filter(charging_point__charging_station_id=id).filter(
            connect_time__range=[range_left, range_right]
        )
        # active_points = list(sessions.order_by().values("charging_point").distinct())
        # points_to_remove = []
        # for i in range(len(active_points)):
        #    if (
        #        ChargingPoint.objects.all()
        #        .get(id=active_points[i]["charging_point"])
        #        .is_active
        #        == 2
        #    ):
        #        points_to_remove.append(active_points[i])
        # for i in points_to_remove:
        #    active_points.remove(i)

        sessions_list = []
        for s in sessions:
            boolean = True
            for d in sessions_list:
                if s.charging_point.id == d["PointID"]:
                    d["PointSessions"] += 1
                    d["EnergyDelivered"] += s.kwh_delivered
                    boolean = False
                    break
            if boolean:
                sessions_list.append(
                    {
                        "PointID": s.charging_point.id,
                        "PointSessions": 1,
                        "EnergyDelivered": s.kwh_delivered,
                    }
                )
        response = {
            "StationID": id,
            "Operator": sessions.first().charging_point.charging_station.owner.id,
            "RequestTimestamp": datetime.now(),
            "PeriodFrom": range_left,
            "PeriodTo": range_right,
            "TotalEnergyDelivered": sessions.aggregate(Sum("kwh_delivered"))[
                "kwh_delivered__sum"
            ],
            "NumberOfChargingSessions": sessions.count(),
            "NumberOfActivePoints": len(sessions_list),
            "SessionsSummaryList": sessions_list,
            # sessions need more fields!!!
        }
        if form == "csv":
            renderer = r.CSVRenderer()
            return Response(renderer.render(data=response))
        else:
            return Response(response)


class SessionsPerVehicleView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id, date_from, date_to):
        form = request.GET.get("form", "")
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
        # serializer = SessionSerializer(sessions, many=True)
        sessions_list = []
        session_index = 0
        for s in sessions:
            sessions_list.append({})
            sessions_list[session_index]["SessionIndex"] = session_index
            sessions_list[session_index]["SessionID"] = s.id
            sessions_list[session_index]["EnergyProvider"] = s.provider.id
            sessions_list[session_index]["StartedOn"] = s.connect_time
            sessions_list[session_index]["FinishedOn"] = s.done_charging_time
            sessions_list[session_index]["Protocol"] = s.protocol
            sessions_list[session_index]["EnergyDelivered"] = s.kwh_delivered
            sessions_list[session_index]["PricePolicyRef"] = s.payment.invoice
            sessions_list[session_index]["CostPerKWh"] = (
                s.payment.cost / s.kwh_delivered
            )
            sessions_list[session_index]["SessionCost"] = s.payment.cost
            session_index += 1
        response = {
            "VehicleID": id,
            "RequestTimestamp": datetime.now(),
            "PeriodFrom": range_left,
            "PeriodTo": range_right,
            "TotalEnergyDelivered": sessions.aggregate(Sum("kwh_delivered"))[
                "kwh_delivered__sum"
            ],
            "NumberOfVisitedPoints": sessions.order_by()
            .values("charging_point")
            .distinct()
            .count(),
            "NumberOfVehicleChargingSessions": sessions.count(),
            "VehicleChargingSessionsList": sessions_list,
        }
        if form == "csv":
            renderer = r.CSVRenderer()
            return Response(renderer.render(data=response))
        else:
            return Response(response)


class SessionsPerProviderView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id, date_from, date_to):
        form = request.GET.get("form", "")
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
        sessions_list = []
        session_index = 0
        for s in sessions:
            sessions_list.append({})
            sessions_list[session_index][
                "StationID"
            ] = s.charging_point.charging_station.id
            sessions_list[session_index]["SessionID"] = s.id
            sessions_list[session_index]["VehicleID"] = s.vehicle.id
            sessions_list[session_index]["StartedOn"] = s.connect_time
            sessions_list[session_index]["FinishedOn"] = s.done_charging_time
            sessions_list[session_index]["Protocol"] = s.protocol
            sessions_list[session_index]["EnergyDelivered"] = s.kwh_delivered
            sessions_list[session_index]["PricePolicyRef"] = s.payment.invoice
            sessions_list[session_index]["CostPerKWh"] = (
                s.payment.cost / s.kwh_delivered
            )
            sessions_list[session_index]["SessionCost"] = s.payment.cost
            session_index += 1
        response = {
            "ProviderID": id,
            "ProviderName": sessions.first().provider.provider_name,
            "SessionsList": sessions_list,
        }
        if form == "csv":
            renderer = r.CSVRenderer()
            return Response(renderer.render(data=response))
        else:
            return Response(response)


class HealthcheckView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        form = request.GET.get("form", "")
        db_conn = connections["default"]
        try:
            c = db_conn.cursor()
            response = {"status": "OK"}
            if form == "csv":
                renderer = r.CSVRenderer()
                return Response(renderer.render(data=response))
            else:
                return Response(response)

        except:
            response = {"status": "failed"}
            if form == "csv":
                renderer = r.CSVRenderer()
                return Response(renderer.render(data=response))
            else:
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
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = [SessionSerializer]
    queryset = Session.objects.all()

    def post(self, request):
        form = request.GET.get("form", "")
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
            serializer = AdminUserSerializer(data=admin_user)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
            if form == "csv":
                renderer = r.CSVRenderer()
                return Response(renderer.render(data=response))
            else:
                return Response(response)

        except:
            raise
            response = {"status": "failed"}
            if form == "csv":
                renderer = r.CSVRenderer()
                return Response(renderer.render(data=response))
            else:
                return Response(response)


class SessionsupdView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    MultipleFieldLookupMixin,
):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = FileUploadSerializer
    queryset = Session.objects.all()

    def post(self, request, *args, **kwargs):
        form = request.GET.get("form", "")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data["file"]
        decoded_file = file.read().decode()
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string)
        sessions_count = 0
        imported_count = 0
        for row in reader:
            sessions_count += 1
            c_year = int(row[3][:4])
            c_month = int(row[3][4:6])
            c_day = int(row[3][6:8])
            c_hour = int(row[3][8:10])
            c_minutes = int(row[3][10:12])
            d_year = int(row[4][:4])
            d_month = int(row[4][4:6])
            d_day = int(row[4][6:8])
            d_hour = int(row[4][8:10])
            d_minutes = int(row[4][10:12])
            done_year = int(row[5][:4])
            done_month = int(row[5][4:6])
            done_day = int(row[5][6:8])
            done_hour = int(row[5][8:10])
            done_minutes = int(row[5][10:12])
            session = {
                "user_comments_ratings": row[0],
                "provider": row[1],
                "kwh_delivered": row[2],
                "connect_time": datetime(
                    c_year, c_month, c_day, c_hour, c_minutes, 0, 0, tzinfo=timezone.utc
                ),
                "disconnect_time": datetime(
                    d_year, d_month, d_day, d_hour, d_minutes, 0, 0, tzinfo=timezone.utc
                ),
                "done_charging_time": datetime(
                    done_year,
                    done_month,
                    done_day,
                    done_hour,
                    done_minutes,
                    0,
                    0,
                    tzinfo=timezone.utc,
                ),
                "charging_point": row[6],
                "vehicle": row[7],
            }
            serializer = SessionSerializer(data=session)
            if serializer.is_valid():
                imported_count += 1
                serializer.create(serializer.validated_data)

        response = {
            "SessionsInUploadedFile": sessions_count,
            "SessionsImported": imported_count,
            "TotalSessionsInDatabase": self.queryset.count(),
        }
        if form == "csv":
            renderer = r.CSVRenderer()
            return Response(renderer.render(data=response))
        else:
            return Response(response)
