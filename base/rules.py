import rules


@rules.predicate
def is_owner(user, obj):
    return user.profile == obj.owner


rules.add_perm('base.change_campaign', is_owner)
rules.add_perm('base.delete_campaign', is_owner)
