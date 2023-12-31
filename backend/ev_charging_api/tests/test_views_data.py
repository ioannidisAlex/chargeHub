from datetime import datetime, timedelta

from django.urls import reverse
from hypothesis import assume, example, given, settings
from hypothesis.strategies import *

from common import models
from ev_charging_api.tests.utils import (
    USEFUL_SETTINGS,
    ApiClientTestCase,
    generate_single,
)


class MyTest(ApiClientTestCase):
    @settings(max_examples=10, **USEFUL_SETTINGS)
    @given(
        s=generate_single(models.Session),
        d=timedeltas(min_value=timedelta(), max_value=timedelta(days=10000)),
    )
    def test_session_single_day(self, s, d):
        assert s.connect_time
        try:
            ((s.connect_time - d < s.connect_time + d))
        except OverflowError:
            assume(False)
        t1 = s.connect_time - d
        t2 = s.connect_time + d
        response = self.api_client.get(
            reverse(
                "sessions_per_provider",
                args=[s.provider.id, t1.date(), t2.date()],
            )
        )
        assert response.status_code == 200
