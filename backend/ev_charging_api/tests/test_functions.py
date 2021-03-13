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

logout_data = [(reverse("logout"), "post")]
login_data = [(reverse("login"), "post")]
session_calls = [
    (
        reverse(
            "sessions_per_point",
            args=[str(uuid.uuid4()), date(2014, 4, 17), date(2014, 6, 18)],
        ),
        "get",
    ),
    (
        reverse(
            "sessions_per_station",
            args=[str(uuid.uuid4()), date(2014, 4, 17), date(2014, 6, 18)],
        ),
        "get",
    ),
    (
        reverse(
            "sessions_per_vehicle",
            args=[str(uuid.uuid4()), date(2014, 4, 17), date(2014, 6, 18)],
        ),
        "get",
    ),
    (
        reverse(
            "sessions_per_provider",
            args=[str(uuid.uuid4()), date(2014, 4, 17), date(2014, 6, 18)],
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
    assert response.status_code == 400


# sessions_per_point
# sessions_per_station
# sessions_per_vehicle
# sessions_per_provider
# password_reset
# password_reset_done
# password_reset_confirm
# password_reset_complete
