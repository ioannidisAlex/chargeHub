from django.db import models
#uncomment when ready
#from ... import Owner


class Location(models.Model):
	LocationId = models.AutoField(primary_key=True)
	#ChargingPoint = models.ForeignKey(ChargingPoint, on_delete = models.CASCADE)
	email = models.CharField(max_length = 100)
	website = models.CharField(max_length = 100)
	telephone = models.CharField(max_length = 13)
	title = models.CharField(max_length = 100)
	town = models.CharField(max_length = 100)
	country = models.CharField(max_length = 100)
	PostalCode = models.IntegerField()
	AddresLine = models.CharField(max_length = 100)

	def __str__(self):
		return f'Id = {self.LocationId}'

class Cluster(models.Model):
	ClusterName = models.CharField(max_length = 100, default = "Tzourhs")
	clusterId = models.AutoField(primary_key = True)

	def __str__(self):
		return f'Id = {self.ClusterId}'

class Provider(models.Model):
	ProviderId = models.AutoField(primary_key = True)
	ProviderName = models.CharField(max_length = 100)

	def __str__(self):
		return f'Id = {self.ProviderId}'

class ChargingStation(models.Model):
	NrChargingCategories = models.IntegerField()
	chargingStationId = models.AutoField(primary_key = True)
	Cluster = models.ForeignKey(Cluster, on_delete = models.CASCADE)
	Provider = models.ForeignKey(Provider , on_delete = models.CASCADE)
    
	def __str__(self):
		return f'Id = {self.ChargingStationId}'


class ChargingPoint(models.Model):
	#uncomment the next line when ready
    #owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    #Test
    owner = models.CharField(max_length = 100 , default = "Tzourhs")
    #EndTest
    chargingStation = models.ForeignKey(ChargingStation , on_delete = models.CASCADE, null = True)
    ChargingPointId = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location , on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    UsageTypeId = models.CharField(max_length = 100)
    Type = models.CharField(max_length = 100)
    UsageCost = models.FloatField()
    KwPower = models.FloatField()
    VoltsPower = models.FloatField()
    AmpsPower = models.FloatField()

    def __str__(self):
        return f'Id = {self.ChargingPointId}'