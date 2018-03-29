from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import ContextMixin
from django.urls import reverse_lazy

# importing this to be used in an exec in a lambda expression
# noinspection PyUnresolvedReferences
from django.http import Http404

from .models import God, GodForm, Person, PersonForm, Population, PopulationForm


class BreadCrumbMixin(ContextMixin):

    extra_breadcrumbs = []

    def get_extra_breadcrumbs(self):
        return self.extra_breadcrumbs

    def get_breadcrumbs(self):
        if hasattr(self, 'kwargs') and self.kwargs.get('base_breadcrumbs'):
            return self.kwargs['base_breadcrumbs'] + self.get_extra_breadcrumbs()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = self.get_breadcrumbs()
        return context


class PeopleListView(BreadCrumbMixin, ListView):
    template_name = 'base/_table.html'
    table_headers = []
    table_data_accessors = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['table_headers'] = self.table_headers
        context['table_data_accessors'] = self.table_data_accessors
        return context


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


class PeopleCreateView(BreadCrumbMixin, CreateView):
    extra_breadcrumbs = [{'text': 'Add'}]
    template_name = 'base/_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = '{}-add'.format(self.model._meta.verbose_name)
        context['model'] = self.model
        return context


class GodAdd(PeopleCreateView):
    model = God
    form_class = GodForm


class PersonAdd(PeopleCreateView):
    model = Person
    form_class = PersonForm


class PopulationAdd(PeopleCreateView):
    model = Population
    form_class = PopulationForm


class PeopleUpdateView(BreadCrumbMixin, UpdateView):
    template_name = 'base/_form.html'

    def get_extra_breadcrumbs(self):
        return [
            {
                'text': self.object.name,
                'href': reverse_lazy(
                    '{}-view'.format(self.model._meta.verbose_name),
                    kwargs={'pk': self.object.pk}
                ),
            },
            {'text': 'Edit'}
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = '{}-edit'.format(self.model._meta.verbose_name)
        context['form'] = self.form_class(instance=self.object)
        return context


class GodEdit(PeopleUpdateView):
    model = God
    form_class = GodForm


class PersonEdit(PeopleUpdateView):
    model = Person
    form_class = PersonForm


class PopulationEdit(PeopleUpdateView):
    model = Population
    form_class = PopulationForm


class PeopleDeleteView(BreadCrumbMixin, DeleteView):
    template_name = 'base/_confirm_delete.html'

    def get_extra_breadcrumbs(self):
        return [
            {
                'text': self.object.name,
                'href': reverse_lazy(
                    '{}-view'.format(self.model._meta.verbose_name),
                    kwargs={'pk': self.object.pk})
            },
            {'text': 'Delete'}
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GodDelete(PeopleDeleteView):
    model = God
    success_url = reverse_lazy('gods-home')


class PersonDelete(PeopleDeleteView):
    model = Person
    success_url = reverse_lazy('npcs-home')


class PopulationDelete(PeopleDeleteView):
    model = Population
    success_url = reverse_lazy('populations-home')


class PeopleDetailView(BreadCrumbMixin, DetailView):
    template_name = 'base/_detail.html'
    form_class = lambda instance: exec('raise Http404')

    def get_extra_breadcrumbs(self):
        return [{'text': self.object.name}]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context


class GodDetail(PeopleDetailView):
    model = God
    form_class = GodForm


class PersonDetail(PeopleDetailView):
    model = Person
    form_class = PersonForm


class PopulationDetail(PeopleDetailView):
    model = Population
    form_class = PopulationForm
