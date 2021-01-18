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
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from common import views as common_views
from ev_charging_api import views as api_views
from rest_framework.authtoken import views
from django.utils import timezone
import datetime

router = DefaultRouter()
router.register('users', api_views.RetrieveUserViewSet,)
#router2 = DefaultRouter()
#router2.register('SessionsPerPoint', api_views.TestViewSet,)

urlpatterns = [
    #path('api/', api_views.home, name='api_home'),
    #path('api/login/', api_views.UserLogin.as_view(), name='rest_login'),
    #path('api/logout/', api_views.Logout.as_view(), name='rest_logout'),
    #path('api-auth/', include('rest_framework.urls')),
    #path('api/usermod/<int:pk>/', api_views.UsermodAPIView.as_view()),
    #path('api/', include(router2.urls)),
    path('SessionsPerPoint/<int:id>/<str:date_from>/<str:date_to>/', api_views.SessionsPerPointView.as_view(), name='sessions_per_point'),
    path('SessionsPerStation/<int:id>/<str:date_from>/<str:date_to>/', api_views.SessionsPerStationView.as_view(), name='sessions_per_station'),
    path('SessionsPerVehicle/<str:id>/<str:date_from>/<str:date_to>/', api_views.SessionsPerVehicleView.as_view(), name='sessions_per_vehicle'),
    path('SessionsPerProvider/<int:id>/<str:date_from>/<str:date_to>/', api_views.SessionsPerProviderView.as_view(), name='sessions_per_provider'),
    path('admin/', admin.site.urls),
    path("example/", api_views.ExampleView.as_view(), name="example"),
    path('generate_csrf/', api_views.CSRFGeneratorView.as_view()),
    path('rest_login/', views.obtain_auth_token, name='rest_login'),
    path("rest_logout/", api_views.LogoutView.as_view(), name="rest_logout"),
    path('api/', include(router.urls)),
    path('api/usermod/<str:username>/<str:password>/', api_views.UsermodAPIView.as_view()),
    path('home/', common_views.home, name='home'),
    path('register/', common_views.register, name='register'),
	path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='common/logout.html'), name='logout'),
    path('profile/', common_views.profile, name='profile'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
