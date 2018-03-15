from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your views here.

class IndexView(DetailView):
    """ zeigt die Startseite an :) """
    def get_object(self):
        from Kommentare import models
        return get_object_or_404(
            models.Liste,
            pk=1,
        )

    template_name = 'Grundgeruest/templates/Grundgeruest/startseite.html'
    context_object_name = 'liste'
