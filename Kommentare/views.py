from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from . import models
from django.urls import reverse

class NeuerKommentar(LoginRequiredMixin, CreateView):
    """ Erstellt Kommentar in der durch die url übergebene Liste """
    model = models.Kommentar
    fields = ['text']
    template_name = 'Kommentare/bearbeiten.html'
    context_object_name = 'kommentar'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        liste = get_object_or_404(models.Liste, pk=self.kwargs.get('pk'))
        instanz = models.Kommentar(liste=liste, autor=self.request.user)
        kwargs.update([('instance', instanz)])
        return kwargs


class KommentarEditieren(LoginRequiredMixin, UpdateView):
    """ Editiert Kommentar mit dem aus der url übergebenen pk """
    model = models.Kommentar
    fields = ['text']
    template_name = 'Kommentare/bearbeiten.html'
    context_object_name = 'kommentar'


class KommentarLoeschen(LoginRequiredMixin, DeleteView):
    """ Entfernt Kommentar mit dem aus der url übergebenen pk """
    model = models.Kommentar
    template_name = 'Kommentare/loeschen.html'
    context_object_name = 'kommentar'

    def get_success_url(self):
        return self.get_object().get_absolute_url()


