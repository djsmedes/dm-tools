# importing this to be used in an exec in a lambda expression
# noinspection PyUnresolvedReferences
from django.http import Http404, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import ContextMixin, TemplateView
from django.shortcuts import redirect, render_to_response

from multiselectfield.db.fields import MSFList

from people.models import Combatant
from .forms import EffectForm


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


class BaseListView(BreadCrumbMixin, ListView):
    template_name = 'base/_table.html'
    table_headers = []
    table_data_accessors = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['table_headers'] = self.table_headers
        context['table_data_accessors'] = self.table_data_accessors
        return context


class BaseCreateView(BreadCrumbMixin, CreateView):
    extra_breadcrumbs = [{'text': 'Add'}]
    template_name = 'base/_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = '{}-add'.format(self.model._meta.verbose_name)
        context['model'] = self.model
        return context


class BaseUpdateView(BreadCrumbMixin, UpdateView):
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
        # context['form'] = self.form_class(instance=self.object)
        return context


class BaseDeleteView(BreadCrumbMixin, DeleteView):
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


class BaseDetailView(BreadCrumbMixin, DetailView):
    template_name = 'base/_detail.html'
    form_class = None

    def get_form(self):
        if self.form_class:
            return self.form_class(instance=self.object)
        return None

    def get_extra_breadcrumbs(self):
        return [{'text': self.object.name}]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.form_class:
            context['form'] = self.get_form()
        return context


class HomepageView(TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        kwargs['combatant_list'] = Combatant.objects.all()
        return super().get_context_data(**kwargs)


def get_effects(request):
    effects = {}
    for key in request.POST:
        if str(key).endswith(('_buff', '_debuff', '_other')):
            effects[key] = request.POST[key]
    return effects


def save_field(name, value):
    if not value:
        return
    name_pieces = name.split('_')
    object_pk = int(name_pieces[1])
    effect_kind = name_pieces[2]
    combatant = Combatant.objects.get(id=object_pk)
    if effect_kind == 'buff':
        combatant.buffs.append(value)
    elif effect_kind == 'debuff':
        combatant.debuffs.append(value)
    else:  # other
        combatant.other_effects.append(value)
    combatant.save()


def update_effect_list(request):
    effects = get_effects(request)
    form = EffectForm(request.POST, extra=effects)
    if form.is_valid():
        for name in form.changed_data:
            save_field(name, form.cleaned_data[name])
    return render_to_response(
        'base/combatant_card_deck.html', {
            'combatant_list': Combatant.objects.all()
        }
    )
