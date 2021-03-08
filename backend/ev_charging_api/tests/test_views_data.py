from django.urls import reverse
from hypothesis import HealthCheck, Phase, Verbosity, given, settings
from hypothesis.strategies import *

from common import models
from ev_charging_api.tests.utils import (
    USEFUL_SETTINGS,
    ApiClientTestCase,
    generate_single,
)


class MyTest(ApiClientTestCase):
    @settings(max_examples=1, **USEFUL_SETTINGS)
    @given(s=generate_single(models.Session))
    def test_session_single_day(self, s):
        assert s.connect_time
