import csv
import io
import uuid
from datetime import datetime

from django.db import connections
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, mixins, status, viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import (
    ChargingPoint,
    ChargingStation,
    Cluster,
    Location,
    Owner,
    Provider,
    Session,
    User,
    Vehicle,
)
from ev_charging_api.authentication import CustomTokenAuthentication

from ..serializers import (
    AdminUserSerializer,
    CreateUserSerializer,
    FileUploadSerializer,
    KWSerializer,
    LocationSerializer,
    SessionSerializer,
    StationSerializer,
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
            return Response(response)

        except:
            data = {"username": username, "password": password}
            serializer = CreateUserSerializer(data=data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Logged out succesfully",
            "data": [],
        }
        return Response(response)


class RetrieveUserViewSet(viewsets.ViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    lookup_field = "username"
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, username=None):
        user = get_object_or_404(self.queryset, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def list(self, request):
        serializer = UserSerializer(self.queryset, many=True)
        return Response(serializer.data)


class SessionsPerPointView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id, date_from, date_to):
        charging_point = get_object_or_404(ChargingPoint, pk=id)
        sessions = self.queryset.filter(charging_point__id=id).filter(
            connect_time__date__range=[date_from, date_to]
        )
        sessions_list = [
            {
                "SessionIndex": session_index,
                "SessionID": s.id,
                "StartedOn": s.connect_time,
                "FinishedOn": s.done_charging_time,
                "Protocol": s.protocol,
                "EnergyDelivered": s.kwh_delivered,
                "Payment": s.payment.payment_method,
                "VehicleType": s.vehicle.model.engine_type,
            }
            for session_index, s in enumerate(sessions, start=1)
        ]

        response = {
            "Point": id,
            "PointOperator": charging_point.charging_station.owner.id,
            "RequestTimestamp": datetime.now(),
            "PeriodFrom": date_from,
            "PeriodTo": date_to,
            "NumberOfChargingSessions": len(sessions),
            "ChargingSessionsList": sessions_list,
        }
        return Response(response)


class SessionsPerStationView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id, date_from, date_to):
        charging_station = get_object_or_404(ChargingStation, pk=id)
        sessions = self.queryset.filter(charging_point__charging_station_id=id).filter(
            connect_time__date__range=[date_from, date_to]
        )

        sessions_list = []
        for s in sessions:
            for d in sessions_list:
                if s.charging_point.id == d["PointID"]:
                    d["PointSessions"] += 1
                    d["EnergyDelivered"] += s.kwh_delivered
                    break
            else:
                sessions_list.append(
                    {
                        "PointID": s.charging_point.id,
                        "PointSessions": 1,
                        "EnergyDelivered": s.kwh_delivered,
                    }
                )
        response = {
            "StationID": id,
            "Operator": charging_station.owner.id,
            "RequestTimestamp": datetime.now(),
            "PeriodFrom": date_from,
            "PeriodTo": date_to,
            "TotalEnergyDelivered": sessions.aggregate(Sum("kwh_delivered"))[
                "kwh_delivered__sum"
            ],
            "NumberOfChargingSessions": sessions.count(),
            "NumberOfActivePoints": len(sessions_list),
            "SessionsSummaryList": sessions_list,
            # sessions need more fields!!!
        }
        return Response(response)


class SessionsPerVehicleView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id, date_from, date_to):
        vehicle = get_object_or_404(Vehicle, pk=id)
        sessions = self.queryset.filter(vehicle__id=id).filter(
            connect_time__date__range=[date_from, date_to]
        )
        sessions_list = [
            {
                "SessionIndex": session_index,
                "SessionID": s.id,
                "EnergyProvider": s.provider.id,
                "StartedOn": s.connect_time,
                "FinishedOn": s.done_charging_time,
                "Protocol": s.protocol,
                "EnergyDelivered": s.kwh_delivered,
                "PricePolicyRef": s.payment.invoice,
                "CostPerKWh": (
                    s.payment.cost / s.kwh_delivered if s.kwh_delivered > 0 else 0.0
                ),
                "SessionCost": s.payment.cost,
            }
            for session_index, s in enumerate(sessions, start=1)
        ]
        response = {
            "VehicleID": id,
            "RequestTimestamp": datetime.now(),
            "PeriodFrom": date_from,
            "PeriodTo": date_to,
            "TotalEnergyDelivered": sessions.aggregate(Sum("kwh_delivered"))[
                "kwh_delivered__sum"
            ],
            "NumberOfVisitedPoints": (
                sessions.order_by().values("charging_point").distinct().count()
            ),
            "NumberOfVehicleChargingSessions": sessions.count(),
            "VehicleChargingSessionsList": sessions_list,
        }
        return Response(response)


