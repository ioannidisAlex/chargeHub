'''import pytest
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

test_data = [
    (reverse("healthcheck"), "get"),
    (reverse("usermod", args=["a", "a"]), "post"),
    (reverse("sessionsupd"), "post"),
    (reverse("resetsessions"), "post"),
    ("evcharge/api/admin/user/1", "get"),
]

@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert User.objects.count() == 1'''