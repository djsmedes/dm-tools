from django.urls import path, include, reverse_lazy

from dmtools.urls import breadcrumbs as core_breadcrumbs
from .views import CanvasView, PlaceDetail, PlaceList
from .models import Place

breadcrumbs = core_breadcrumbs

places_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('places-home'), 'text': 'Places'}]

places_patterns = [
    path('', CanvasView.as_view(), name='places-home')
]

api_patterns = [
    path(Place.api_url(), PlaceList.as_view()),
    path(Place.api_url() + '<int:pk>/', PlaceDetail.as_view()),
]

urlpatterns = [
    path('places/', include(places_patterns), {'base_breadcrumbs': places_breadcrumbs}),
    path('', include(api_patterns))
]
