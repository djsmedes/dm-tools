from django.shortcuts import render
from django.views.generic.base import TemplateView

from base.views import BreadCrumbMixin


class CanvasView(BreadCrumbMixin, TemplateView):

    template_name = 'places/canvas.html'
