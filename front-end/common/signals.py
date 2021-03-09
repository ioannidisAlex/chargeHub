from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Owner, Profile, Provider, User, VehicleOwner


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if instance.user_type == 1:
        if created:
            Profile.objects.create(user=instance)
            VehicleOwner.objects.create(user=instance)
    if instance.user_type == 2:
        if created:
            Profile.objects.create(user=instance)
            Owner.objects.create(user=instance)
    if instance.user_type == 3:
        if created:
            Profile.objects.create(user=instance)
            Provider.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.profile.save()
        instance.vehicle_owner.save()
    if instance.user_type == 2:
        instance.profile.save()
        instance.owner.save()
    if instance.user_type == 3:
        instance.profile.save()
        instance.provider.save()
