"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import datetime

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path, register_converter
from django.utils import timezone
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from common import views as common_views
from ev_charging_api import views as api_views

router = DefaultRouter()
router2 = DefaultRouter()
router_KWatts = DefaultRouter()
router.register(
    "users",
    api_views.RetrieveUserViewSet,
)
router2.register(
    "stations",
    api_views.StationsViewSet,
)


# pylint: disable=R0201
class YyyyMmDdConverter:
    regex = "[0-9]{7,8}"

    def to_python(self, value):
        return datetime.datetime.strptime(value, "%Y%m%d").date()

    def to_url(self, value):
        return value.strftime("%Y%m%d")


register_converter(YyyyMmDdConverter, "yyyymmdd")

urlpatterns = [
    path(
        "evcharge/api/admin/resetsessions/",
        api_views.ResetSessionsView.as_view(),
        name="resetsessions",
    ),
    path(
        "evcharge/api/admin/healthcheck/",
        api_views.HealthcheckView.as_view(),
        name="healthcheck",
    ),
    path(
        "evcharge/api/KWstats/",
        api_views.KWstatsView.as_view(),
        name="KWstats",
    ),
    path(
        "evcharge/api/SessionsPerPoint/<uuid:id>/<yyyymmdd:date_from>/<yyyymmdd:date_to>/",
        api_views.SessionsPerPointView.as_view(),
        name="sessions_per_point",
    ),
    path(
        "evcharge/api/SessionsPerStation/<uuid:id>/<yyyymmdd:date_from>/<yyyymmdd:date_to>/",
        api_views.SessionsPerStationView.as_view(),
        name="sessions_per_station",
    ),
    path(
        "evcharge/api/SessionsPerVehicle/<uuid:id>/<yyyymmdd:date_from>/<yyyymmdd:date_to>/",
        api_views.SessionsPerVehicleView.as_view(),
        name="sessions_per_vehicle",
    ),
    path(
        "evcharge/api/SessionsPerProvider/<uuid:id>/<yyyymmdd:date_from>/<yyyymmdd:date_to>/",
        api_views.SessionsPerProviderView.as_view(),
        name="sessions_per_provider",
    ),
    path("admin/", admin.site.urls),
    path(
        "evcharge/api/admin/system/sessionsupd/",
        api_views.SessionsupdView.as_view(),
        name="sessionsupd",
    ),
    path("evcharge/api/login/", views.obtain_auth_token, name="rest_login"),
    path("evcharge/api/logout/", api_views.LogoutView.as_view(), name="rest_logout"),
    path("evcharge/api/admin/", include(router.urls)),
    path("evcharge/api/", include(router2.urls)),
    path(
        "evcharge/api/admin/usermod/<str:username>/<str:password>/",
        api_views.UsermodAPIView.as_view(),
        name="usermod",
    ),
    path("home/", common_views.home, name="home"),
    path("register/", common_views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="common/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="common/logout.html"),
        name="logout",
    ),
    path("profile/", common_views.profile, name="profile"),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="common/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="common/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="common/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="common/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "evcharge/api/charging_cost/<uuid:id>/",
        api_views.ChargingCostView.as_view(),
        name="charging_cost",
    ),
    path(
        "evcharge/api/insert_payment/",
        api_views.InsertPaymentView.as_view(),
        name="insert_payment",
    ),
    path(
        "evcharge/api/insert_session/",
        api_views.InsertSessionView.as_view(),
        name="insert_session",
    ),
    path(
        "evcharge/api/cost_estimation/<uuid:id>/<yyyymmdd:date_from>/<yyyymmdd:date_to>/",
        api_views.CostEstimationView.as_view(),
        name="cost_estimation",
    ),
    path(
        "evcharge/api/InvoiceForVehicle/<uuid:id>/<yyyymmdd:date_from>/<yyyymmdd:date_to>/",
        api_views.InvoiceForVehicleView.as_view(),
        name="invoice_for_vehicle",
    ),
    # path("generate_csrf/", api_views.CSRFGeneratorView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
