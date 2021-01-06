from django.contrib import admin

# Register your models here.
from .models import Vehicle,VehicleModel

admin.site.register(Vehicle)  
admin.site.register(VehicleModel)
