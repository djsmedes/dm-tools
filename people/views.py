from django.urls import reverse_lazy

from base.views import PeopleListView, PeopleCreateView, PeopleUpdateView, PeopleDeleteView, \
    PeopleDetailView
from .models import God, GodForm, Person, PersonForm, Population, PopulationForm


class GodList(PeopleListView):
    model = God
    table_headers = [
        'Name',
        'Patron of',
    ]
    table_data_accessors = [
        'name',
        'patron_of',
    ]


class PersonList(PeopleListView):
    model = Person
    table_headers = [
        'Name',
    ]
    table_data_accessors = [
        'name',
    ]


class PopulationList(PeopleListView):
    model = Population
    table_headers = [
        'Name',
        'Subpopulation of',
    ]
    table_data_accessors = [
        'name',
        'sub_population_of',
    ]


class GodAdd(PeopleCreateView):
    model = God
    form_class = GodForm


class PersonAdd(PeopleCreateView):
    model = Person
    form_class = PersonForm


class PopulationAdd(PeopleCreateView):
    model = Population
    form_class = PopulationForm


class GodEdit(PeopleUpdateView):
    model = God
    form_class = GodForm


class PersonEdit(PeopleUpdateView):
    model = Person
    form_class = PersonForm


class PopulationEdit(PeopleUpdateView):
    model = Population
    form_class = PopulationForm


class GodDelete(PeopleDeleteView):
    model = God
    success_url = reverse_lazy('gods-home')


class PersonDelete(PeopleDeleteView):
    model = Person
    success_url = reverse_lazy('npcs-home')


class PopulationDelete(PeopleDeleteView):
    model = Population
    success_url = reverse_lazy('populations-home')


class GodDetail(PeopleDetailView):
    model = God
    form_class = GodForm


class PersonDetail(PeopleDetailView):
    model = Person
    form_class = PersonForm


class PopulationDetail(PeopleDetailView):
    model = Population
    form_class = PopulationForm
