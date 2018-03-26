from django.urls import path, include, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .models import God
from .views import GodCreate, GodDelete, GodUpdate, GodDetail
from dmtools.urls import breadcrumbs as core_breadcrumbs

breadcrumbs = core_breadcrumbs + [{'href': reverse_lazy('people-home'), 'text': 'People'}]

gods_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('gods-home'), 'text': 'Gods'}]

gods_patterns = [
    path(
        '',
        ListView.as_view(
            model=God,
            template_name='people/_list.html',
            extra_context={'breadcrumbs': gods_breadcrumbs},
        ),
        name='gods-home'
    ),
    path(
        'add/',
        GodCreate.as_view(
            extra_context={'breadcrumbs': gods_breadcrumbs + [{'text': 'Add'}]}
        ),
        name='god-add'
    ),
    path(
        '<int:pk>/',
        GodDetail.as_view(
            extra_context={'base_breadcrumbs': gods_breadcrumbs},
        ),
        name='god-view'
    ),
    path(
        '<int:pk>/edit/',
        GodUpdate.as_view(
            extra_context={'base_breadcrumbs': gods_breadcrumbs},
        ),
        name='god-edit'
    ),
    path('<int:pk>/delete/', GodDelete.as_view(), name='god-delete'),
]

urlpatterns = [
    path(
        '',
        TemplateView.as_view(
            template_name='people/home.html',
            extra_context={'breadcrumbs': breadcrumbs}
        ),
        name='people-home'
    ),
    path('gods/', include(gods_patterns)),
]
