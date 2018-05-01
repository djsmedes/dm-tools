from rest_framework import serializers

from places.models import Place


class PointSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()


class PlaceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    dimensions = serializers.CharField()
    points = PointSerializer(many=True)
    pointstring = serializers.CharField()
