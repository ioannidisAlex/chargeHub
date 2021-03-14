import time

from locust import HttpUser, TaskSet, task

LOGIN_URL = "/login/?next=/"
DATA = {"username": "ilias", "password": "iiiiii6^"}

"""
class LoginAndGet(TaskSet):
    def on_start(self):
        self.login()
    def login(l):
        response = l.client.get(LOGIN_URL, name='LOGIN_URL')
        csrftoken = response.cookies['csrftoken']
        l.client.post(LOGIN_URL, {"username": "fedra", "password": "gggggggg8*"}, headers={"X-CSRFToken": csrftoken}, name="LOGIN_URL")

    task(1)
    def lessson(l):
        l.client.get("http://127.0.0.1:8765/profile")
"""


class MyLocust(HttpUser):

    min_wait = 0
    max_wait = 0

    csrftoken = "m"
    x_observatory_auth = "m"

    def on_start(self):
        response = self.client.get("http://127.0.0.1:8765/login/?next=/")
        global csrftoken
        csrftoken = response.cookies["csrftoken"]
        self.client.post(
            "http://127.0.0.1:8765/login/",
            data=DATA,
            headers={"X-CSRFToken": csrftoken},
        )
        response2 = self.client.post(
            "/evcharge/api/login/", data=DATA, headers={"X-CSRFToken": csrftoken}
        )
        global x_observatory_auth
        # x_observatory_auth = response2.cookies['X-OBSERVATORY_AUTH']
        x_observatory_auth = response2.text
        x_observatory_auth = x_observatory_auth[10:-2]
        # print(text)

    # task_set = LoginAndGet

    @task
    def take_profil(self):
        # self.client.get('/profile')
        global csrftoken
        specialtoken = csrftoken
        global x_observatory_auth
        specialauth = "Token " + x_observatory_auth

        HEADERS = {"X-CSRFToken": specialtoken, "X-OBSERVATORY-AUTH": specialauth}

        # id = 123e4567-e89b-12d3-a456-426614174000
        # {"X-CSRFToken": specialtoken, "X-OBSERVATORY-AUTH": specialauth}
        self.client.get(
            "/evcharge/api/SessionsPerPoint/de512cc4-047d-4ea4-b12a-1060dbdfef46/20190901/20190903/",
            data=DATA,
            headers=HEADERS,
        )


#  123e4567-e89b-12d3-a456-426614174000
