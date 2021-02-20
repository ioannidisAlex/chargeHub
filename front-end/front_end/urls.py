"""front_end URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import include, path, re_path
from django.utils import timezone

from common import views as common_views

urlpatterns = [
    path("admin/", admin.site.urls),
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
        "rest_login/",
        login_required(common_views.RestLoginView.as_view()),
        name="rest_login",
    ),
    path(
        "rest_logout/",
        login_required(common_views.RestLogoutView.as_view()),
        name="rest_logout",
    ),
    path(
        "usermod/",
        login_required(common_views.UsermodView.as_view()),
        name="usermod",
    ),
    path(
        "users/",
        login_required(common_views.UsersView.as_view()),
        name="users",
    ),
    path(
        "healthcheck/",
        login_required(common_views.HealthcheckView.as_view()),
        name="healthcheck",
    ),
    path(
        "resetsessions/",
        login_required(common_views.ResetSessionsView.as_view()),
        name="resetsessions",
    ),
    path(
        "sessionsupd/",
        login_required(common_views.SessionsupdView.as_view()),
        name="sessionsupd",
    ),
    path(
        "sessiosn_per_point/",
        login_required(common_views.SessionsPerPointView.as_view()),
        name="sessions_per_point",
    ),
    path(
        "sessions_per_station/",
        login_required(common_views.SessionsPerStationView.as_view()),
        name="sessions_per_station",
    ),
    path(
        "sessions_per_ev/",
        login_required(common_views.SessionsPerEVView.as_view()),
        name="sessions_per_ev",
    ),
    path(
        "sessions_per_provider/",
        login_required(common_views.SessionsPerProviderView.as_view()),
        name="sessions_per_provider",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)