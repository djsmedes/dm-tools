from django.db.models.signals import post_save
from django.contrib.auth.models import User

from base.models import Profile


def create_profile(sender, instance: User, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    print(type(instance.profile))


post_save.connect(create_profile, User)
