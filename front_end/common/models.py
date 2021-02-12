import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from localflavor.gr.forms import GRPostalCodeField
from multiselectfield import MultiSelectField
from phone_field import PhoneField
from PIL import Image


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        (1, "Regular User"),
        (2, "Station Owner"),
        (3, "Energy Provider"),
    ]
    email = models.EmailField(unique=True)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, default=1)


class VehicleOwner(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="vehicle_owner"
    )

    def __str__(self):
        return f"{self.user.username}"


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

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    engine_type = models.CharField(max_length=8, choices=Engine.choices)
    release_year = models.PositiveSmallIntegerField(null=True)
    brand = models.CharField(max_length=32)
    variant = models.CharField(max_length=32, blank=True)
    model = models.CharField(max_length=64)
    # category? car,...

    ac_ports = MultiSelectField(choices=AcCharger.choices, max_choices=2, max_length=5)
    ac_usable_phaces = models.PositiveIntegerField()
    ac_max_power = models.FloatField()
    ac_charging_power = models.JSONField()

    dc_ports = MultiSelectField(choices=DcCharger.choices, max_choices=4, max_length=12)
    dc_max_power = models.FloatField(null=True)
    dc_charging_curve = models.JSONField(null=True)
    is_default_curve = models.BooleanField(null=True)

    usable_battery_size = models.FloatField()
    average_energy_consumption = models.FloatField()

    def __str__(self):
        return "%s  %s" % (self.brand, self.model)


class Vehicle(models.Model):
    model = models.ForeignKey(
        VehicleModel, on_delete=models.CASCADE, related_name="vehicles"
    )
    owner = models.ForeignKey(
        VehicleOwner, on_delete=models.CASCADE, related_name="vehicles"
    )
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return "%s's %s" % (self.owner, self.model)


class Profile(models.Model):
    user = models.OneToOneField(
        User, unique=True, related_name="profile", on_delete=models.CASCADE
    )
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return f"{self.user.username} Profile"


class Location(models.Model):
    # location_id = models.AutoField(primary_key = True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    email = models.EmailField()
    website = models.URLField()
    telephone = PhoneField(blank=True)
    title = models.CharField(max_length=15)
    town = models.CharField(max_length=20)
    country = CountryField()
    post_code = GRPostalCodeField()
    address_line = models.CharField(max_length=100)

    def __str__(self):
        return f"Title = {self.title}"


class Cluster(models.Model):
    # cluster_id = models.AutoField(primary_key = True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    cluster_name = models.CharField(max_length=15)

    def __str__(self):
        return f"Cluster name = {self.cluster_name}"


class Provider(models.Model):
    # provider_id = models.AutoField(primary_key = True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    provider_name = models.CharField(max_length=20)

    def __str__(self):
        return f"Provider name = {self.user.username}"


class ChargingStation(models.Model):
    # charging_station_id = models.AutoField(primary_key = True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster, on_delete=models.CASCADE)
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)

    def __str__(self):
        return f"Id = {self.id}"


