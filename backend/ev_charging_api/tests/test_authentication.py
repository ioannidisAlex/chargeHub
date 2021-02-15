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


def test_cors_same_origin(client):
    response = client.options("/", HTTP_ORIGIN="http://localhost:8000/")
    assert response[ACCESS_CONTROL_ALLOW_ORIGIN] == "http://localhost:8000/"
    assert response[ACCESS_CONTROL_ALLOW_HEADERS] == ", ".join(
        list(default_headers)
        + [
            "x-observatory-auth",
        ]
    )


def test_cors_different_origin(client):
    response = client.options("/", HTTP_ORIGIN="http://localhost:8001/")
    assert ACCESS_CONTROL_ALLOW_ORIGIN not in response
    assert ACCESS_CONTROL_ALLOW_HEADERS not in response
