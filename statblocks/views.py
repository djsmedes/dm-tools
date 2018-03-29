from .models import Monster

from base.views import BaseListView


class MonsterList(BaseListView):
    model = Monster
    table_headers = [
        'Name',
    ]
    table_data_accessors = [
        'name',
    ]
