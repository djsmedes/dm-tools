from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from .models import God, GodForm


class GodCreate(CreateView):
    model = God
    fields = [field.name for field in God._meta.fields]
    # todo: many to many fields (God._meta.many_to_many)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'god-add'
        return context


class GodUpdate(UpdateView):
    model = God
    # fields = [field.name for field in God._meta.fields]
    form_class = GodForm
    # todo: many to many fields (God._meta.many_to_many)
    # for fields defined in reverse from other models, see
    #   https://stackoverflow.com/questions/2216974/django-modelform-for-many-to-many-fields

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumbs'] = context['base_breadcrumbs'] + [
            {'text': self.object.name, 'href': reverse_lazy('god-view', kwargs={'pk': self.object.pk})},
            {'text': 'Edit'}
        ]
        context['form_action'] = 'god-edit'
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
