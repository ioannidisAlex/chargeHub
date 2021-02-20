import pytest
from django.urls import reverse


def test_json_csv_get_routed_properly(client):
    response_json = client.get(reverse("healthcheck"), {"format": "json"})
    response_csv = client.get(reverse("healthcheck"), {"format": "csv"})
    response_raw = client.get(reverse("healthcheck"))
    assert (
        response_json.status_code
        == response_csv.status_code
        == response_raw.status_code
        == 401
    )


def test_csv_output_healthcheck_unauthenticated(client):
    response_csv = client.get(reverse("healthcheck"), {"format": "csv"})
    assert (
        response_csv.content
        == b"detail\r\nAuthentication credentials were not provided.\r\n"
    )


def test_csv_output_healthcheck(admin_api_client):
    response_csv = admin_api_client.get(reverse("healthcheck"), {"format": "csv"})
    assert response_csv.content == b"status\r\nOK\r\n"


def test_json_output_healthcheck(admin_api_client):
    response_json = admin_api_client.get(reverse("healthcheck"), {"format": "json"})
    assert response_json.content == b'{"status":"OK"}'


def test_json_is_default(client):
    response_json = client.get(reverse("healthcheck"), {"format": "json"})
    response_raw = client.get(reverse("healthcheck"))
    assert (
        response_json.content
        == response_raw.content
        == b'{"detail":"Authentication credentials were not provided."}'
    )
