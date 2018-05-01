from django.urls import path

from .views import PlaceList

urlpatterns = [
    path('places/', PlaceList.as_view())
]
