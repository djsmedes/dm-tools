from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .models import God, GodForm, Person, PersonForm, Organization, Population


class PeopleListView(ListView):
    template_name = 'people/_list.html'
    extra_breadcrumbs = []

    def get(self, *args, **kwargs):
        if kwargs.get('base_breadcrumbs'):
            self.base_breadcrumbs = kwargs['base_breadcrumbs']
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'base_breadcrumbs'):
            context['breadcrumbs'] = self.base_breadcrumbs + self.extra_breadcrumbs
        context['model'] = self.model
        return context


class GodList(PeopleListView):
    model = God


class PersonList(PeopleListView):
    model = Person


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


class GodEdit(UpdateView):
    model = God
    form_class = GodForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = context['base_breadcrumbs'] + [
            {'text': self.object.name, 'href': reverse_lazy('god-view', kwargs={'pk': self.object.pk})},
            {'text': 'Edit'}
        ]
        context['form_action'] = 'god-edit'
        context['form'] = GodForm(instance=self.object)
        return context


class GodDelete(DeleteView):
    model = God
    success_url = reverse_lazy('gods-home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = context['base_breadcrumbs'] + [
            {'text': self.object.name, 'href': reverse_lazy('god-view', kwargs={'pk': self.object.pk})},
            {'text': 'Delete'}
        ]


class GodDetail(DetailView):
    model = God

    def get(self, *args, **kwargs):
        if kwargs.get('base_breadcrumbs'):
            self.base_breadcrumbs = kwargs['base_breadcrumbs']
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'base_breadcrumbs'):
            context['breadcrumbs'] = self.base_breadcrumbs + [{'text': self.object.name}]
        context['form'] = GodForm(instance=self.object)
        return context
