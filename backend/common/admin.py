from django.contrib import admin
from .models import Location, Cluster, ChargingPoint, Provider , ChargingStation, Profile, Owner
#from .forms import LocationAdminForm

admin.site.register(Location)
admin.site.register(ChargingPoint)
admin.site.register(Provider)
admin.site.register(ChargingStation)
admin.site.register(Cluster)
admin.site.register(Profile)
admin.site.register(Owner)

#class LocationAdmin(admin.ModelAdmin):
#    form = LocationAdminForm