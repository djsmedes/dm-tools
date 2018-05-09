from django.urls import path, include, reverse_lazy

from dmtools.urls import breadcrumbs as core_breadcrumbs
from .views import PlaceDetailAPI, PlaceListAPI, PlaceComboCanvasView, PlaceComboView
from .models import Place

breadcrumbs = core_breadcrumbs

places_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('places-home'), 'text': 'Places'}]

places_patterns = [
    path('', PlaceComboView.as_view(), name='places-home'),
    path('canvas/', PlaceComboCanvasView.as_view(), name='places-canvas'),
]

api_patterns = [
    path(Place.api_url(), PlaceListAPI.as_view()),
    path(Place.api_url() + '<int:pk>/', PlaceDetailAPI.as_view()),
]

urlpatterns = [
    path('places/', include(places_patterns), {'base_breadcrumbs': places_breadcrumbs}),
    path('', include(api_patterns))
]
