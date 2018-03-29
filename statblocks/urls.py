from django.urls import path, include, reverse_lazy

from .views import \
    MonsterList

from dmtools.urls import breadcrumbs as core_breadcrumbs

breadcrumbs = core_breadcrumbs

monsters_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('monsters-home'), 'text': 'Monsters'}]

monsters_patterns = [
    path('', MonsterList.as_view(), name='monsters-home'),
    # path('', MonsterList.as_view(), name='monsters-home'),
    # path('add/', MonsterAdd.as_view(), name='monster-add'),
    # path('<int:pk>/', MonsterDetail.as_view(), name='monster-view'),
    # path('<int:pk>/edit/', MonsterEdit.as_view(), name='monster-edit'),
    # path('<int:pk>/delete/', MonsterDelete.as_view(), name='monster-delete'),
]

urlpatterns = [
    path('monsters/', include(monsters_patterns), {'base_breadcrumbs': monsters_breadcrumbs}),
]
