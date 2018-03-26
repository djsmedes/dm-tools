from django.db import models
from django.shortcuts import reverse


class NamedModel(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Person(NamedModel):

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


class Organization(NamedModel):

    description = models.TextField(null=True)
    parent_org = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='child_orgs',
        null=True,
    )
    member_count = models.IntegerField(
        help_text='Including unnamed members not in the database.',
        null=True,
    )

    # todo: implement organization type... probably as a subclass? for now this can go in description
    # FAMILY = 1
    # RELIGION = 2
    # POLITICAL = 3
    # MILITARY = 4
    # CLAN = 5
    # OTHER = 99
    # ORG_TYPE_CHOICES = [
    #     (FAMILY, 'Family'),
    #     (RELIGION, 'Religion'),
    #     (POLITICAL, 'Political'),
    #     (MILITARY, 'Military'),
    #     (CLAN, 'Clan'),
    #
    #     (OTHER, 'Other'),
    # ]
    # org_type = models.IntegerField(choices=ORG_TYPE_CHOICES)

    god_followed = models.ForeignKey(
        'people.God',
        on_delete=models.SET_NULL,
        related_name='follower_orgs',
        null=True,
    )


class Population(NamedModel):

    description = models.TextField(null=True)
    member_count = models.IntegerField(
        help_text='Including unnamed members not in the database.',
        null=True,
    )
    sub_population_of = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='sub_populations',
        null=True
    )


class God(NamedModel):

    description = models.TextField(null=True)
    gender = models.IntegerField(choices=Person.GENDER_CHOICES)
    patron_of = models.CharField(max_length=255, null=True)

    # todo: install django-multiselectfield and switch cleric domains to this
    cleric_domains = models.CharField(max_length=255, null=True)

    follower_populations = models.ManyToManyField(
        'people.Population',
        related_name='gods_followed',
    )

    def get_absolute_url(self):
        return reverse('gods-update', kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('gods-add')
