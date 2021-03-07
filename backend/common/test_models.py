import pytest
from rest_framework.test import RequestsClient

from common.models import User, VehicleOwner


# Create your tests here.
@pytest.mark.django_db
def test_vehicle_owner_creation():
    user = User.objects.create(user_type=1, username="user", password="password345")
    assert user.vehicle_owner
    assert not getattr(user, "provider", None)
    assert not getattr(user, "owner", None)


client = RequestsClient()

"""
LEX = {
    #"Cookie": "X-OBSERVATORY_AUTH=Token9784f7ba356de923d3cb12af98e51ae93da4d549; csrftoken=QSzydvbyr403bZyyamKaVbR4IMPXKiep2vGJlcUiFDjuWWlljKuamc03LASwKnZr; sessionid=7tx31nh9uthuuqwid7dvv3tuthbg1n1l",
    #"Postman-Cookie": "416b0a54-7982-4bf6-82c8-3e23f8ffecde",
    #"Content-Type": "multipart/form-data; boundary=boundary=aBoundaryString",
    #"Content-Length": "285",
    #"Host": "127.0.0.1:8000",
    #"User-Agent": "PostmanRuntime/7.26.10",
    #"Accept": "*/*",
    #"Accept-Encoding": "gzip,deflate,br",
    #"Connection": "keep-alive",
    "X-CSRFToken": "mhzhamhTu3AjWHYlWQL2K2vRyurl4vuDg8FIo9PjG7wgQr8ZCm0S2CzJodQiEN82",
}
response = client.get('http://localhost:8000/home/')
#csrftoken = response.cookies['csrftoken']
#name, value = response.cookies['name'], response.cooikies['value']
assert response.status_code == 200
csrftoken = response.cookies['csrftoken']
CREDENTIALS = {
    "username": "fedra",
    "password": "gggggggg8*"
}

"""
# Obtain a CSRF token.
# response = client.post('http://localhost:8000/login/', data=CREDENTIALS, headers=LEX)
# assert response.status_code == 200
# csrftoken = response.cookies['csrftoken']

# Interact with the API.
# response = client.post('http://localhost:8000/login/', json={
#    'username': 'fedra',
#    'password': 'gggggggg8*'
# }, headers={'X-CSRFToken': csrftoken})
# assert response.status_code == 200

response = client.get("http://localhost:8000/home")
assert response.status_code == 200
csrftoken = response.cookies["csrftoken"]

response = client.post("http://localhost/")
