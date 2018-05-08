from django.urls import path

from .views import PlaceDetail, PlaceList

urlpatterns = [
    path('places/', PlaceList.as_view()),
    path('places/<int:pk>/', PlaceDetail.as_view()),
]
