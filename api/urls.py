from django.urls import path

from .views import PlaceList, PlaceInfo

urlpatterns = [
    path('places/', PlaceList.as_view()),
    path('places/<int:pk>/', PlaceInfo.as_view()),
]
