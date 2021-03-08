import pytest
from django.db.models import Model
from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import *

from common import models
from ev_charging_api.tests.utils import generate_single


def all_models():
    return [
        x
        for x in models.__dict__.values()
        if isinstance(x, type) and issubclass(x, Model) and "Abstract" not in x.__name__
    ]


def test_models_exist():
    assert all_models() != []


@pytest.mark.django_db
@settings(
    max_examples=2,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
)
@given(data())
def test_model_generation(data):
    for m in all_models():
        assert data.draw(generate_single(m))


@pytest.mark.django_db
@settings(
    max_examples=2,
    suppress_health_check=[HealthCheck.too_slow, HealthCheck.filter_too_much],
)
@given(data())
def test_model_generation_second(data):
    for m in all_models():
        assert isinstance(data.draw(generate_single(m)), m)
