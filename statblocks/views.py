from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Monster, MonsterForm, SpecialProperty, SpecialPropertyForm, Action, ActionForm

from base.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseDetailView


class MonsterList(LoginRequiredMixin, BaseListView):
    model = Monster


class SpecialPropertyList(LoginRequiredMixin, BaseListView):
    model = SpecialProperty


class ActionList(LoginRequiredMixin, BaseListView):
    model = Action


class MonsterAdd(BaseCreateView):
    model = Monster
    template_name = 'statblocks/monster_form.html'
    form_class = MonsterForm


class SpecialPropertyAdd(BaseCreateView):
    model = SpecialProperty
    form_class = SpecialPropertyForm


class ActionAdd(BaseCreateView):
    model = Action
    form_class = ActionForm
    template_name = 'statblocks/action_form.html'


class MonsterEdit(BaseUpdateView):
    model = Monster
    template_name = 'statblocks/monster_form.html'
    form_class = MonsterForm


class SpecialPropertyEdit(BaseUpdateView):
    model = SpecialProperty
    form_class = SpecialPropertyForm


class MonsterDelete(BaseDeleteView):
    model = Monster
    success_url = reverse_lazy('monsters-home')


class SpecialPropertyDelete(BaseDeleteView):
    model = SpecialProperty
    success_url = reverse_lazy('specialproperties-home')


class MonsterDetail(LoginRequiredMixin, BaseDetailView):
    model = Monster
    template_name = 'statblocks/monster_detail.html'


class SpecialPropertyDetail(LoginRequiredMixin, BaseDetailView):
    model = SpecialProperty
    template_name = 'statblocks/specialproperty_detail.html'
