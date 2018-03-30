from django.urls import reverse_lazy

from .models import Monster, MonsterForm

from base.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseDetailView


class MonsterList(BaseListView):
    model = Monster
    table_headers = [
        'Name',
    ]
    table_data_accessors = [
        'name',
    ]


class MonsterAdd(BaseCreateView):
    model = Monster
    template_name = 'statblocks/monster_form.html'
    form_class = MonsterForm
    extra_context = {
        'multiselect_field_names': [
            'damage_vulnerabilities',
            'damage_resistances',
            'damage_immunities',
            'condition_immunities',
            'languages',
        ]
    }


class MonsterEdit(BaseUpdateView):
    model = Monster
    template_name = 'statblocks/monster_form.html'
    form_class = MonsterForm


class MonsterDelete(BaseDeleteView):
    model = Monster
    success_url = reverse_lazy('monsters-home')


class MonsterDetail(BaseDetailView):
    model = Monster
    template_name = 'statblocks/monster_detail.html'
