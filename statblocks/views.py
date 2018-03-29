from .models import Monster

from base.views import PeopleListView


class MonsterList(PeopleListView):
    model = Monster
    table_headers = [
        'Name',
    ]
    table_data_accessors = [
        'name',
    ]
