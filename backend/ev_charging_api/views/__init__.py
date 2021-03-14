from .views import (  # CSRFGeneratorView,; CustomAuthToken,; ExampleView,; InsertStationView,
    ChargingCostView,
    CostEstimationView,
    HealthcheckView,
    InsertPaymentView,
    InsertSessionView,
    InvoiceForVehicleView,
    KWstatsView,
    LogoutView,
    ResetSessionsView,
    RetrieveUserViewSet,
    SessionsPerPointView,
    SessionsPerProviderView,
    SessionsPerStationView,
    SessionsPerVehicleView,
    SessionsupdView,
    StationsViewSet,
    UsermodAPIView,
)

"""
from django.shortcuts import render, redirect

def home(request):
    return render(request, 'ev_charging_api/api.html')
"""
