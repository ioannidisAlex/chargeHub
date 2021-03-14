import json
import uuid
from datetime import date

import pytest
from corsheaders.defaults import default_headers
from corsheaders.middleware import (
    ACCESS_CONTROL_ALLOW_CREDENTIALS,
    ACCESS_CONTROL_ALLOW_HEADERS,
    ACCESS_CONTROL_ALLOW_METHODS,
    ACCESS_CONTROL_ALLOW_ORIGIN,
    ACCESS_CONTROL_EXPOSE_HEADERS,
    ACCESS_CONTROL_MAX_AGE,
)
from django.urls import reverse
from rest_framework import status

ids = str(uuid.uuid4())

logout_data = [(reverse("logout"), "post")]
login_data = [(reverse("login"), "post")]
session_calls = [
    (
        reverse(
            "sessions_per_point",
            args=[ids, date(2014, 4, 17), date(2014, 6, 18)],
        ),
        "get",
    ),
    (
        reverse(
            "sessions_per_station",
            args=[ids, date(2014, 4, 17), date(2014, 6, 18)],
        ),
        "get",
    ),
    (
        reverse(
            "sessions_per_vehicle",
            args=[ids, date(2014, 4, 17), date(2014, 6, 18)],
        ),
        "get",
    ),
    (
        reverse(
            "sessions_per_provider",
            args=[ids, date(2014, 4, 17), date(2014, 6, 18)],
        ),
        "get",
    ),
]


@pytest.mark.parametrize("url,method", logout_data)
def test_logout(authenticated_api_client, url, method):
    response = getattr(authenticated_api_client, method)(url)
    assert response.status_code == 200


@pytest.mark.parametrize("url,method", login_data)
def test_login(client, url, method, django_user_model):
    user = django_user_model.objects.create(username="client", password="client")
    client.login(username="client", password="client")
    response = client.post(url)
    # print(type(response.content))
    # response = getattr(client, method)(url)
    # json_data=(response.content)
    # json_data = json.loads(response.content)
    # assert type(response) == 'dict'
    assert response.status_code == 200


@pytest.mark.parametrize("url,method", session_calls)
def test_sessions_calls(authenticated_api_client, url, method):
    response = getattr(authenticated_api_client, method)(url)
    assert response.status_code == 404


@pytest.mark.parametrize("url,method", session_calls[:-1])
def test_session_consistency(authenticated_api_client, url, method):
    from common import models

    # ids = uuid.uuid4()
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
        connect_time="2014-05-03 00:00:00+00:00",
        charging_point=chargingpoint,
        vehicle=vehicle,
    )
    response = getattr(authenticated_api_client, method)(url)
    assert response.status_code == 200


# sessions_per_point
# sessions_per_station
# sessions_per_vehicle
# sessions_per_provider
# password_reset
# password_reset_done
# password_reset_confirm
# password_reset_complete
