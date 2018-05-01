from rest_framework import serializers

from places.models import Place


class PointSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()


class PlaceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    dimensions = serializers.IntegerField()
    points = PointSerializer(many=True)
    type = serializers.IntegerField()
