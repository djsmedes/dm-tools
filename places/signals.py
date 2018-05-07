from django.db.models.signals import post_save

from places.models import Place, PlacePair


def create_place_pairs(sender, instance: Place, **kwargs):
    # todo: change this queryset to filter so that only places that SHOULD have a relationship get one
    other_instances = Place.objects.all()

    for other_instance in other_instances:
        if instance is other_instance:
            continue
        min_distance = instance.shape.distance(other_instance.shape)
        PlacePair.objects.create(
            place1=instance,
            place2=other_instance,
            min_distance=min_distance
        )


post_save.connect(create_place_pairs, Place)
