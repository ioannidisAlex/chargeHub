#from cities_light.models import City
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
#from common.models import Location

#class LocationAdminForm(forms.ModelForm):
#	def __init__(self, *args, **kwargs):
#		super(LocationAdminForm, self).__init__(*args, **kwargs)
#		if self.instance:
#			country = self.instance.country
#			cities = City.objects.all().filter(country__name = country)
#			self.fields["town"] = ChoiceField(choices = cities)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']