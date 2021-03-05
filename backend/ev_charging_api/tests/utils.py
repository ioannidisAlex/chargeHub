from django.db import models
from hypothesis.extra.django import TestCase, from_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from common.models import User


def generate_single(m: models.Model, **kw):
    field_strategies = {
        field.name: generate_single(field.related_model)
        for field in m._meta.concrete_fields
        if isinstance(field, (models.ForeignKey, models.OneToOneField))
    }
    field_strategies.update(kw)
    return from_model(m, **field_strategies)


class ApiClientTestCase(TestCase):
    """docstring for MyTest"""

    def setUp(self):
        user = User.objects.create(username="client2", password="client2")
        token = Token.objects.create(user=user)
        client = APIClient()
        client.credentials(HTTP_X_OBSERVATORY_AUTH="Token " + token.key)
        self.api_client = client
