import rules

from base.rules import is_owner


rules.add_perm('places.change_place', is_owner)
rules.add_perm('places.delete_place', is_owner)
