import os
import subprocess as subp
import uuid
from math import inf, nan

import pytest
from django.core.exceptions import ValidationError
from django.shortcuts import get_list_or_404, get_object_or_404
from django.test import TestCase

from common.models import ChargingPoint, Payment, Provider, User

# Create your tests here.


@pytest.mark.django_db
def test_vehicle_owner_creation():
    user = User.objects.create(user_type=1, username="user", password="password345")
    assert user.vehicle_owner
    assert not getattr(user, "provider", None)
    assert not getattr(user, "owner", None)


@pytest.mark.django_db
class TestPayment(TestCase):
    def test_validate_positive(self):

        payment = Payment(
            id=1, payment_req=False, payment_method="paypal", cost=-2, invoice="miltos"
        )
        with self.assertRaisesRegex(
            ValidationError, "Oups,non-positive values are not allowed"
        ):
            payment.full_clean()

    def test_infinity(self):
        payment = Payment(
            id=1, payment_req=False, payment_method="paypal", cost=inf, invoice="miltos"
        )
        with self.assertRaisesMessage(
            ValidationError, "Oups, infinite values are not allowed"
        ):
            payment.full_clean()

    def test_nan(self):
        payment = Payment(
            id=1, payment_req=False, payment_method="paypal", cost=nan, invoice="miltos"
        )
        with self.assertRaisesMessage(
            ValidationError, "Oups, NaN values are not allowed"
        ):
            payment.full_clean()


@pytest.mark.django_db
def test_owner_creation():
    user = User.objects.create(user_type=2, username="user", password="password345")
    assert user.owner
    assert not getattr(user, "provider", None)
    assert not getattr(user, "vehicle_owner", None)


@pytest.mark.django_db
def test_provider_creation():
    user = User.objects.create(user_type=3, username="user", password="password345")
    assert user.provider
    assert not getattr(user, "owner", None)
    assert not getattr(user, "vehicle_owner", None)


@pytest.mark.django_db
def test_charging_points_validity():
    # os.system("./putdata.sh")
    # subp.check_call("./putdata.sh", shell=True)
    from common.models import ChargingPoint

    points = ChargingPoint.objects.all()
    # assert points.count()>499
    for p in points:
        flag = True
        ctflag = False
        for ct in p.CONNECTION_TYPE_CHOICES:
            if p.connection_type == ct[0]:
                ctflag = True
        if not ctflag:
            assert False
    assert True


@pytest.mark.django_db
def test_all_model_creation():
    from common import models

    ids = uuid.uuid4()
    user = models.User.objects.create(
        user_type=1, username="user", password="password345"
    )
    user2 = models.User.objects.create(
        user_type=2, username="user2", password="password345"
    )
    user3 = models.User.objects.create(
        user_type=3, username="user3", password="password345"
    )
    payment = models.Payment.objects.create(
        id=ids,
        payment_req=False,
        payment_method="paypal",
        cost=7,
        invoice="miltos",
        user_id=user,
    )
    vm = models.VehicleModel.objects.create(
        id=ids,
        engine_type="bev",
        brand="Tesla",
        model="Cybertruck",
        ac_max_power=1.0,
        ac_usable_phaces="3",
        usable_battery_size=10.0,
        average_energy_consumption=10.0,
    )
    vehicle = models.Vehicle.objects.create(id=ids, model=vm, owner=user.vehicle_owner)
    location = models.Location.objects.create(
        id=ids,
        email="user@tlmpa.gr",
        website="https://www.tlmpa.gr",
        title="place",
        town="Athens",
        country="Greece",
        address_line="a",
    )
    cluster = models.Cluster.objects.create(id=ids, cluster_name="name")
    chargingstation = models.ChargingStation.objects.create(
        id=ids,
        owner=user2.owner,
        cluster=cluster,
        provider=user3.provider,
        location=location,
    )
    chargingpoint = models.ChargingPoint.objects.create(
        id=ids,
        charging_station=chargingstation,
        connection_type=1,
        current_type=1,
        status_type=0,
        charger_type=1,
        usage_type_id=1,
        kw_power=1,
        usage_cost=1,
        volts_power=1,
        amps_power=1,
    )
    session = models.Session.objects.create(
        id=ids,
        payment=payment,
        user_comments_ratings="",
        provider=user3.provider,
        kwh_delivered=1,
        connect_time="1998-03-03 00:00:00+00:00",
        charging_point=chargingpoint,
        vehicle=vehicle,
    )
    assert session.vehicle.model.model == "Cybertruck"
    assert session.vehicle.owner
    assert chargingpoint.charging_station.cluster
    assert chargingpoint.charging_station.provider
    assert chargingpoint.charging_station.owner
    assert chargingpoint.charging_station.location
    assert session.payment


class TestSomething(TestCase):
    def setUp(self):
        from django.conf import settings

        settings.DEBUG = True

    def test_something(self):
        user75 = User(user_type=2, username="mitsous", password="gurou")
        user75.save()
        prov75 = Provider(user=user75, provider_name="kopal")
        prov75.save()
        # papari = get_object_or_404(Provider.objects.select_related('user'), provider_name="kopal")
        # papari = get_object_or_404(Provider, provider_name="kopal")
        p = get_object_or_404(
            Provider.objects.select_related("user"), provider_name="kopal"
        )
        master = p.user.username
        assert master == "mitsous"

    def tearDown(self):
        from django.db import connection

        for query in connection.queries:
            print(f"{query['sql']}\n")
