from django.db import models
from phone_field import PhoneField
from localflavor.gr.forms import GRPostalCodeField
from PIL import Image
#uncomment when ready
#from ... import Owner


class Location(models.Model):
	#location_id = models.AutoField(primary_key = True)
	#ChargingPoint = models.ForeignKey(ChargingPoint, on_delete = models.CASCADE)
	email = models.EmailField()
	website = models.URLField()
	telephone = models.PhoneField()
	title = models.CharField(max_length = 15)
	town = models.CharField(max_length = 15)
	country = models.CharField(max_length = 15)
	post_code = GRPostalCodeField()
	address_line = models.CharField(max_length = 100)

	def __str__(self):
		return f'Title = {self.title}'

class Cluster(models.Model):
	#cluster_id = models.AutoField(primary_key = True)
	cluster_name = models.CharField(max_length = 15)
	
	def __str__(self):
		return f'Cluster name = {self.cluster_name}'

class Provider(models.Model):
	#provider_id = models.AutoField(primary_key = True)
	provider_name = models.CharField(max_length = 15)

	def __str__(self):
		return f'Provider name = {self.provider_name}'

class ChargingStation(models.Model):
	######################
	nr_charging_categories = models.IntegerField()
	######################
	#charging_station_id = models.AutoField(primary_key = True)
	cluster = models.ForeignKey(Cluster, on_delete = models.CASCADE)
	provider = models.ForeignKey(Provider , on_delete = models.CASCADE)
    
	def __str__(self):
		return f'Id = {self.id}'


class ChargingPoint(models.Model):
	CONNECTION_TYPE_CHOICES = [
		(7,	'Avcon Connector'),
		(4,	'Blue Commando (2P+E)'),
		(3,	'BS1363 3 Pin 13 Amp'),
		(32,	'CCS (Type 1)'),
		(33,'CCS (Type 2)'),
		(16,	'CEE 3 Pin'),
		(17,	'CEE 5 Pin'),
		(28,	'CEE 7/4 - Schuko - Type F'),
		(23,	'CEE 7/5'),
		(18,	'CEE+ 7 Pin'),
		(2,	'CHAdeMO'),
		(13,	'Europlug 2-Pin (CEE 7/16)'),
		(1038,	'GB-T AC - GB/T 20234.2 (Socket)'),
		(1039,	'GB-T AC - GB/T 20234.2 (Tethered Cable)'),
		(1040,	'GB-T DC - GB/T 20234.3'),
		(34,	'IEC 60309 3-pin'),
		(35,	'IEC 60309 5-pin'),
		(5,	'LP Inductive'),
		(10,	'NEMA 14-30'),
		(11, 'NEMA 14-50'),
		(22,	'NEMA 5-15R'),
		(9,	'NEMA 5-20R'),
		(15,	'NEMA 6-15'),
		(14,	'NEMA 6-20'),
		(1042,	'NEMA TT-30R'),
		(36,	'SCAME Type 3A (Low Power)'),
		(26,	'SCAME Type 3C (Schneider-Legrand)'),
		(6,	'SP Inductive'),
		(1037,	'T13 - SEC1011 ( Swiss domestic 3-pin ) - Type J'),
		(30,	'Tesla (Model S/X)'),
		(8,	'Tesla (Roadster)'),
		(31,	'Tesla Battery Swap'),
		(27,	'Tesla Supercharger'),
		(1041,	'Three Phase 5-Pin (AS/NZ 3123)'),
		(1,	'Type 1 (J1772)'),
		(25,	'Type 2 (Socket Only)'),
		(1036,	'Type 2 (Tethered Connector)'),
		(29,	'Type I (AS 3112)'),
		(0,	'Unknown'),
		(24,	'Wireless Charging'),
		(21,	'XLR Plug (4 pin)'),
	]

	CURRENT_TYPE_CHOICES = [
		(1, 'AC - Single Phase'),
		(2, 'AC - Three Phase'),
		(3, 'DC'),
	]

	STATUS_TYPE_CHOICES = [
		(0, 'Unknown'),
		(10, 'Currently Available (Automated Status)'),
		(20, 'Currently In Use (Automated Status)'),
		(30, 'Temporarily Unavailable'),
		(50, 'Operational'),
		(75, 'Partly Operational (Mixed)'),
		(100, 'Not Operational'),
		(150, 'Planned For Future Date'),
		(200, 'Removed (Decommissioned)'),
		(210, 'Removed (Duplicate Listing)'),
	]

	USAGE_TYPE_CHOICES = [
		(0, 'Unknown'),
		(6, 'Private - For Staff'),
		(2, 'Private - Restricted Access'),
		(3, 'Privately Owned - Notice Required'),
		(1, 'Public'),
		(4, 'Public - Membership Required'),
		(7, 'Public - Notice Required'),
		(5, 'Public - Pay At Location'),
	]
	CHARGER_TYPE_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
        ]
    
    KW_POWER_CHOICES = [
        (1, 'Under 2 kW'),
        (2, 'Over 2 kW'),
        (3, 'Over 40 kW'),
    ]
    #charging_point_id = models.AutoField(primary_key=True)
    #uncomment the next line when ready
    #owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    #Test
    owner = models.CharField(max_length = 15, defualt = "Tzourhs")
    #EndTest
    connection_type = models.IntegerField(choices = CONNECTION_TYPE_CHOICES)
    current_type = models.IntegerField(choices = CURRENT_TYPE_CHOICES)
    status_type = models.IntegerField(choices = STATUS_TYPE_CHOICES)
    charging_station = models.ForeignKey(ChargingStation , on_delete = models.CASCADE)
    location = models.ForeignKey(Location , on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    type_ = models.IntegerField(,choices = CHARGER_TYPE_CHOICES)
    usage_type_id = models.IntegerField(choices = USAGE_TYPE_CHOICES)
    kw_power = models.IntegerField(choices = KW_POWER_CHOICES)
    usage_cost = models.FloatField()
    volts_power = models.FloatField()
    amps_power = models.FloatField()

    def __str__(self):
        return f'Id = {self.id}'