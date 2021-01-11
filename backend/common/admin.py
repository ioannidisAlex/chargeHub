from django.contrib import admin
from .models import Location, Cluster, ChargingPoint, Provider , ChargingStation, Profile, Owner, User, Vehicle, VehicleModel, VehicleOwner, Session, Payment

admin.site.register(Payment)
admin.site.register(Session)
admin.site.register(VehicleOwner)
admin.site.register(Vehicle)  
admin.site.register(VehicleModel)
admin.site.register(Location)
admin.site.register(ChargingPoint)
admin.site.register(Provider)
admin.site.register(ChargingStation)
admin.site.register(Cluster)
admin.site.register(Profile)
admin.site.register(Owner)
admin.site.register(User)