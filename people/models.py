from django.db import models


class Person(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    race = models.ForeignKey(
        'people.Population',
        on_delete=models.SET_NULL,
        related_name='members_of_race',
        null=True,
    )
    organizations_in = models.ManyToManyField(
        'people.Organization',
        related_name='members',
    )
    populations_in = models.ManyToManyField(
        'people.Population',
        related_name='members',
    )

    MALE = 1
    FEMALE = 2
    OTHER = 3
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]
    gender = models.IntegerField(choices=GENDER_CHOICES)


class Organization(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    parent_org = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='child_orgs',
        null=True,
    )

    FAMILY = 1
    RELIGION = 2
    POLITICAL = 3
    MILITARY = 4
    CLAN = 5
    OTHER = 99
    ORG_TYPE_CHOICES = [
        (FAMILY, 'Family'),
        (RELIGION, 'Religion'),
        (POLITICAL, 'Political'),
        (MILITARY, 'Military'),
        (CLAN, 'Clan'),

        (OTHER, 'Other'),
    ]
    org_type = models.IntegerField(choices=ORG_TYPE_CHOICES)

    god_followed = models.ForeignKey(
        'people.God',
        on_delete=models.SET_NULL,
        related_name='follower_orgs',
        null=True,
    )


class Population(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    sub_population_of = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='sub_populations',
        null=True
    )


class God(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    gender = models.IntegerField(choices=Person.GENDER_CHOICES)
    patron_of = models.CharField(max_length=255, null=True)

    # todo: install django-multiselectfield and switch cleric domains to this
    cleric_domains = models.CharField(max_length=255, null=True)

    follower_populations = models.ManyToManyField(
        'people.Population',
        related_name='gods_followed',
    )
