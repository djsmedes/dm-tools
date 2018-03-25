from django.db import models

from .base import Feature


class WaterFeature(Feature):
    pass


class Ocean(WaterFeature):
    pass


class Lake(WaterFeature):
    pass


class River(WaterFeature):

    source = models.CharField(max_length=255)
    terminus = models.CharField(max_length=255)
