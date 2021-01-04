#from cities_light.models import City
from django import forms
from django.contrib import admin
#from common.models import Location

#class LocationAdminForm(forms.ModelForm):
#	def __init__(self, *args, **kwargs):
#		super(LocationAdminForm, self).__init__(*args, **kwargs)
#		if self.instance:
#			country = self.instance.country
#			cities = City.objects.all().filter(country__name = country)
#			self.fields["town"] = ChoiceField(choices = cities)