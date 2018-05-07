from django.db.models.signals import post_save
from django.contrib.auth.models import User

from base.models import Profile


def create_profile(sender, instance: User, **kwargs):
    if not instance.profile:
        Profile.objects.create(user=instance)


post_save.connect(create_profile, User)
