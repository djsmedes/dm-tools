from dal import autocomplete
from django.db import models
from django.forms import ModelForm, ModelMultipleChoiceField

from multiselectfield import MultiSelectField

from base.models import BaseModel
from base.utils import update_last_updated, BootstrapColor
from statblocks.models import Monster


class Person(BaseModel):

    description = models.TextField(null=True, blank=True)
    race = models.ForeignKey(
        'people.Race',
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


class Race(BaseModel):

    description = models.TextField(null=True, blank=True)
    subrace_of = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='subraces',
        null=True,
        blank=True,
    )

    @property
    def parent_race(self):
        return self.subrace_of if self.subrace_of else ''


class God(BaseModel):

    description = models.TextField(null=True, blank=True)
    gender = models.IntegerField(choices=Person.GENDER_CHOICES, null=True, blank=True)
    patron_of = models.CharField(max_length=255, null=True, blank=True)

    # todo: install django-multiselectfield and switch cleric domains to this
    cleric_domains = models.CharField(max_length=255, null=True, blank=True)

    follower_races = models.ManyToManyField(
        'people.Race',
        related_name='gods_followed',
        blank=True
    )


class Combatant(BaseModel):

    class Meta:
        ordering = ['-initiative']

    color = models.CharField(max_length=7, choices=BootstrapColor.MODEL_CHOICES, null=True, blank=True)
    initiative = models.IntegerField(null=True, blank=True)
    buffs = MultiSelectField(null=True, blank=True)
    debuffs = MultiSelectField(null=True, blank=True)
    other_effects = MultiSelectField(null=True, blank=True)
    statblock = models.ForeignKey(
        'statblocks.Monster',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return '/'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_last_updated(self)

    def delete(self, using=None, keep_parents=False):
        super().delete(using=using, keep_parents=keep_parents)
        update_last_updated(self)

    @classmethod
    def login_protected_field_names(cls):
        return ['statblock']


class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'


class RaceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subrace_of'].queryset = Race.objects.filter(subrace_of__isnull=True)

    class Meta:
        model = Race
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


class CombatantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color_field = self.fields.get('color')
        if color_field:
            color_field.choices = color_field.choices[1:]

    class Meta:
        model = Combatant
        fields = ['name', 'color', 'initiative', 'statblock']
        widgets = {
            'statblock': autocomplete.ModelSelect2(url='monster-autocomplete'),
        }
