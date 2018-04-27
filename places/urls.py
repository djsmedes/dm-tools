from django.urls import path, include, reverse_lazy

from dmtools.urls import breadcrumbs as core_breadcrumbs
from .views import CanvasView

breadcrumbs = core_breadcrumbs

places_breadcrumbs = breadcrumbs + [{'href': reverse_lazy('places-home'), 'text': 'Places'}]

places_patterns = [
    path('', CanvasView.as_view(), name='places-home')
]

urlpatterns = [
    path('', include(places_patterns), {'base_breadcrumbs': places_breadcrumbs})
]
