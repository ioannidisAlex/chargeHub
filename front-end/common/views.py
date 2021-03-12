from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework import status

from .forms import (
    DeleteStationForm,
    InsertStationForm,
    ProfileUpdateForm,
    RestLoginForm,
    SessionsPer_Form,
    SessionsupdForm,
    StationsForm,
    UsermodForm,
    UserRegisterForm,
    UsersForm,
    UserUpdateForm,
)


def home(request):
    return render(request, "common/home.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Your account has been created! You are now able to log in"
            )
            return redirect("/login")
    else:
        form = UserRegisterForm()
    return render(request, "common/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect("profile")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "common/profile.html", context)


class UsermodView(View):
    template_name = "common/usermod.html"
    form_class = UsermodForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        context = {
            "username": str(request.POST["username"]),
            "password": str(request.POST["password"]),
        }
        return render(request, "common/usermod_data.html", context)


class RestLoginView(View):
    template_name = "common/rest_login.html"
    form_class = RestLoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        context = {
            "username": request.POST["username"],
            "password": request.POST["password"],
        }
        return render(request, "common/get_login_data.html", context)


class RestLogoutView(View):
    template_name = "common/rest_logout.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        return render(request, "common/rest_logout_data.html")


class HealthcheckView(View):
    template_name = "common/healthcheck.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        return render(request, "common/healthcheck_data.html")


class SessionsupdView(View):
    template_name = "common/sessionsupd.html"
    form_class = SessionsupdForm

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class,
            },
        )

    def post(self, request):
        pass
        # return render(request, 'common/sessionsupd_data.html', context)


class ResetSessionsView(View):
    template_name = "common/resetsessions.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        return render(request, "common/resetsessions_data.html")


class SessionsPerPointView(View):
    template_name = "common/sessions_per_point.html"
    form_class = SessionsPer_Form

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"form": self.form_class},
        )

    def post(self, request):
        context = {
            "id": request.POST["ID"],
            "date_from": request.POST["date_from"],
            "date_to": request.POST["date_to"],
        }
        return render(request, "common/sessions_per_provider_data.html", context)


class SessionsPerStationView(View):
    template_name = "common/sessions_per_station.html"
    form_class = SessionsPer_Form

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"form": self.form_class},
        )

    def post(self, request):
        context = {
            "id": request.POST["ID"],
            "date_from": request.POST["date_from"],
            "date_to": request.POST["date_to"],
        }
        return render(request, "common/sessions_per_provider_data.html", context)


class SessionsPerEVView(View):
    template_name = "common/sessions_per_ev.html"
    form_class = SessionsPer_Form

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"form": self.form_class},
        )

    def post(self, request):
        context = {
            "id": request.POST["ID"],
            "date_from": request.POST["date_from"],
            "date_to": request.POST["date_to"],
        }
        return render(request, "common/sessions_per_provider_data.html", context)


class SessionsPerProviderView(View):
    template_name = "common/sessions_per_provider.html"
    form_class = SessionsPer_Form

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"form": self.form_class},
        )

    def post(self, request):
        context = {
            "id": request.POST["ID"],
            "date_from": request.POST["date_from"],
            "date_to": request.POST["date_to"],
        }
        return render(request, "common/sessions_per_provider_data.html", context)


class UsersView(View):
    template_name = "common/users.html"
    form_class = UsersForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        context = {
            "username": request.POST["username"],
        }
        return render(request, "common/get_users.html", context)


class StationsView(View):
    template_name = "common/stations.html"
    form_class = StationsForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
        # {"form": self.form_class()}

    def post(self, request):
        # print("HELLOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO", request.POST["ID"])
        # context = {
        #    "id": request.POST["ID"],
        # }
        return render(request, "common/stations_data.html")
        # , context


class InsertStationView(View):
    template_name = "common/insert_stations.html"
    form_class = InsertStationForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):

        context = {
            "owner": request.POST["owner"],
            "cluster": request.POST["cluster"],
            "provider": request.POST["provider"],
            "email": request.POST["email"],
            "website": request.POST["website"],
            "title": request.POST["title"],
            "town": request.POST["town"],
            "area": request.POST["area"],
            "country": request.POST["country"],
            "address": request.POST["address"],
        }
        return render(request, "common/insert_station_data.html", context)


class DeleteStationView(View):
    template_name = "common/delete_stations.html"
    form_class = DeleteStationForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):

        context = {
            "id": request.POST["ID"],
        }
        return render(request, "common/delete_stations_data.html", context)


class ChargeView(View):
    template_name = "common/charge.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,)

    def post(self, request):
        pass