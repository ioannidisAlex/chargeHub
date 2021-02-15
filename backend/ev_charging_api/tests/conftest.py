import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def admin_api_client(admin_user):
    token = Token.objects.create(user=admin_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.fixture
def authenticated_api_client(django_user_model):
    user = django_user_model.objects.create(username="client", password="client")
    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client


@pytest.fixture
def unauthenticated_api_client():
    return APIClient()


@pytest.fixture
def api_client(authenticated_api_client):
    return authenticated_api_client
