# from cities_light.models import City
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, User

# from common.models import Location

# class LocationAdminForm(forms.ModelForm):
# 	def __init__(self, *args, **kwargs):
# 		super(LocationAdminForm, self).__init__(*args, **kwargs)
# 		if self.instance:
# 			country = self.instance.country
# 			cities = City.objects.all().filter(country__name = country)
# 			self.fields["town"] = ChoiceField(choices = cities)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ["user_type", "username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]


class UsermodForm(forms.Form):
        token = forms.CharField(max_length=100)
        username = forms.CharField(max_length=20, required=True)
        password = forms.CharField(widget=forms.PasswordInput)
        
        class Meta:
            widgets = {
                'password': forms.PasswordInput(),
            }
            fields = ["token", "username", "password", ]

class UsersForm(forms.Form):
        token = forms.CharField(max_length=100)
        username = forms.CharField(max_length=20, required=True)
        
        class Meta:
            fields = ["token", "username",]

class SessionsupdForm(forms.Form):
        token = forms.CharField(max_length=100)
        file = forms.FileField()
        
        class Meta:
            fields = ["token", "file",]

class TokenForm(forms.Form):
        token = forms.CharField(max_length=100)
        
        class Meta:
            fields = ["token", "username", "password", ]

class RestLoginForm(forms.Form):
        username = forms.CharField(max_length=100)
        password = forms.CharField(widget=forms.PasswordInput)
        
        class Meta:
            widgets = {
                'password': forms.PasswordInput(),
            }
            fields = ["username", "password",]