from dal import autocomplete
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Monster, MonsterForm, \
    SpecialProperty, SpecialPropertyForm, \
    Action, ActionForm, \
    LegendaryAction, LegendaryActionForm, \
    Reaction, ReactionForm

from base.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, BaseDetailView


class MonsterList(LoginRequiredMixin, BaseListView):
    model = Monster


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


# Special Properties
class SpecialPropertyList(LoginRequiredMixin, BaseListView):
    model = SpecialProperty
    table_headers = [
        'Name', 'Save DC', 'Save targets', 'Monsters'
    ]
    table_data_accessors = [
        'name', 'save_dc', 'save_type', 'monsters_with'
    ]


class SpecialPropertyAdd(BaseCreateView):
    model = SpecialProperty
    form_class = SpecialPropertyForm


class SpecialPropertyEdit(BaseUpdateView):
    model = SpecialProperty
    form_class = SpecialPropertyForm


class SpecialPropertyDelete(BaseDeleteView):
    model = SpecialProperty
    success_url = reverse_lazy('specialproperties-home')


class SpecialPropertyDetail(LoginRequiredMixin, BaseDetailView):
    model = SpecialProperty
    template_name = 'statblocks/statblockbit_detail.html'


class SpecialPropertyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return SpecialProperty.objects.none()

        qs = SpecialProperty.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


# Actions
class ActionList(LoginRequiredMixin, BaseListView):
    model = Action
    table_headers = [
        'Name', 'Monsters'
    ]
    table_data_accessors = [
        'name', 'monsters_with'
    ]


class ActionAdd(BaseCreateView):
    model = Action
    form_class = ActionForm
    template_name = 'statblocks/action_form.html'


class ActionEdit(BaseUpdateView):
    model = Action
    form_class = ActionForm
    template_name = 'statblocks/action_form.html'


class ActionDelete(BaseDeleteView):
    model = Action
    success_url = reverse_lazy('actions-home')


class ActionDetail(LoginRequiredMixin, BaseDetailView):
    model = Action
    template_name = 'statblocks/action_detail.html'


class ActionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Action.objects.none()

        qs = Action.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


# Legendary Actions
class LegendaryActionList(LoginRequiredMixin, BaseListView):
    model = LegendaryAction
    table_headers = [
        'Name', 'Monsters'
    ]
    table_data_accessors = [
        'name', 'monsters_with'
    ]


class LegendaryActionAdd(BaseCreateView):
    model = LegendaryAction
    form_class = LegendaryActionForm


class LegendaryActionEdit(BaseUpdateView):
    model = LegendaryAction
    form_class = LegendaryActionForm


class LegendaryActionDelete(BaseDeleteView):
    model = LegendaryAction
    success_url = reverse_lazy('legendaryactions-home')


class LegendaryActionDetail(LoginRequiredMixin, BaseDetailView):
    model = LegendaryAction
    template_name = 'statblocks/statblockbit_detail.html'


class LegendaryActionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return LegendaryAction.objects.none()

        qs = LegendaryAction.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


# Reactions
class ReactionList(LoginRequiredMixin, BaseListView):
    model = Reaction
    table_headers = [
        'Name', 'Monsters'
    ]
    table_data_accessors = [
        'name', 'monsters_with'
    ]


class ReactionAdd(BaseCreateView):
    model = Reaction
    form_class = ReactionForm


class ReactionEdit(BaseUpdateView):
    model = Reaction
    form_class = ReactionForm


class ReactionDelete(BaseDeleteView):
    model = Reaction
    success_url = reverse_lazy('reactions-home')


class ReactionDetail(LoginRequiredMixin, BaseDetailView):
    model = Reaction
    template_name = 'statblocks/statblockbit_detail.html'


class ReactionAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Reaction.objects.none()

        qs = Reaction.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs
