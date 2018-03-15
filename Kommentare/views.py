from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from . import models
from django.urls import reverse

class NeuerKommentar(CreateView):
    """ Erstellt Kommentar in der aus der url übergeben Liste """
    model = models.Kommentar
    fields = ['text']
    template_name = 'Kommentare/erstellen.html'
    context_object_name = 'kommentar'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        liste = get_object_or_404(models.Liste, pk=self.kwargs.get('pk'))
        instanz = models.Kommentar(liste=liste, autor=self.request.user.profil)
        kwargs.update([('instance', instanz)])
        return kwargs


