import pytest
from django.urls import reverse


def test_json_csv_get_routed_properly(client):
    response_json = client.get(reverse("healthcheck"), {"format": "json"})
    response_csv = client.get(reverse("healthcheck"), {"format": "csv"})
    assert response_json.status_code == response_csv.status_code == 401
