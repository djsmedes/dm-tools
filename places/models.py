from typing import Type
from shapely.wkb import loads as wkb_loads
from shapely.geometry.base import BaseGeometry
from django.db import models

from base.models import BaseModel


class Place(BaseModel):

    _shape = models.BinaryField(db_column='shape', null=True, blank=True)

    @property
    def shape(self):
        return wkb_loads(bytes(self.test))

    @shape.setter
    def shape(self, shape: Type[BaseGeometry]):
        self.test = shape.wkb
