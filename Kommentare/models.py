from django.db import models
from Grundgeruest.models import Grundklasse, MinimalModel
from django_markdown.models import MarkdownField
from django.conf import settings

Profil = settings.AUTH_PROFILE_MODULE

class Liste(MinimalModel):
    def __str__(self):
        if hasattr(self, 'objekt'):
            return str(self.objekt)
        else:
            return super().__str__()

    class Meta:
        verbose_name = 'Kommentarliste'
        verbose_name_plural = 'Kommentarlisten'


class Kommentar(MinimalModel):
    liste = models.ForeignKey(
        Liste,
        on_delete=models.CASCADE,
        related_name='kommentare',
    ) 
    text = MarkdownField()
    autor = models.ForeignKey(
        Profil,
        on_delete=models.CASCADE,
        null=True,
        related_name='kommentare',
    ) 

    class Meta:
        verbose_name = 'Kommentar'
        verbose_name_plural = 'Kommentare'

