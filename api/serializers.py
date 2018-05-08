from rest_framework import serializers

from places.models import Place


class PointSerializer(serializers.Serializer):
    x = serializers.FloatField()
    y = serializers.FloatField()


class PlaceSerializer(serializers.Serializer):
    # todo - convert to ModelSerializer
    id = serializers.IntegerField(read_only=True)
    points = PointSerializer(many=True)
    type = serializers.IntegerField()


class PlaceInfoSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True)
    nearby_places = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ('id', 'name', 'description', 'type', 'points', 'nearby_places')

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.points = validated_data.get('points', instance.points)
        instance.save()
        return instance

    def get_nearby_places(self, obj: Place):
        places = obj.get_nearby_places(float(self.context.get('inclusion_distance', 0)))
        return [{
            'name': place.name,
            'id': place.id,
            'type': place.type,
        } for place in places]
