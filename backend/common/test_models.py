import pytest

from common.models import User, VehicleOwner


# Create your tests here.
@pytest.mark.django_db
def test_vehicle_owner_creation():
    user = User.objects.create(user_type=1, username="user", password="password345")
    assert user.vehicle_owner
    assert not getattr(user, "provider", None)
    assert not getattr(user, "owner", None)
