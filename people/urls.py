from django.urls import path, include
from .views import GodCreate, GodDelete, GodUpdate


urlpatterns = [
    path('god/add/', GodCreate.as_view(), name='god-add'),
    path('god/<int:pk/', GodUpdate.as_view(), name='god-update'),
    path('god/<int:pk/delete/', GodDelete.as_view(), name='god-delete'),
]
