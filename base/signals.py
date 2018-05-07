from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group

from base.models import Profile


def create_profile(sender, instance: User, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)


def add_to_users(sender, instance: User, **kwargs):
    users = Group.objects.get(name='Users')
    if instance not in users.user_set.all():
        users.user_set.add(instance)


post_save.connect(create_profile, User)
post_save.connect(add_to_users, User)