class SessionsPerProviderView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SessionSerializer
    queryset = Session.objects.all()

    def get(self, request, id, date_from, date_to):
        provider = get_object_or_404(Provider, pk=id)
        sessions = self.queryset.filter(provider__id=id).filter(
            connect_time__date__range=[date_from, date_to]
        )
        sessions_list = [
            {
                "StationID": s.charging_point.charging_station.id,
                "SessionID": s.id,
                "VehicleID": s.vehicle.id,
                "StartedOn": s.connect_time,
                "FinishedOn": s.done_charging_time,
                "Protocol": s.protocol,
                "EnergyDelivered": s.kwh_delivered,
                "PricePolicyRef": s.payment.invoice,
                "CostPerKWh": (
                    (s.payment.cost / s.kwh_delivered) if s.kwh_delivered > 0 else 0.0
                ),
                "SessionCost": s.payment.cost,
            }
            for session_index, s in enumerate(sessions, start=1)
        ]
        response = {
            "ProviderID": id,
            "ProviderName": provider.provider_name,
            "SessionsList": sessions_list,
        }
        return Response(response)


class HealthcheckView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        db_conn = connections["default"]
        try:
            c = db_conn.cursor()
            response = {"status": "OK"}
        except:
            response = {"status": "failed"}
        return Response(response)


class ResetSessionsView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = [SessionSerializer]
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
            serializer = AdminUserSerializer(data=admin_user)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)

        except:
            response = {"status": "failed"}
        return Response(response)


class SessionsupdView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = FileUploadSerializer
    queryset = Session.objects.all()

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")
        if file is None:
            return Response("no file provided", status=status.HTTP_400_BAD_REQUEST)
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
                "payment": row[8],
            }
            serializer = SessionSerializer(data=session)
            if serializer.is_valid():
                imported_count += 1
                serializer.create(serializer.validated_data)
            else:
                return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

        response = {
            "SessionsInUploadedFile": sessions_count,
            "SessionsImported": imported_count,
            "TotalSessionsInDatabase": self.queryset.count(),
        }
        return Response(response)


class KWstatsView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    # notAdminUser
    serializer_class = KWSerializer
    queryset = Session.objects.all()

    def get(self, request):
        print("Helloo")
        KW = []
        index = 0
        print(self.queryset.all())
        for s in self.queryset.all():
            KW.append(
                {
                    "SessionIndex": index,
                    # "SessionID": s.id,
                    "EnergyDelivered": s.kwh_delivered,
                }
            )
            index += 1
        response = {
            "SessionKW": KW,
        }
        return Response(response)


