#from cities_light.models import City
from django import forms
from django.contrib import admin
from .models import User
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

USER_TYPE_CHOICES = [
        (1, "Regular User"),
        (2, "Station Owner"),
        (3, "Energy Provider"),
    ]

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices = USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['user_type', 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']