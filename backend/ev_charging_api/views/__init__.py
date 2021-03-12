from .views import (  # CSRFGeneratorView,; CustomAuthToken,; ExampleView,
    HealthcheckView,
    InsertStationView,
    LogoutView,
    ResetSessionsView,
    RetrieveUserViewSet,
    SessionsPerPointView,
    SessionsPerProviderView,
    SessionsPerStationView,
    SessionsPerVehicleView,
    SessionsupdView,
    StationsView,
    UsermodAPIView,
)

"""
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'ev_charging_api/api.html')
"""
