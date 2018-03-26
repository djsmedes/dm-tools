from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import God


class GodCreate(CreateView):
    model = God
    fields = [field.name for field in God._meta.fields]
    # todo: many to many fields (God._meta.many_to_many)


class GodUpdate(UpdateView):
    model = God
    fields = [field.name for field in God._meta.fields]
    # todo: many to many fields (God._meta.many_to_many)


class GodDelete(DeleteView):
    model = God
    success_url = reverse_lazy('gods-list')
