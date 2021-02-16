from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from .forms import (
    ProfileUpdateForm,
    RestLoginForm,
    SessionsupdForm,
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
        messages.success(request, f"ola popa")
        return redirect("home")


class RestLoginView(View):
    template_name = "common/rest_login.html"
    form_class = RestLoginForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        return render(request, "common/home.html")


class RestLogoutView(View):
    template_name = "common/rest_logout.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        pass


class HealthcheckView(View):
    template_name = "common/healthcheck.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        pass


class SessionsupdView(View):
    template_name = "common/sessionsupd.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        pass


class ResetSessionsView(View):
    template_name = "common/resetsessions.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        pass


class SessionsPerPointView(View):
    template_name = "common/sessions_per_point.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        pass


class SessionsPerStationView(View):
    template_name = "common/sessions_per_station.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        pass


class SessionsPerEVView(View):
    template_name = "common/sessions_per_ev.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        pass


class SessionsPerProviderView(View):
    template_name = "common/sessions_per_provider.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
        )

    def post(self, request):
        pass


class UsersView(View):
    template_name = "common/users.html"
    form_class = UsersForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request):
        pass
