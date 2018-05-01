from collections import deque
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from shapely.geometry import Point, LineString, Polygon

from places.models import Place
from .serializers import PlaceSerializer


class PlaceList(APIView):

    def get(self, request, format=None):
        polygons = topo_sort_shapes(Place.objects.filter(_dimensions=2))
        other_shapes = list(Place.objects.filter(_dimensions__lt=2))
        places = polygons + other_shapes
        serializer = PlaceSerializer(places, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        coords = [(datum['x'], datum['y']) for datum in request.data['points']]
        dimensions = request.data['dimensions']
        place = Place()
        if dimensions == 0:
            try:
                shape = Point(coords)
            except ValueError:
                return Response({
                    'points': {
                        'errors': 'Points cannot have more than one coordinate pair.'
                    }}, HTTP_400_BAD_REQUEST)
        elif dimensions == 1:
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
        place.save()
        return Response({}, HTTP_201_CREATED)


def topo_sort_shapes(places) -> list:
    # construct dependency graph
    graph = {place.id: [] for place in places}
    index = {place.id: place for place in places}
    for place in places:
        for other_place in places:
            if place is not other_place and place.shape.within(other_place.shape):
                graph[other_place.id].append(place.id)

    # topological sort
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = 0
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == 0:
                raise ValueError("cycle")
            if sk == 1:
                continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = 1

    while enter:
        dfs(enter.pop())

    return [index[pk] for pk in order]
