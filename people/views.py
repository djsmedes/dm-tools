from dal import autocomplete
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from base.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, \
    BaseDetailView, BreadCrumbMixin
from .models import God, GodForm, \
    Person, PersonForm, \
    Race, RaceForm, \
    Combatant, CombatantForm
from statblocks.models import Monster


class GodList(BaseListView):
    model = God
    table_headers = [
        'Name',
        'Patron of',
    ]
    table_data_accessors = [
        'name',
        'patron_of',
    ]


class PersonList(BaseListView):
    model = Person
    table_headers = [
        'Name',
    ]
    table_data_accessors = [
        'name',
    ]


class RaceList(BaseListView):
    model = Race
    table_headers = [
        'Name',
        'Subrace of',
    ]
    table_data_accessors = [
        'name',
        'parent_race',
    ]


class GodAdd(BaseCreateView):
    model = God
    form_class = GodForm


class PersonAdd(BaseCreateView):
    model = Person
    form_class = PersonForm


class RaceAdd(BaseCreateView):
    model = Race
    form_class = RaceForm


class CombatantAdd(BaseCreateView):
    model = Combatant
    form_class = CombatantForm
    extra_breadcrumbs = [{'text': 'Add combatant'}]


class GodEdit(BaseUpdateView):
    model = God
    form_class = GodForm


class PersonEdit(BaseUpdateView):
    model = Person
    form_class = PersonForm


class RaceEdit(BaseUpdateView):
    model = Race
    form_class = RaceForm


class CombatantEdit(BreadCrumbMixin, UpdateView):
    model = Combatant
    form_class = CombatantForm
    # template_name = 'people/combatant_form.html'

    def get_extra_breadcrumbs(self):
        return [{'text': 'Edit {}'.format(self.object.name)}]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = '{}-edit'.format(self.model.url_prefix())
        return context


class GodDelete(BaseDeleteView):
    model = God
    success_url = reverse_lazy('gods-home')


class PersonDelete(BaseDeleteView):
    model = Person
    success_url = reverse_lazy('npcs-home')


class RaceDelete(BaseDeleteView):
    model = Race
    success_url = reverse_lazy('races-home')


class CombatantDelete(BaseDeleteView):
    model = Combatant
    success_url = reverse_lazy('home')

    def get_extra_breadcrumbs(self):
        return [{'text': 'Delete {}'.format(self.object.name)}]


class GodDetail(BaseDetailView):
    model = God
    form_class = GodForm


class PersonDetail(BaseDetailView):
    model = Person
    form_class = PersonForm


class RaceDetail(BaseDetailView):
    model = Race
    form_class = RaceForm
