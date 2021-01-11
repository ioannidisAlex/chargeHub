from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.signals import user_logged_in

'''
def login_handler(sender, user, request, **kwargs):
    print('logged in')

user_logged_in.connect(login_handler)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_auth_token(sender, instance=None, **kwargs):
	instance.token.save()
'''