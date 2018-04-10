from django.urls import path, include, reverse_lazy

from .views import DmScreenTabList, DmScreenTabAdd, DmScreenTabDetail, DmScreenTabEdit, DmScreenTabDelete

from dmtools.urls import breadcrumbs

dmscreen_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('dmscreentabs-home'), 'text': 'DM Screen Tabs'}]

dmscreen_patterns = [
    path('', DmScreenTabList.as_view(), name='dmscreentabs-home'),
    path('add/', DmScreenTabAdd.as_view(), name='dmscreentab-add'),
    path('<int:pk>/', DmScreenTabDetail.as_view(), name='dmscreentab-view'),
    path('<int:pk>/edit/', DmScreenTabEdit.as_view(), name='dmscreentab-edit'),
    path('<int:pk>/delete/', DmScreenTabDelete.as_view(), name='dmscreentab-delete'),
]

urlpatterns = [
    path('dm-screen-tabs/', include(dmscreen_patterns), {'base_breadcrumbs': dmscreen_breadcrumbs}),
]
