from django.urls import resolve, reverse
from hypothesis import assume, given, settings
from hypothesis.strategies import *


@settings(max_examples=1000)
@given(
    sampled_from(
        [
            "sessions_per_station",
            "sessions_per_station",
            "sessions_per_point",
            "sessions_per_vehicle",
        ]
    ),
    uuids(),
    dates(),
    dates(),
)
def test_date_converter(endpoint, u, d1, d2):
    output_url = reverse(endpoint, args=[u, d1, d2])
    assert output_url.endswith(f"{u}/{d1:%Y%m%d}/{d2:%Y%m%d}/")
    n, a, kw = resolve(output_url)
    assert kw == {"date_from": d1, "date_to": d2, "id": u}
