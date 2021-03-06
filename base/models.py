from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    cur_campaign = models.ForeignKey('base.Campaign', on_delete=models.SET_NULL, related_name='cur_campaign_of',
                                     null=True, blank=True)

    def __str__(self):
        return self.user.__str__()


class BaseModelManager(models.Manager):

    def get_qs_prod(self):
        return super().get_queryset()

    def owned_by(self, owner):
        return super().get_queryset().filter(owner=owner)

    def requester_owns(self, request):
        if request.user.is_authenticated:
            return self.owned_by(owner=request.user.profile)
        else:
            return self.none()

    def request_can_access(self, request):
        if request.user.is_authenticated:
            # if request.user.has_perm()
            return self.requester_owns(request)
        else:
            # todo - figure out how to check if an object requires no permission to view
            return self.none()


class BaseModel(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        'base.Profile',
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_owned_set"
    )
    objects = BaseModelManager()

    def __str__(self):
        return self.name

    def meta(self):
        return self._meta

    class Meta:
        abstract = True
        ordering = ['name']

    @classmethod
    def url_prefix(cls):
        return cls._meta.verbose_name.replace(' ', '')

    @classmethod
    def class_slug(cls) -> str:
        return slugify(cls._meta.verbose_name_plural)

    def get_absolute_url(self):
        return reverse('{}-view'.format(self.url_prefix()), kwargs={'pk': self.pk})

    @classmethod
    def get_create_url(cls):
        return reverse('{}-add'.format(cls.url_prefix()))

    def get_edit_url(self):
        return reverse('{}-edit'.format(self.url_prefix()), kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('{}-delete'.format(self.url_prefix()), kwargs={'pk': self.pk})

    @classmethod
    def login_protected_field_names(cls) -> list:
        return []

    @classmethod
    def api_url(cls) -> str:
        return 'api/{}/'.format(cls.class_slug())


class TableMetaData(models.Model):
    which_table = models.CharField(max_length=255, primary_key=True)
    last_updated = models.DateTimeField(null=True, blank=True)


class DmScreenTab(BaseModel):
    name = models.CharField(max_length=50, verbose_name='tab title')
    sort_order = models.IntegerField(default=0)
    tab_contents = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['sort_order']


class DmScreenTabForm(ModelForm):
    class Meta:
        model = DmScreenTab
        fields = '__all__'


class Campaign(BaseModel):
    dm = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='campaigns')
    current_location = models.ForeignKey('places.Place', on_delete=models.SET_NULL, null=True, blank=True)
    place_inclusion_distance = models.FloatField(default=0, blank=True)
