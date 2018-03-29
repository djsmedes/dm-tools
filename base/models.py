from django.db import models

# Create your models here.
from django.urls import reverse


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