class ChargingPoint(models.Model):
    CONNECTION_TYPE_CHOICES = [
        (7, "Avcon Connector"),
        (4, "Blue Commando (2P+E)"),
        (3, "BS1363 3 Pin 13 Amp"),
        (32, "CCS (Type 1)"),
        (33, "CCS (Type 2)"),
        (16, "CEE 3 Pin"),
        (17, "CEE 5 Pin"),
        (28, "CEE 7/4 - Schuko - Type F"),
        (23, "CEE 7/5"),
        (18, "CEE+ 7 Pin"),
        (2, "CHAdeMO"),
        (13, "Europlug 2-Pin (CEE 7/16)"),
        (1038, "GB-T AC - GB/T 20234.2 (Socket)"),
        (1039, "GB-T AC - GB/T 20234.2 (Tethered Cable)"),
        (1040, "GB-T DC - GB/T 20234.3"),
        (34, "IEC 60309 3-pin"),
        (35, "IEC 60309 5-pin"),
        (5, "LP Inductive"),
        (10, "NEMA 14-30"),
        (11, "NEMA 14-50"),
        (22, "NEMA 5-15R"),
        (9, "NEMA 5-20R"),
        (15, "NEMA 6-15"),
        (14, "NEMA 6-20"),
        (1042, "NEMA TT-30R"),
        (36, "SCAME Type 3A (Low Power)"),
        (26, "SCAME Type 3C (Schneider-Legrand)"),
        (6, "SP Inductive"),
        (1037, "T13 - SEC1011 ( Swiss domestic 3-pin ) - Type J"),
        (30, "Tesla (Model S/X)"),
        (8, "Tesla (Roadster)"),
        (31, "Tesla Battery Swap"),
        (27, "Tesla Supercharger"),
        (1041, "Three Phase 5-Pin (AS/NZ 3123)"),
        (1, "Type 1 (J1772)"),
        (25, "Type 2 (Socket Only)"),
        (1036, "Type 2 (Tethered Connector)"),
        (29, "Type I (AS 3112)"),
        (0, "Unknown"),
        (24, "Wireless Charging"),
        (21, "XLR Plug (4 pin)"),
    ]

    CURRENT_TYPE_CHOICES = [
        (1, "AC - Single Phase"),
        (2, "AC - Three Phase"),
        (3, "DC"),
    ]

    STATUS_TYPE_CHOICES = [
        (0, "Unknown"),
        (10, "Currently Available (Automated Status)"),
        (20, "Currently In Use (Automated Status)"),
        (30, "Temporarily Unavailable"),
        (50, "Operational"),
        (75, "Partly Operational (Mixed)"),
        (100, "Not Operational"),
        (150, "Planned For Future Date"),
        (200, "Removed (Decommissioned)"),
        (210, "Removed (Duplicate Listing)"),
    ]

    USAGE_TYPE_CHOICES = [
        (0, "Unknown"),
        (6, "Private - For Staff"),
        (2, "Private - Restricted Access"),
        (3, "Privately Owned - Notice Required"),
        (1, "Public"),
        (4, "Public - Membership Required"),
        (7, "Public - Notice Required"),
        (5, "Public - Pay At Location"),
    ]

    CHARGER_TYPE_CHOICES = [
        (1, "Low"),
        (2, "Medium"),
        (3, "High"),
    ]

    KW_POWER_CHOICES = [
        (1, "Under 2 kW"),
        (2, "Over 2 kW"),
        (3, "Over 40 kW"),
    ]

    IS_ACTIVE_CHOICES = [
    (1,"Active"),
    (2,"Inactive"),
    ]

    # charging_point_id = models.AutoField(primary_key=True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    charging_station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    connection_type = models.IntegerField(choices=CONNECTION_TYPE_CHOICES)
    current_type = models.IntegerField(choices=CURRENT_TYPE_CHOICES)
    status_type = models.IntegerField(choices=STATUS_TYPE_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    charger_type = models.IntegerField(choices=CHARGER_TYPE_CHOICES)
    usage_type_id = models.IntegerField(choices=USAGE_TYPE_CHOICES)
    kw_power = models.IntegerField(choices=KW_POWER_CHOICES)
    usage_cost = models.FloatField()
    volts_power = models.FloatField()
    amps_power = models.FloatField()
    is_active = models.IntegerField(choices=IS_ACTIVE_CHOICES, default=2)

    def __str__(self):
        return f"Id = {self.id}"

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    _PAYMENT_METHODS = [
        ("credit_card", "credit card"),
        ("cash", "cash"),
        ("paypal", "paypal"),
        ("coupon", "coupon"),
    ]

    payment_req = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=20, choices=_PAYMENT_METHODS, default="cash"
    )
    cost = models.FloatField(blank=True)
    invoice = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    #session_id = models.OneToOneField(Session, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)

class Session(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    protocol = models.TextField(default="Unknown")
    user_comments_ratings = models.TextField()
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    # cluster = models.CharField(max_length=100)   #potential fk Null
    kwh_delivered = models.IntegerField()  # check type
    site_id = models.UUIDField(editable=False, default=uuid.uuid4)
    connect_time = models.DateTimeField(null=True)
    disconnect_time = models.DateTimeField(null=True)
    done_charging_time = models.DateTimeField(null=True)
    charging_point = models.ForeignKey(
        ChargingPoint, on_delete=models.CASCADE, related_name="sessions"
    )
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="sessions"
    )

    def __str__(self):
        return f"Id = {self.id}"