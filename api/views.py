from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_202_ACCEPTED
from shapely.geometry import Point, LineString, Polygon
from django.http import Http404

from places.models import Place
from places.utils import topological_sort_shapes
from .serializers import PlaceSerializer, PlaceInfoSerializer


class PlaceInfo(APIView):

    def get(self, request, pk, format=None):
        place = Place.objects.get(id=pk)
        serializer = PlaceInfoSerializer(place)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        try:
            place = Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404
        serializer = PlaceInfoSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            place = Place.objects.get(pk=pk)
        except Place.DoesNotExist:
            raise Http404
        place.delete()
        return Response({}, status=HTTP_202_ACCEPTED)


class PlaceList(APIView):

    def get(self, request, format=None):
        polygons = topological_sort_shapes(Place.objects.filter(_dimensions=2))
        other_shapes = list(Place.objects.filter(_dimensions__lt=2))
        places = polygons + other_shapes
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        coords = [(datum['x'], datum['y']) for datum in request.data['points']]
        type = int(request.data['type'])
        place = Place()
        if type < 100:
            try:
                shape = Point(coords)
            except ValueError:
                return Response({
                    'points': {
                        'errors': 'Points cannot have more than one coordinate pair.'
                    }}, HTTP_400_BAD_REQUEST)
        elif type < 200:
            try:
                shape = LineString(coords)
            except ValueError:
                return Response({
                    'points': {
                        'errors': 'Lines must have at least two coordinate pairs.'
                    }}, HTTP_400_BAD_REQUEST)
        else:  # dimensions == 2
            try:
                shape = Polygon(coords)
            except ValueError:
                return Response({
                    'points': {
                        'errors': 'Polygons must have at least three coordinate pairs.'
                    }}, HTTP_400_BAD_REQUEST)
        place.shape = shape
        place.type = type
        place.save()
        return Response({}, HTTP_201_CREATED)
