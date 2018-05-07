from django.db.models.signals import post_save

from places.models import Place, PlacePair


def create_place_pairs(sender, instance: Place, **kwargs):
    # todo: change this queryset to filter so that only places that SHOULD have a relationship get one
    other_places = Place.objects.all()

    for other_place in other_places:
        if instance is other_place:
            continue
        min_distance = instance.shape.distance(other_place.shape)
        PlacePair.objects.create(
            place1=instance,
            place2=other_place,
            min_distance=min_distance
        )


post_save.connect(create_place_pairs, Place)
