from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.http import Http404

from .models import God, GodForm, Person, PersonForm, Population, PopulationForm


class PeopleHomeView(TemplateView):
    template_name = 'people/home.html'

    def get(self, *args, **kwargs):
        if kwargs.get('base_breadcrumbs'):
            self.base_breadcrumbs = kwargs['base_breadcrumbs']
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['god_model'] = God
        context['npc_model'] = Person
        context['god_list'] = God.objects.all()
        context['npc_list'] = Person.objects.all()
        if hasattr(self, 'base_breadcrumbs'):
            context['breadcrumbs'] = self.base_breadcrumbs
        return context


class PeopleListView(ListView):
    template_name = 'people/_table.html'
    extra_breadcrumbs = []
    table_headers = []
    table_data_accessors = []

    def get(self, *args, **kwargs):
        if kwargs.get('base_breadcrumbs'):
            self.base_breadcrumbs = kwargs['base_breadcrumbs']
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'base_breadcrumbs'):
            context['breadcrumbs'] = self.base_breadcrumbs + self.extra_breadcrumbs
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


class PeopleCreateView(CreateView):
    extra_breadcrumbs = [{'text': 'Add'}]
    template_name = 'people/_form.html'

    def get(self, *args, **kwargs):
        if kwargs.get('base_breadcrumbs'):
            self.base_breadcrumbs = kwargs['base_breadcrumbs']
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = '{}-add'.format(self.model._meta.verbose_name)
        if hasattr(self, 'base_breadcrumbs'):
            context['breadcrumbs'] = self.base_breadcrumbs + self.extra_breadcrumbs
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


class PeopleUpdateView(UpdateView):
    template_name = 'people/_form.html'

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
        if hasattr(self, 'base_breadcrumbs'):
            context['breadcrumbs'] = self.base_breadcrumbs + self.get_extra_breadcrumbs()
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


class PeopleDeleteView(DeleteView):
    template_name = 'people/_confirm_delete.html'

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
        context['breadcrumbs'] = context['base_breadcrumbs'] + self.get_extra_breadcrumbs()
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


class PeopleDetailView(DetailView):
    template_name = 'people/_detail.html'
    form_class = lambda instance: exec('raise Http404')

    def get_extra_breadcrumbs(self):
        return [{'text': self.object.name}]

    def get(self, *args, **kwargs):
        if kwargs.get('base_breadcrumbs'):
            self.base_breadcrumbs = kwargs['base_breadcrumbs']
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'base_breadcrumbs'):
            context['breadcrumbs'] = self.base_breadcrumbs + self.get_extra_breadcrumbs()
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
