from django.db import models

from .base import Feature


class GeoFeature(Feature):
    pass


class Landmass(GeoFeature):
    pass


class MountainRange(GeoFeature):
    pass


class Mountain(GeoFeature):
    pass
