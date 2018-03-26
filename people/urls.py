from django.urls import path, include, reverse_lazy
from django.views.generic.base import TemplateView

from .views import PeopleHomeView,\
    GodList, GodAdd, GodDetail, GodEdit, GodDelete,\
    PersonList, PersonAdd, PersonDetail, PersonEdit, PersonDelete
from dmtools.urls import breadcrumbs as core_breadcrumbs

breadcrumbs = core_breadcrumbs + [{'href': reverse_lazy('people-home'), 'text': 'People'}]

gods_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('gods-home'), 'text': 'Gods'}]

gods_patterns = [
    path('', GodList.as_view(), name='gods-home'),
    path('add/', GodAdd.as_view(), name='god-add'),
    path('<int:pk>/', GodDetail.as_view(), name='god-view'),
    path('<int:pk>/edit/', GodEdit.as_view(), name='god-edit'),
    path('<int:pk>/delete/', GodDelete.as_view(), name='god-delete'),
]

npcs_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('npcs-home'), 'text': 'NPCs'}]

npcs_patterns = [
    path('', PersonList.as_view(), name='npcs-home'),
    path('add/', PersonAdd.as_view(), name='npc-add'),
    path('<int:pk>/', PersonDetail.as_view(), name='npc-view'),
    path('<int:pk>/edit/', PersonEdit.as_view(), name='npc-edit'),
    path('<int:pk>/delete/', PersonDelete.as_view(), name='npc-delete'),
]

urlpatterns = [
    path('', PeopleHomeView.as_view(), {'base_breadcrumbs': breadcrumbs}, name='people-home'),
    path('gods/', include(gods_patterns), {'base_breadcrumbs': gods_breadcrumbs}),
    path('npcs/', include(npcs_patterns), {'base_breadcrumbs': npcs_breadcrumbs}),
]
