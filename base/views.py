from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import ContextMixin, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
from pytz import utc

from people.models import Combatant
from .forms import EffectForm
from .utils import get_last_updated
from .models import DmScreenTab, DmScreenTabForm


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


class BaseComboView(BreadCrumbMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['api_url'] = '/' + self.model.api_url()  # can't start with / for urlconf, needs to for axios
        return context


class BaseListView(BreadCrumbMixin, ListView):
    template_name = 'base/_table.html'
    table_headers = [
        'Name',
    ]
    table_data_accessors = [
        'name'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['table_headers'] = self.table_headers
        context['table_data_accessors'] = self.table_data_accessors
        return context


class BaseCreateView(LoginRequiredMixin, BreadCrumbMixin, CreateView):
    extra_breadcrumbs = [{'text': 'Add'}]
    template_name = 'base/_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = '{}-add'.format(self.model.url_prefix())
        context['model'] = self.model
        return context


class BaseUpdateView(LoginRequiredMixin, BreadCrumbMixin, UpdateView):
    template_name = 'base/_form.html'

    def get_extra_breadcrumbs(self):
        return [
            {
                'text': self.object.name,
                'href': reverse_lazy(
                    '{}-view'.format(self.model.url_prefix()),
                    kwargs={'pk': self.object.pk}
                ),
            },
            {'text': 'Edit'}
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = '{}-edit'.format(self.model.url_prefix())
        return context


class BaseDeleteView(LoginRequiredMixin, BreadCrumbMixin, DeleteView):
    template_name = 'base/_confirm_delete.html'

    def get_extra_breadcrumbs(self):
        return [
            {
                'text': self.object.name,
                'href': reverse_lazy(
                    '{}-view'.format(self.model.url_prefix()),
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
        kwargs['dmscreentabs'] = DmScreenTab.objects.filter(sort_order__gte=0)
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
    htmls = {}
    for combatant in Combatant.objects.all():
        htmls[combatant.id] = render_to_string(
            'base/combatant_card_body.html', {
                'combatant': combatant
            })
    return JsonResponse(htmls)


def remove_effect(request):
    if not (
            request.POST.get('index') and
            request.POST.get('effect_type') and
            request.POST.get('combatant')
    ):
        return HttpResponse('')

    index = int(request.POST['index'])
    effect_type = request.POST['effect_type']
    combatant_id = int(request.POST['combatant'])

    combatant = Combatant.objects.get(id=combatant_id)
    if effect_type == 'buff':
        combatant.buffs.pop(index)
    elif effect_type == 'debuff':
        combatant.debuffs.pop(index)
    else:  # other
        combatant.other_effects.pop(index)
    combatant.save()

    return render_to_response(
        'base/combatant_card_body.html',
        {'combatant': combatant}
    )


def remove_combatants(request):
    combatant_ids = []
    for thing in request.POST:
        if thing.isdigit() and bool(request.POST[thing]):
            combatant_ids.append(int(thing))

    if not combatant_ids:
        return HttpResponse('')

    # combatant_ids = [int(cid) for cid in request.POST['combatant_ids'].split(',') if cid]
    for cid in combatant_ids:
        c = Combatant.objects.get(id=cid)
        c.delete()
    resp = render(
        request,
        'base/combatant_card_deck.html',
        {'combatant_list': Combatant.objects.all()}
    )
    return resp


def update_initiative(request):
    if not (
        request.POST.get('combatant_id') and
        request.POST.get('initiative')
    ):
        return HttpResponse('')

    # update combatant initiative
    c = Combatant.objects.get(id=int(request.POST['combatant_id']))
    c.initiative = int(request.POST['initiative'])
    c.save()

    return update_all_combatants(request)


def update_all_combatants(request):
    return render(
        request,
        'base/combatant_card_deck.html',
        {'combatant_list': Combatant.objects.all()}
    )


def poll_for_combatant_updates(request):
    resp = {}
    if not request.GET.get('last_updated'):
        return JsonResponse(resp)

    page_last_updated = datetime.utcfromtimestamp(
        float(request.GET['last_updated'])/1000.
    )
    page_last_updated = utc.localize(page_last_updated)
    combatants_last_updated = get_last_updated(Combatant)
    if combatants_last_updated is None:
        # never updated, so whatever the page loaded the first time is fine
        pass
    elif page_last_updated < combatants_last_updated:
        resp['needs_update'] = True

    return JsonResponse(resp)


class DmScreenTabList(LoginRequiredMixin, BaseListView):
    model = DmScreenTab


class DmScreenTabAdd(BaseCreateView):
    model = DmScreenTab
    form_class = DmScreenTabForm


class DmScreenTabEdit(BaseUpdateView):
    model = DmScreenTab
    form_class = DmScreenTabForm


class DmScreenTabDelete(BaseDeleteView):
    model = DmScreenTab
    success_url = reverse_lazy('dmscreentabs-home')


class DmScreenTabDetail(LoginRequiredMixin, BaseDetailView):
    model = DmScreenTab
    template_name = 'base/dmscreentab_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = [context.get('object', None)]
        return context
