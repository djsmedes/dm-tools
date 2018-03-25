from django.db import models

from .base import Feature


class PoliticalFeature(Feature):
    pass


class World(PoliticalFeature):
    pass


class Nation(PoliticalFeature):
    pass


class Settlement(PoliticalFeature):

    METROPOLIS = 'ME'
    CITY = 'CI'
    TOWN = 'TO'
    VILLAGE = 'VI'

    SIZE_CLASS_CHOICES = [
        (METROPOLIS, 'Metropolis'),
        (CITY, 'City'),
        (TOWN, 'Town'),
        (VILLAGE, 'Village')
    ]

    size_class = models.CharField(max_length=2, choices=SIZE_CLASS_CHOICES)
