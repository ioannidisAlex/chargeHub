# Generated by Django 3.1.7 on 2021-03-12 18:56

import uuid

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import multiselectfield.db.fields
import phone_field.models
from django.conf import settings
from django.db import migrations, models

import common.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, unique=True
                    ),
                ),
                (
                    "user_type",
                    models.IntegerField(
                        choices=[
                            (1, "Regular User"),
                            (2, "Station Owner"),
                            (3, "Energy Provider"),
                        ],
                        default=1,
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="ChargingPoint",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "connection_type",
                    models.IntegerField(
                        choices=[
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
                    ),
                ),
                (
                    "current_type",
                    models.IntegerField(
                        choices=[
                            (1, "AC - Single Phase"),
                            (2, "AC - Three Phase"),
                            (3, "DC"),
                        ]
                    ),
                ),
                (
                    "status_type",
                    models.IntegerField(
                        choices=[
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
                    ),
                ),
                (
                    "charger_type",
                    models.IntegerField(
                        choices=[(1, "Low"), (2, "Medium"), (3, "High")]
                    ),
                ),
                (
                    "usage_type_id",
                    models.IntegerField(
                        choices=[
                            (0, "Unknown"),
                            (6, "Private - For Staff"),
                            (2, "Private - Restricted Access"),
                            (3, "Privately Owned - Notice Required"),
                            (1, "Public"),
                            (4, "Public - Membership Required"),
                            (7, "Public - Notice Required"),
                            (5, "Public - Pay At Location"),
                        ]
                    ),
                ),
                (
                    "kw_power",
                    models.IntegerField(
                        choices=[(1, "Under 2 kW"), (2, "Over 2 kW"), (3, "Over 40 kW")]
                    ),
                ),
                (
                    "usage_cost",
                    models.FloatField(validators=[common.validators.validate_positive]),
                ),
                (
                    "volts_power",
                    models.FloatField(validators=[common.validators.validate_positive]),
                ),
                (
                    "amps_power",
                    models.FloatField(validators=[common.validators.validate_positive]),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Cluster",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("cluster_name", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("email", models.EmailField(max_length=254)),
                ("website", models.URLField()),
                (
                    "telephone",
                    phone_field.models.PhoneField(blank=True, max_length=31, null=True),
                ),
                ("title", models.CharField(max_length=15)),
                ("town", models.CharField(max_length=20)),
                (
                    "country",
                    django_countries.fields.CountryField(max_length=2, null=True),
                ),
                ("address_line", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("payment_req", models.BooleanField(default=False)),
                (
                    "payment_method",
                    models.CharField(
                        choices=[
                            ("credit_card", "credit card"),
                            ("cash", "cash"),
                            ("paypal", "paypal"),
                            ("coupon", "coupon"),
                        ],
                        default="cash",
                        max_length=20,
                    ),
                ),
                (
                    "cost",
                    models.FloatField(
                        blank=True, validators=[common.validators.validate_positive]
                    ),
                ),
                ("invoice", models.CharField(max_length=100)),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Provider",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("provider_name", models.CharField(max_length=20)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VehicleModel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "engine_type",
                    models.CharField(
                        choices=[
                            ("bev", "Battery Electric Vehicle"),
                            ("phev", "Plugin Hybrid Electric Vehicle"),
                            ("hev", "Hybrid Electric Vehicle"),
                        ],
                        max_length=8,
                    ),
                ),
                ("release_year", models.PositiveSmallIntegerField(null=True)),
                ("brand", models.CharField(max_length=32)),
                ("variant", models.CharField(blank=True, max_length=32)),
                ("model", models.CharField(max_length=64)),
                (
                    "ac_ports",
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[("type1", "Type1"), ("type2", "Type2")],
                        max_length=5,
                        null=True,
                    ),
                ),
                ("ac_usable_phaces", models.PositiveIntegerField()),
                (
                    "ac_max_power",
                    models.FloatField(validators=[common.validators.validate_positive]),
                ),
                ("ac_charging_power", models.JSONField(blank=True, null=True)),
                (
                    "dc_ports",
                    multiselectfield.db.fields.MultiSelectField(
                        choices=[
                            ("ccs", "Combined Charging System"),
                            ("chademo", "Chademo"),
                            ("tesla_ccs", "Tesla Combined Charging System"),
                            ("tesla_suc", "Tesla Supercharger"),
                        ],
                        max_length=12,
                        null=True,
                    ),
                ),
                (
                    "dc_max_power",
                    models.FloatField(
                        null=True, validators=[common.validators.validate_positive]
                    ),
                ),
                ("dc_charging_curve", models.JSONField(blank=True, null=True)),
                ("is_default_curve", models.BooleanField(null=True)),
                (
                    "usable_battery_size",
                    models.FloatField(validators=[common.validators.validate_positive]),
                ),
                (
                    "average_energy_consumption",
                    models.FloatField(validators=[common.validators.validate_positive]),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VehicleOwner",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vehicle_owner",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vehicle",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vehicles",
                        to="common.vehiclemodel",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="vehicles",
                        to="common.vehicleowner",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("protocol", models.TextField(default="Unknown")),
                ("user_comments_ratings", models.TextField()),
                ("kwh_delivered", models.IntegerField()),
                ("site_id", models.UUIDField(default=uuid.uuid4, editable=False)),
                ("connect_time", models.DateTimeField()),
                ("disconnect_time", models.DateTimeField(null=True)),
                ("done_charging_time", models.DateTimeField(null=True)),
                (
                    "charging_point",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to="common.chargingpoint",
                    ),
                ),
                (
                    "payment",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="common.payment"
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.provider",
                    ),
                ),
                (
                    "vehicle",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to="common.vehicle",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(default="default.jpg", upload_to="profile_pics"),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Owner",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ChargingStation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "cluster",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="common.cluster"
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.location",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="common.owner"
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="common.provider",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="chargingpoint",
            name="charging_station",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="common.chargingstation"
            ),
        ),
    ]
