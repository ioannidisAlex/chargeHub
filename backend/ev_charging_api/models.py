from django.db import models
from django.contrib.auth.signals import user_logged_in

'''
def login_handler(sender, user, request, **kwargs):
    print('logged in')

user_logged_in.connect(login_handler)
'''