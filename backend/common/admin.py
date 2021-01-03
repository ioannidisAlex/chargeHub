from django.contrib import admin
from .models import Location, Cluster, ChargingPoint, Provider , ChargingStation

admin.site.register(Location)
admin.site.register(ChargingPoint)
admin.site.register(Provider)
admin.site.register(ChargingStation)
admin.site.register(Cluster)