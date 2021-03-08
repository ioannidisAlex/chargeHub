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
        with self.assertRaises(ValidationError):
            payment.full_clean()
