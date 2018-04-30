from rest_framework import serializers

from places.models import Place


class PlaceSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.IntegerField(read_only=True)
    dimensions = serializers.CharField()
    points = serializers.OrderedDict()
