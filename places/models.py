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
    def dimensions(self):
        if isinstance(self.shape, Point):
            return 0
        elif isinstance(self.shape, Polygon):
            return 2
        else:
            return 1

    @property
    def points(self):
        dim = self.dimensions
        if dim == 0:
            # do something appropriate for a point
            pass
        elif dim == 1:
            # do something appropriate for a line
            pass
        else:
            # it's a polygon
            pts = list(self.shape.exterior.coords)[:-1]
            return [{'x': pt[0], 'y': pt[1]} for pt in pts]

    @property
    def pointstring(self):
        pointstring = ''
        for pt in self.points:
            pointstring += '{},{} '.format(int(pt['x']), int(pt['y']))
        return pointstring
