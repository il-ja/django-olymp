from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404
from django.urls import reverse

# Create your views here.

class IndexView(RedirectView):
    permanent = False
    url = "/olymp"

class RandomusView(RedirectView):
    permanent = False
    def get_redirect_url(self, *args, **kwargs):
        from random import random, choice
        from Wettbewerbe.models import Veranstaltung, WettbewerbKonkret
        if random() < 0.3:
            return "/olymp/"
        if random() < 0.5:
            return choice(Veranstaltung.objects.all()).get_absolute_url()
        
        return choice(WettbewerbKonkret.objects.all()).get_absolute_url()


