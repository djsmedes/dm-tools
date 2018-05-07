from rules import predicate, add_perm


@predicate
def is_owner(user, obj):
    # assert isinstance(user, User)
    # assert hasattr(obj, 'owner')
    print(user, user.profile, obj, obj.owner)
    return user.profile == obj.owner


add_perm('base.change_campaign', is_owner)
add_perm('places.change_place', is_owner)
