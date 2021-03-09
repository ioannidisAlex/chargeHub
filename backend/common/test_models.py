from math import inf, nan

import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from common.models import Payment, User

# Create your tests here.


@pytest.mark.django_db
def test_vehicle_owner_creation():
    user = User.objects.create(user_type=1, username="user", password="password345")
    assert user.vehicle_owner
    assert not getattr(user, "provider", None)
    assert not getattr(user, "owner", None)


@pytest.mark.django_db
class TestPayment(TestCase):
    def test_validate_positive(self):

        payment = Payment(
            id=1, payment_req=False, payment_method="paypal", cost=-2, invoice="miltos"
        )
        with self.assertRaisesRegex(
            ValidationError, "Oups,non-positive values are not allowed"
        ):
            payment.full_clean()

    def test_infinity(self):
        payment = Payment(
            id=1, payment_req=False, payment_method="paypal", cost=inf, invoice="miltos"
        )
        with self.assertRaisesMessage(
            ValidationError, "Oups, infinite values are not allowed"
        ):
            payment.full_clean()

    def test_nan(self):
        payment = Payment(
            id=1, payment_req=False, payment_method="paypal", cost=nan, invoice="miltos"
        )
        with self.assertRaisesMessage(
            ValidationError, "Oups, NaN values are not allowed"
        ):
            payment.full_clean()
