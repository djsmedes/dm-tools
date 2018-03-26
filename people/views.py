from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .models import God, GodForm


class GodCreate(CreateView):
    model = God
    form_class = GodForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'god-add'
        return context


class GodUpdate(UpdateView):
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


class GodDetail(DetailView):
    model = God

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = context['base_breadcrumbs'] + [{'text': self.object.name}]
        context['form'] = GodForm(instance=self.object)
        return context
