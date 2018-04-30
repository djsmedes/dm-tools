from typing import Type
from shapely.wkb import loads as wkb_loads
from shapely.geometry.base import BaseGeometry
from shapely.geometry import Point, LineString, LinearRing, Polygon
from django.db import models

from base.models import BaseModel


class Place(BaseModel):

    _shape = models.BinaryField(db_column='shape', null=True, blank=True)

    @property
    def shape(self):
        return wkb_loads(bytes(self._shape))

    @shape.setter
    def shape(self, shape: Type[BaseGeometry]):
        self._shape = shape.wkb

    @property
    def shape_type(self):
        if isinstance(self.shape, Point):
            return 'point'
        elif isinstance(self.shape, Polygon):
            return 'polygon'
        else:
            return 'line'

    @property
    def points(self):
        pointstring = ''
        if isinstance(self.shape, Polygon):
            points = list(self.shape.exterior.coords)[:-1]
            for x, y in points:
                pointstring += '{},{} '.format(int(x), int(y))
        return pointstring
