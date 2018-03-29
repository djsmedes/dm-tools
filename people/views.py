from django.urls import reverse_lazy

from base.views import BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView, \
    BaseDetailView
from .models import God, GodForm, Person, PersonForm, Population, PopulationForm


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


class PopulationList(BaseListView):
    model = Population
    table_headers = [
        'Name',
        'Subpopulation of',
    ]
    table_data_accessors = [
        'name',
        'sub_population_of',
    ]


class GodAdd(BaseCreateView):
    model = God
    form_class = GodForm


class PersonAdd(BaseCreateView):
    model = Person
    form_class = PersonForm


class PopulationAdd(BaseCreateView):
    model = Population
    form_class = PopulationForm


class GodEdit(BaseUpdateView):
    model = God
    form_class = GodForm


class PersonEdit(BaseUpdateView):
    model = Person
    form_class = PersonForm


class PopulationEdit(BaseUpdateView):
    model = Population
    form_class = PopulationForm


class GodDelete(BaseDeleteView):
    model = God
    success_url = reverse_lazy('gods-home')


class PersonDelete(BaseDeleteView):
    model = Person
    success_url = reverse_lazy('npcs-home')


class PopulationDelete(BaseDeleteView):
    model = Population
    success_url = reverse_lazy('populations-home')


class GodDetail(BaseDetailView):
    model = God
    form_class = GodForm


class PersonDetail(BaseDetailView):
    model = Person
    form_class = PersonForm


class PopulationDetail(BaseDetailView):
    model = Population
    form_class = PopulationForm
