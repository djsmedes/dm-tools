from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.urls import reverse
from multiselectfield import MultiSelectField


class BaseModel(models.Model):

    name = models.CharField(max_length=255)

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

    def get_absolute_url(self):
        return reverse('{}-view'.format(self.url_prefix()), kwargs={'pk': self.pk})

    @classmethod
    def get_create_url(cls):
        return reverse('{}-add'.format(cls.url_prefix()))

    def get_edit_url(self):
        return reverse('{}-edit'.format(self.url_prefix()), kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('{}-delete'.format(self.url_prefix()), kwargs={'pk': self.pk})

    @property
    def multiselect_field_names(self):
        return [field.name for field in self._meta.fields if isinstance(field, MultiSelectField)]

    @classmethod
    def login_protected_field_names(cls) -> list:
        return []


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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')


class Campaign(BaseModel):
    dm = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='campaigns')
