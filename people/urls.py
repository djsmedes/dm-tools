from django.urls import path, include
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from .models import God
from .views import GodCreate, GodDelete, GodUpdate

gods_patterns = [
    path('', ListView.as_view(model=God, template_name='people/people_list.html'), name='gods-list'),
    path('add/', GodCreate.as_view(), name='god-add'),
    path('<int:pk>/', GodUpdate.as_view(), name='god-update'),
    path('<int:pk>/delete/', GodDelete.as_view(), name='god-delete'),
]


urlpatterns = [
    path('', TemplateView.as_view(template_name='people/home.html'), name='people-home'),
    path('gods/', include(gods_patterns)),
]
