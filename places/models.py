from typing import Type
from shapely.wkb import loads as wkb_loads
from shapely.geometry.base import BaseGeometry
from shapely.geometry import Point, LineString, LinearRing, Polygon
from django.db import models

from base.models import BaseModel


class Place(BaseModel):

    POINT = 0
    LINE = 1
    POLYGON = 2
    DIMENSIONS_CHOICES = [
        (POINT, 'point'),
        (LINE, 'line'),
        (POLYGON, 'polygon')
    ]

    _shape = models.BinaryField(db_column='shape', null=True, blank=True)
    _dimensions = models.IntegerField(db_column='dimensions', choices=DIMENSIONS_CHOICES, null=True, blank=True)
    _shapely_object = None

    class Meta:
        ordering = ['-_dimensions']

    @property
    def shape(self):
        if self._shape is None:
            return None
        if self._shapely_object is None:
            self._shapely_object = wkb_loads(bytes(self._shape))
        return self._shapely_object

    @shape.setter
    def shape(self, shape: Type[BaseGeometry]):
        self._shapely_object = shape
        if shape is None:
            self._shape = None
        else:
            self._shape = shape.wkb
        self._dimensions = self.dimensions

    @property
    def dimensions(self):
        if isinstance(self.shape, Point):
            return self.POINT  # 0
        elif isinstance(self.shape, LineString):
            return self.LINE  # 1
        elif isinstance(self.shape, Polygon):
            return self.POLYGON  # 2
        else:
            return None

    @property
    def points(self):
        dim = self.dimensions
        if dim < 2:
            # points or lines use attr .coords directly
            pts = list(self.shape.coords)
        else:
            # it's a polygon, which you have to get the exterior attr of first
            # and also it lists start and end point as the same point, so slice that sucker off
            pts = self.shape.exterior.coords[:-1]
        return [{'x': int(pt[0]), 'y': int(pt[1])} for pt in pts]

    @property
    def pointstring(self):
        pointstring = ''
        for pt in self.points:
            pointstring += '{x},{y} '.format(x=pt['x'], y=pt['y'])
        return pointstring

    def __lt__(self, other):
        return self.shape.within(other.shape)

    def __repr__(self):
        return str(self.id)
