from rest_framework.views import APIView
from rest_framework.response import Response
from shapely.geometry import Point, LineString, Polygon

from places.models import Place
from .serializers import PlaceSerializer


class PlaceList(APIView):

    def get(self, request, format=None):
        places = Place.objects.all()
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        coords = [(datum['x'], datum['y']) for datum in request.data['points']]
        dimensions = request.data['dimensions']
        place = Place()
        if dimensions == 0:
            shape = Point(coords)
        elif dimensions == 1:
            shape = LineString(coords)
        else:  # dimensions == 2
            shape = Polygon(coords)
        place.shape = shape
        place.save()
        return Response({})
