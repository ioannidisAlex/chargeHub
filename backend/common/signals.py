from django import dispatch
from django.db.models import signals
from django.conf import settings

from common.models import Profile


@dispatch.receiver(signals.post_save,sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
