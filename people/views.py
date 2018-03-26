from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import God


class GodCreate(CreateView):
    model = God
    fields = ['name']


class GodUpdate(UpdateView):
    model = God
    fields = ['name', 'description', 'gender', 'patron_of', 'cleric_domains']


class GodDelete(DeleteView):
    model = God
    success_url = reverse_lazy('author-list')
