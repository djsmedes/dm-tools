from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Monster, MonsterForm

from base.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseDetailView


class MonsterList(LoginRequiredMixin, BaseListView):
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


class MonsterEdit(BaseUpdateView):
    model = Monster
    template_name = 'statblocks/monster_form.html'
    form_class = MonsterForm


class MonsterDelete(BaseDeleteView):
    model = Monster
    success_url = reverse_lazy('monsters-home')


class MonsterDetail(LoginRequiredMixin, BaseDetailView):
    model = Monster
    template_name = 'statblocks/monster_detail.html'
