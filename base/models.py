from django.db import models

# Create your models here.
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

    def get_absolute_url(self):
        return reverse('{}-view'.format(self._meta.verbose_name), kwargs={'pk': self.pk})

    def get_create_url(self):
        return reverse('{}-add'.format(self._meta.verbose_name))

    def get_edit_url(self):
        return reverse('{}-edit'.format(self._meta.verbose_name), kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('{}-delete'.format(self._meta.verbose_name), kwargs={'pk': self.pk})

    @property
    def multiselect_field_names(self):
        return [field.name for field in self._meta.fields if isinstance(field, MultiSelectField)]

    @classmethod
    def login_protected_field_names(cls) -> list:
        return []


class TableMetaData(models.Model):

    which_table = models.CharField(max_length=255, primary_key=True)
    last_updated = models.DateTimeField(null=True, blank=True)
