from django.urls import path, include, reverse_lazy

from .views import \
    MonsterList, MonsterAdd, MonsterDetail, MonsterEdit, MonsterDelete, MonsterAutocomplete, \
    SpecialPropertyList, SpecialPropertyAdd, SpecialPropertyDetail, SpecialPropertyEdit, SpecialPropertyDelete, SpecialPropertyAutocomplete, \
    ActionList, ActionAdd, ActionDetail, ActionEdit, ActionDelete, ActionAutocomplete, \
    LegendaryActionList, LegendaryActionAdd, LegendaryActionDetail, LegendaryActionEdit, LegendaryActionDelete, LegendaryActionAutocomplete, \
    ReactionList, ReactionAdd, ReactionDetail, ReactionEdit, ReactionDelete, ReactionAutocomplete

from dmtools.urls import breadcrumbs

monsters_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('monsters-home'), 'text': 'Monsters'}]

monsters_patterns = [
    path('', MonsterList.as_view(), name='monsters-home'),
    path('add/', MonsterAdd.as_view(), name='monster-add'),
    path('<int:pk>/', MonsterDetail.as_view(), name='monster-view'),
    path('<int:pk>/edit/', MonsterEdit.as_view(), name='monster-edit'),
    path('<int:pk>/delete/', MonsterDelete.as_view(), name='monster-delete'),
]

specialprop_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('specialproperties-home'), 'text': 'Monster Special Properties'}]

specialprop_patterns = [
    path('', SpecialPropertyList.as_view(), name='specialproperties-home'),
    path('add/', SpecialPropertyAdd.as_view(), name='specialproperty-add'),
    path('<int:pk>/', SpecialPropertyDetail.as_view(), name='specialproperty-view'),
    path('<int:pk>/edit/', SpecialPropertyEdit.as_view(), name='specialproperty-edit'),
    path('<int:pk>/delete/', SpecialPropertyDelete.as_view(), name='specialproperty-delete'),
]

action_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('actions-home'), 'text': 'Monster Actions'}]

action_patterns = [
    path('', ActionList.as_view(), name='actions-home'),
    path('add/', ActionAdd.as_view(), name='action-add'),
    path('<int:pk>/', ActionDetail.as_view(), name='action-view'),
    path('<int:pk>/edit/', ActionEdit.as_view(), name='action-edit'),
    path('<int:pk>/delete/', ActionDelete.as_view(), name='action-delete'),
]

legaction_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('legendaryactions-home'), 'text': 'Monster Legendary Actions'}]

legaction_patterns = [
    path('', LegendaryActionList.as_view(), name='legendaryactions-home'),
    path('add/', LegendaryActionAdd.as_view(), name='legendaryaction-add'),
    path('<int:pk>/', LegendaryActionDetail.as_view(), name='legendaryaction-view'),
    path('<int:pk>/edit/', LegendaryActionEdit.as_view(), name='legendaryaction-edit'),
    path('<int:pk>/delete/', LegendaryActionDelete.as_view(), name='legendaryaction-delete'),
]

reaction_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('reactions-home'), 'text': 'Monster Reactions'}]

reaction_patterns = [
    path('', ReactionList.as_view(), name='reactions-home'),
    path('add/', ReactionAdd.as_view(), name='reaction-add'),
    path('<int:pk>/', ReactionDetail.as_view(), name='reaction-view'),
    path('<int:pk>/edit/', ReactionEdit.as_view(), name='reaction-edit'),
    path('<int:pk>/delete/', ReactionDelete.as_view(), name='reaction-delete'),
]

autocomplete_patterns = [
    path('special-property/', SpecialPropertyAutocomplete.as_view(create_field='name'), name='specialproperty-autocomplete'),
    path('action/', ActionAutocomplete.as_view(create_field='name'), name='action-autocomplete'),
    path('legendary-action/', LegendaryActionAutocomplete.as_view(create_field='name'), name='legendaryaction-autocomplete'),
    path('reaction/', ReactionAutocomplete.as_view(create_field='name'), name='reaction-autocomplete'),
    path('monster/', MonsterAutocomplete.as_view(), name='monster-autocomplete'),
]

urlpatterns = [
    path('monsters/', include(monsters_patterns), {'base_breadcrumbs': monsters_breadcrumbs}),
    path('monster-properties/', include(specialprop_patterns), {'base_breadcrumbs': specialprop_breadcrumbs}),
    path('monster-actions/', include(action_patterns), {'base_breadcrumbs': action_breadcrumbs}),
    path('monster-legendary-actions/', include(legaction_patterns), {'base_breadcrumbs': legaction_breadcrumbs}),
    path('monster-reactions/', include(reaction_patterns), {'base_breadcrumbs': reaction_breadcrumbs}),
    path('autocomplete/', include(autocomplete_patterns)),
]
