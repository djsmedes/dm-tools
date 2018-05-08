from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from places.models import Place
from places.utils import topological_sort_shapes
from .serializers import PlaceSerializer, PlaceLiteSerializer


class PlaceList(APIView):
    """Get a list of Places or create a new one"""
    def get(self, request, format=None):
        # todo add ability to get other owners stuff somehow for non-logged-in users
        owner = request.user.profile
        polygons = topological_sort_shapes(
            Place.objects.filter(_dimensions=2).filter(owner=owner)
        )
        places = polygons + list(
            Place.objects.filter(_dimensions__lt=2).filter(owner=owner)
        )
        serializer = PlaceLiteSerializer(places, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        if not request.user.has_perm('places.add_place'):
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        data = {k: v for k, v in request.data.items()}
        data['owner'] = request.user.profile.pk
        serializer = PlaceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlaceDetail(APIView):
    """Retrieve, update, or delete an existing Place"""
    def get(self, request, pk, format=None):
        try:
            place = Place.objects.get(id=pk, owner=request.user.profile)
        except Place.DoesNotExist:
            return Response({}, status.HTTP_404_NOT_FOUND)
        serializer = PlaceSerializer(place, context={
            'inclusion_distance': request.query_params.get('inclusion_distance', 0)
        })
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        try:
            place = Place.objects.get(pk=pk, owner=request.user.profile)
        except Place.DoesNotExist:
            return Response({}, status.HTTP_404_NOT_FOUND)
        if not request.user.has_perm('places.change_place', place):
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        serializer = PlaceSerializer(place, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            place = Place.objects.get(pk=pk, owner=request.user.profile)
        except Place.DoesNotExist:
            return Response({}, status.HTTP_404_NOT_FOUND)
        if not request.user.has_perm('places.delete_place', place):
            return Response({}, status=status.HTTP_403_FORBIDDEN)
        place.delete()
        return Response({}, status=status.HTTP_202_ACCEPTED)
