from django.urls import reverse
from hypothesis import HealthCheck, given, settings
from hypothesis.strategies import *

from common import models
from ev_charging_api.tests.utils import ApiClientTestCase, generate_single


class MyTest(ApiClientTestCase):
    @settings(
        max_examples=1,
        suppress_health_check=[
            HealthCheck.too_slow,
            HealthCheck.filter_too_much,
        ],
    )
    @given(s=generate_single(models.Session))
    def test_session_single_day(self, s):
        assert s.connect_time
