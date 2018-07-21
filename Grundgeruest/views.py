from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your views here.

class IndexView(TemplateView):
    """ zeigt die Startseite an :) """
    template_name = 'Grundgeruest/templates/Grundgeruest/startseite.html'
