from django.db import models
from multiselectfield import MultiselectField
# Create your models here.



class VehicleModel(models.Model):
	class Engine(models.TextChoices):
		BATTERY_ELECTRIC_VEHICLE="bev"
		PLUGIN_HYBRID_ELECTRIC_VEHICLE="phev"
		HYBRID_ELECTRIC_VEHICLE="hev"

	class DcCharger(models.TextChoices):
		COMBINED_CHARGING_SYSTEM="ccs"
		CHADEMO="chademo"
		TESLA_COMBINED_CHARGING_SYSTEM="tesla_ccs"
		TESLA_SUPERCHARGER="tesla_suc"

	class AcCharger(models.TextChoices):
		TYPE1="type1"
		TYPE2="type2"

	engine_type=models.CharField(max_length=8, choices=Engine)
	release_year=models.PositiveSmallIntegerField(null=True)
	brand=models.CharField(max_length=32)
	variant=models.CharField(max_length=32,blank=True)
	# category? car,...

	ac_ports=MultiselectField(choices=AcCharger)
	ac_usable_phaces=models.PositiveIntegerField()
	ac_max_power=models.FloatField()
	ac_charging_power=models.JSONField()

	dc_ports=MultiselectField(choices=DcCharger)
	dc_max_power=models.FloatField(null=True)
	dc_charging_curve=models.JSONField(null=True)
	is_default_curve=models.BooleanField(null=True)


	usable_battery_size=models.FloatField()
	average_energy_consumption=models.FloatField()















