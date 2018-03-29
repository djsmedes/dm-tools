from django.db import models
from django.forms import ModelForm, ModelMultipleChoiceField
from django.shortcuts import reverse


class BaseModel(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def meta(self):
        return self._meta

    class Meta:
        abstract = True
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('{}-view'.format(self._meta.verbose_name), kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('{}-add'.format(self._meta.verbose_name))

    def get_delete_url(self):
        return reverse('{}-delete'.format(self._meta.verbose_name), kwargs={'pk': self.pk})


class Person(BaseModel):

    description = models.TextField(null=True, blank=True)
    race = models.ForeignKey(
        'people.Population',
        on_delete=models.SET_NULL,
        related_name='members_of_race',
        null=True,
        blank=True,
    )
    organizations_in = models.ManyToManyField(
        'people.Organization',
        related_name='members',
        blank=True,
    )
    populations_in = models.ManyToManyField(
        'people.Population',
        related_name='members',
        blank=True,
    )

    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    ]
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True, blank=True)

    class Meta:
        verbose_name = 'npc'
        verbose_name_plural = 'npcs'


class Organization(BaseModel):

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


class Population(BaseModel):

    description = models.TextField(null=True, blank=True)
    member_count = models.IntegerField(
        help_text='Including unnamed members not in the database.',
        null=True,
        blank=True,
    )
    sub_population_of = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='sub_populations',
        null=True,
        blank=True,
    )


class God(BaseModel):

    description = models.TextField(null=True, blank=True)
    gender = models.IntegerField(choices=Person.GENDER_CHOICES, null=True, blank=True)
    patron_of = models.CharField(max_length=255, null=True, blank=True)

    # todo: install django-multiselectfield and switch cleric domains to this
    cleric_domains = models.CharField(max_length=255, null=True, blank=True)

    follower_populations = models.ManyToManyField(
        'people.Population',
        related_name='gods_followed',
        blank=True
    )


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class PopulationForm(ModelForm):
    class Meta:
        model = Population
        fields = '__all__'


class GodForm(ModelForm):
    class Meta:
        model = God
        fields = '__all__'

    # ModelMultipleChoiceField for a field defined on another model and auto generated
    # https://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields
    follower_orgs = ModelMultipleChoiceField(
        queryset=Organization.objects.all(),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        follower_orgs_query = models.Q(god_followed__isnull=True)
        if kwargs.get('instance'):
            initial = kwargs.setdefault('initial', {})
            initial['follower_orgs'] = [o.pk for o in kwargs['instance'].follower_orgs.all()]
            follower_orgs_query |= models.Q(god_followed=kwargs['instance'])
        super(GodForm, self).__init__(*args, **kwargs)
        self.fields['follower_orgs'].queryset = Organization.objects.filter(follower_orgs_query)

    def save(self, commit=True):
        instance = ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.follower_orgs.clear()
            for org in self.cleaned_data['follower_orgs']:
                instance.follower_orgs.add(org)
        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance
