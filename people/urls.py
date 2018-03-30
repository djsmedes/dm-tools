from django.urls import path, include, reverse_lazy

from .views import \
    GodList, GodAdd, GodDetail, GodEdit, GodDelete,\
    PersonList, PersonAdd, PersonDetail, PersonEdit, PersonDelete,\
    PopulationList, PopulationAdd, PopulationDetail, PopulationEdit, PopulationDelete, \
    CombatantAdd
from dmtools.urls import breadcrumbs as core_breadcrumbs

breadcrumbs = core_breadcrumbs

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

populations_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('populations-home'), 'text': 'Populations'}]

populations_patterns = [
    path('', PopulationList.as_view(), name='populations-home'),
    path('add/', PopulationAdd.as_view(), name='population-add'),
    path('<int:pk>/', PopulationDetail.as_view(), name='population-view'),
    path('<int:pk>/edit/', PopulationEdit.as_view(), name='population-edit'),
    path('<int:pk>/delete/', PopulationDelete.as_view(), name='population-delete'),
]

urlpatterns = [
    path('gods/', include(gods_patterns), {'base_breadcrumbs': gods_breadcrumbs}),
    path('npcs/', include(npcs_patterns), {'base_breadcrumbs': npcs_breadcrumbs}),
    path('populations/', include(populations_patterns), {'base_breadcrumbs': populations_breadcrumbs}),
    path('add-combatant/', CombatantAdd.as_view(), {'base_breadcrumbs': breadcrumbs}, name='combatant-add'),
]
