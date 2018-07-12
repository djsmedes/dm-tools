from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView

from .views import \
    GodList, GodAdd, GodDetail, GodEdit, GodDelete,\
    PersonList, PersonAdd, PersonDetail, PersonEdit, PersonDelete,\
    RaceList, RaceAdd, RaceDetail, RaceEdit, RaceDelete, \
    CombatantAdd, CombatantEdit, CombatantDelete
from _config.urls import breadcrumbs as core_breadcrumbs

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

races_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('races-home'), 'text': 'Races'}]

races_patterns = [
    path('', RaceList.as_view(), name='races-home'),
    path('add/', RaceAdd.as_view(), name='race-add'),
    path('<int:pk>/', RaceDetail.as_view(), name='race-view'),
    path('<int:pk>/edit/', RaceEdit.as_view(), name='race-edit'),
    path('<int:pk>/delete/', RaceDelete.as_view(), name='race-delete'),
]

combatants_patterns = [
    path('', RedirectView.as_view(url=reverse_lazy('home'))),
    path('add/', CombatantAdd.as_view(), name='combatant-add'),
    path('<int:pk>/', RedirectView.as_view(url=reverse_lazy('combatant-edit'))),
    path('<int:pk>/edit/', CombatantEdit.as_view(), name='combatant-edit'),
    path('<int:pk>/delete/', CombatantDelete.as_view(), name='combatant-delete'),
]

urlpatterns = [
    path('gods/', include(gods_patterns), {'base_breadcrumbs': gods_breadcrumbs}),
    path('npcs/', include(npcs_patterns), {'base_breadcrumbs': npcs_breadcrumbs}),
    path('races/', include(races_patterns), {'base_breadcrumbs': races_breadcrumbs}),
    path('combatants/', include(combatants_patterns), {'base_breadcrumbs': breadcrumbs}),
]
