import uuid
from django.conf import settings
from django.db import models
from multiselectfield import MultiSelectField








class VehicleModel(models.Model):
    class Engine(models.TextChoices):
        BATTERY_ELECTRIC_VEHICLE = "bev"
        PLUGIN_HYBRID_ELECTRIC_VEHICLE = "phev"
        HYBRID_ELECTRIC_VEHICLE = "hev"

    class DcCharger(models.TextChoices):
        COMBINED_CHARGING_SYSTEM = "ccs"
        CHADEMO = "chademo"
        TESLA_COMBINED_CHARGING_SYSTEM = "tesla_ccs"
        TESLA_SUPERCHARGER = "tesla_suc"

    class AcCharger(models.TextChoices):
        TYPE1 = "type1"
        TYPE2 = "type2"

    engine_type = models.CharField(max_length=8, choices=Engine)
    release_year = models.PositiveSmallIntegerField(null=True)
    brand = models.CharField(max_length=32)
    variant = models.CharField(max_length=32, blank=True)
    model = models.CharField(64)
    # category? car,...

    ac_ports = MultiSelectField(choices=AcCharger)
    ac_usable_phaces = models.PositiveIntegerField()
    ac_max_power = models.FloatField()
    ac_charging_power = models.JSONField()

    dc_ports = MultiSelectField(choices=DcCharger)
    dc_max_power = models.FloatField(null=True)
    dc_charging_curve = models.JSONField(null=True)
    is_default_curve = models.BooleanField(null=True)

    usable_battery_size = models.FloatField()
    average_energy_consumption = models.FloatField()


class Profile(models.Model):
    class Role(models.TextChoices):
        VEHICLE_OWNER="vo"
        STATION_OWNER="seo"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role=models.CharField(max_length=4,choices=Role,default="vo")

    @property
    def is_vehicle_owner(self):
        return self.role == Profile.Role.VEHICLE_OWNER

    @property
    def is_station_owner(self):
        return self.role == Profile.Role.STATION_OWNER

    

class Vehicle(models.Model):
    model=models.ForeignKey(VehicleModel,on_delete= models.CASCADE,
        related_name="vehicles"
    )
    owner= models.ForeignKey(Profile,on_delete=models.SET_NULL,
        related_name="vehicles"
    )
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
