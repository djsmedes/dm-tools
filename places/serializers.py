from rest_framework import serializers

from places.models import Place


class PointSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()


class PlaceLiteSerializer(serializers.ModelSerializer):
    """A lighter-weight serializer appropriate for getting lists of Places"""
    points = PointSerializer(many=True)

    class Meta:
        model = Place
        fields = ('id', 'name', 'owner', 'type', 'points')

    def create(self, validated_data):
        # needs type first so that it knows what Shapely shape to create with the points
        p = Place(type=validated_data['type'])
        return self.update(p, validated_data)

    def update(self, instance, validated_data):
        for field in self.Meta.fields:
            field_default_data = getattr(instance, field) if hasattr(instance, field) else None
            field_data = validated_data.get(field, field_default_data)
            setattr(instance, field, field_data)
        instance.save()
        return instance


class PlaceSerializer(PlaceLiteSerializer):
    """A serializer for everything you need for a Place
    Note: because we are just looping over fields for update(),
      it's not necessarily guaranteed that 'type' will come before 'points'.
      Therefore this serializer assumes that Places cannot change between
      types of different dimension (Point vs Line vs Polygon)"""

    nearby_places = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ('id', 'name', 'owner', 'description', 'type', 'points', 'nearby_places')

    def get_nearby_places(self, obj: Place):
        places = obj.get_nearby_places(float(self.context.get('inclusion_distance', 0)))
        return PlaceLiteSerializer(places, many=True).data
