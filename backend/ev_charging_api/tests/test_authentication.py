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


def test_an_admin_view(admin_api_client):
    response = admin_api_client.get(reverse("healthcheck"))
    assert response.status_code == 200


def test_cors_same_origin(client):
    response = client.options("/", HTTP_ORIGIN="http://localhost:8000")
    assert response[ACCESS_CONTROL_ALLOW_ORIGIN] == "http://localhost:8000"
    assert response[ACCESS_CONTROL_ALLOW_HEADERS] == ", ".join(
        list(default_headers)
        + [
            "x-observatory-auth",
        ]
    )


def test_cors_different_origin(client):
    response = client.options("/", HTTP_ORIGIN="http://localhost:8001")
    assert ACCESS_CONTROL_ALLOW_ORIGIN not in response
    assert ACCESS_CONTROL_ALLOW_HEADERS not in response


test_data = [
    (reverse("healthcheck"), "get"),
    (reverse("usermod", args=["a", "a"]), "post"),
    (reverse("sessionsupd"), "post"),
    (reverse("resetsessions"), "post"),
    ("evcharge/api/admin/user/1", "get"),
]


@pytest.mark.parametrize("url,method", test_data)
def test_admin_can_access_admin_endpoints(url, method, admin_api_client):
    response = getattr(admin_api_client, method)(url)
    assert response.status_code not in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_403_FORBIDDEN,
    )


@pytest.mark.parametrize("url,method", test_data)
def test_user_cannot_access_admin_endpoints(url, method, api_client):
    response = getattr(api_client, method)(url)
    assert response.status_code in (
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
    )


@pytest.mark.parametrize("url,method", test_data)
def test_unauthenticated_cannot_access_admin_endpoints(
    url, method, unauthenticated_api_client
):
    response = getattr(unauthenticated_api_client, method)(url)
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
    )


@pytest.mark.parametrize("url,method", test_data)
def test_old_authorization_cannot_access_admin_endpoints(
    url, method, old_admin_api_client
):
    response = getattr(old_admin_api_client, method)(url)
    assert response.status_code in (
        status.HTTP_401_UNAUTHORIZED,
        status.HTTP_404_NOT_FOUND,
    )
