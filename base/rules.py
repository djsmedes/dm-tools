from rules import predicate, add_perm


@predicate
def is_owner(user, obj):
    # assert isinstance(user, User)
    # assert hasattr(obj, 'owner')
    return user.profile is obj.owner


add_perm('places.add_place', is_owner)
