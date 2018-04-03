from django.urls import path, include, reverse_lazy

from .views import \
    MonsterList, MonsterAdd, MonsterDetail, MonsterEdit, MonsterDelete, \
    SpecialPropertyList, SpecialPropertyAdd, SpecialPropertyDetail, SpecialPropertyEdit, SpecialPropertyDelete

from dmtools.urls import breadcrumbs as core_breadcrumbs

breadcrumbs = core_breadcrumbs

monsters_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('monsters-home'), 'text': 'Monsters'}]

monsters_patterns = [
    path('', MonsterList.as_view(), name='monsters-home'),
    path('add/', MonsterAdd.as_view(), name='monster-add'),
    path('<int:pk>/', MonsterDetail.as_view(), name='monster-view'),
    path('<int:pk>/edit/', MonsterEdit.as_view(), name='monster-edit'),
    path('<int:pk>/delete/', MonsterDelete.as_view(), name='monster-delete'),
]

specialprop_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('specialproperties-home'), 'text': 'Monster properties'}]

specialprop_patterns = [
    path('', SpecialPropertyList.as_view(), name='specialproperties-home'),
    path('add/', SpecialPropertyAdd.as_view(), name='specialproperty-add'),
    path('<int:pk>/', SpecialPropertyDetail.as_view(), name='specialproperty-view'),
    path('<int:pk>/edit/', SpecialPropertyEdit.as_view(), name='specialproperty-edit'),
    path('<int:pk>/delete/', SpecialPropertyDelete.as_view(), name='specialproperty-delete'),
]

urlpatterns = [
    path('monsters/', include(monsters_patterns), {'base_breadcrumbs': monsters_breadcrumbs}),
    path('monster-properties/', include(specialprop_patterns), {'base_breadcrumbs': specialprop_breadcrumbs}),
]
