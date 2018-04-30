from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import JsonResponse

from base.views import BreadCrumbMixin

from .models import Place


class CanvasView(BreadCrumbMixin, TemplateView):

    template_name = 'places/canvas.html'


def get_place_data(request):
    ret_dict = []
    for place in Place.objects.all():
        ret_dict.append({'points': place.pointstring})
    return JsonResponse({'shape_set': ret_dict}, safe=False)