class StationsViewSet(viewsets.ViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = StationSerializer
    queryset = ChargingStation.objects.all()
    # lookup_field = "pk"

    def list(self, request):
        # id = str(list(request.POST.items())[0][0].split(":")[1][1:-2])
        # print(id)
        try:
            # stations = self.queryset.get(id=id)
            # stations = self.get_queryset()
            # print(stations)
            serializer = StationSerializer(ChargingStation.objects.all(), many=True)
            print(serializer.data)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        # id = str(list(request.POST.items())[0][0].split(":")[1][1:-2])
        print(request.POST)
        l = list(request.POST.items())[0][0][1:-1].split(",")
        print(l)
        d = {}
        for x in l:
            if len(x.split(":")[1:]) > 1:
                y = ""
                count = 1
                for k in x.split(":")[1:]:
                    if count == len(x.split(":")[1:]):
                        y += ":" + k[:-1]
                    elif count > 1:
                        y += ":" + k
                    else:
                        y = k[1:]
                    count += 1
                d[x.split(":")[0][1:-1]] = y
            else:
                d[x.split(":")[0][1:-1]] = x.split(":")[1][1:-1]

        print(d)
        location = {
            "email": d["email"],
            "website": d["website"],
            "title": d["title"],
            "town": d["town"],
            "area": d["area"],
            "country": d["country"],
            "address_line": d["address_line"],
        }
        d2 = {}
        for i, j in d.items():
            if (
                i != "email"
                and i != "website"
                and i != "town"
                and i != "title"
                and i != "area"
                and i != "country"
                and i != "address_line"
            ):
                d2[i] = j
        try:
            print(d)
            location_serializer = LocationSerializer(data=location)
            print("This is serializer", location_serializer)
            if location_serializer.is_valid(raise_exception=True):
                location_serializer.save()
            else:
                return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)
            d2["owner"] = Owner.objects.all().get(user__username=d["owner"]).id
            print("hello")
            d2["provider"] = Provider.objects.all().get(provider_name=d["provider"]).id
            d2["cluster"] = Cluster.objects.all().get(cluster_name=d2["cluster"]).id
            print("hi")
            d2["location"] = location_serializer.data["id"]
            print(d2)
            serializer = self.serializer_class(data=d2)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            print("POST", request.POST)
            # id = str(list(request.POST.items())[0][0].split(":")[1][1:-2])
            l = list(request.POST.items())[0][0][1:-1].split(",")
            id = l[0].split(":")[1][1:-1]
            print("ID", id)
            print("HERE WE ARE")
            d = {}
            for x in l:
                if len(x.split(":")[1:]) > 1:
                    y = ""
                    count = 1
                    for k in x.split(":")[1:]:
                        if count == len(x.split(":")[1:]):
                            y += ":" + k[:-1]
                        elif count > 1:
                            y += ":" + k
                        else:
                            y = k[1:]
                        count += 1
                    if y != "":
                        d[x.split(":")[0][1:-1]] = y
                else:
                    if x.split(":")[1][1:-1] != "":
                        d[x.split(":")[0][1:-1]] = x.split(":")[1][1:-1]
            print("are you here?")
            print(d)
            if "owner" in d.keys():
                d["owner"] = Owner.objects.all().get(user__username=d["owner"])
            if "cluster" in d.keys():
                d["cluster"] = Cluster.objects.all().get(cluster_name=d["cluster"])
            if "provider" in d.keys():
                d["provider"] = Provider.objects.all().get(provider_name=d["provider"])
            if "title" in d.keys():
                d["location"] = Location.objects.all().get(title=d["title"])
                d.pop("title")
            print("Are we ok?", d)
            ChargingStation.objects.update_or_create(d)
            return Response({"status": "ok"}, status.HTTP_200_OK)

        except:
            return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

        """location = {
            "email": d["email"],
            "website": d["website"],
            "title": d["title"],
            "town": d["town"],
            "area": d["area"],
            "country": d["country"],
            "address_line": d["address_line"],
        }
        d2 = {}
        for i, j in d.items():
            if (
                i != "email"
                and i != "website"
                and i != "town"
                and i != "title"
                and i != "area"
                and i != "country"
                and i != "address_line"
            ):
                if j!='':
                    d2[i] = j
        try:
            print("DATA", request.data)
            # print(d)
            location_serializer = LocationSerializer(data=location)
            print("This is serializer", location_serializer)
            if location_serializer.is_valid(raise_exception=True):
                location_serializer.update()
            else:
                return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)
            d2["owner"] = Owner.objects.all().get(user__username=d["owner"]).id
            print("hello")
            d2["provider"] = Provider.objects.all().get(provider_name=d["provider"]).id
            d2["cluster"] = Cluster.objects.all().get(cluster_name=d2["cluster"]).id
            print("hi")
            d2["location"] = location_serializer.data["id"]
            print(d2)
            serializer = self.serializer_class(data=d2)
            if serializer.is_valid():
                serializer.update()
                return Response(serializer.data, status.HTTP_200_OK)
            return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)

        except:
            return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)"""

    def delete(self, request):
        try:
            print(request.data)
            # id = str(list(request.POST.items())[0][0].split(":")[1][1:-2])
            self.queryset.get(id=request.data["id"]).delete()
            return Response({"status": "OK"}, status.HTTP_200_OK)

        except:
            return Response({"status": "failed"}, status.HTTP_400_BAD_REQUEST)


"""class CreateStationView(generics.GenericAPIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = [SessionSerializer]
    queryset = Session.objects.all()
        lookup_fields = [
        "owner",
        "cluster",
        "provider"
    ]
    def post(self, request, *args, **kwargs):
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
            return Response(response)

        except:
            data = {"username": username, "password": password}
            serializer = CreateUserSerializer(data=data)
            if serializer.is_valid():
                serializer.create(serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""
