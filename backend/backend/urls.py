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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from common import views as common_views

urlpatterns = [
    path('home/', common_views.home, name='home'),
    path('register/', common_views.register, name='register'),
	path('register/provider/', common_views.register_provider, name='register_provider'),
    path('register/owner/', common_views.register_owner, name='register_owner'),
    path('register/user/', common_views.register_user, name='register_user'),
    path('admin/', admin.site.urls),
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
