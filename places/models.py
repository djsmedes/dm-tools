from shapely.wkb import loads as wkb_loads
from shapely.geometry import Point
from django.db import models

from base.models import BaseModel


class Place(BaseModel):

    _shape = models.BinaryField(db_column='shape', null=True, blank=True)

    @property
    def shape(self):
        return wkb_loads(bytes(self.test))

    @shape.setter
    def shape(self, shape):
        self.test = shape.wkb