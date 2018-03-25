from django.db import models


class Person(models.Model):

    name = models.CharField(max_length=255)
    # race = ??? a serializable python class probably?
    organizations_in = models.ManyToManyField(
        'people.Organization',
        related_name='members',
        null=True,
    )


class Organization(models.Model):

    name = models.CharField(max_length=255)
    parent_org = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
    )
