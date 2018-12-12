from django.db import models
from django_extensions.db.models import TimeStampedModel
from Grundgeruest.models import Grundklasse
from django.db.models.base import ModelBase
from django.contrib.auth import get_user_model

class Liste(TimeStampedModel):

    models_mit_kommentaren = []

    @property
    def objekt(self):
        """ Gibt das verknüpfte Objekt zurück
        Validiert nebenbei, dass nicht mehrere verknüpft sind """
        objekt = None
        for model in self.models_mit_kommentaren:
            if hasattr(self, 'objekt_%s' % model.__name__):
                if objekt: # also wenn bei vorherigem Schleifendurchlauf schon gesetzt
                    raise(ValidationError(
                        "Kommentarliste darf nur zu %s gehören!" % " *oder* ".join(self.models_mit_kommentaren)
                    ))
                else:
                    objekt = getattr(self, 'objekt_%s' % model.__name__)
        return objekt

    def __str__(self):
        if hasattr(self, 'objekt'):
            return str(self.objekt)
        else:
            return super().__str__()

    def get_absolute_url(self):
        return self.objekt.get_absolute_url()

    class Meta:
        verbose_name = 'Kommentarliste'
        verbose_name_plural = 'Kommentarlisten'


class Kommentar(TimeStampedModel):
    liste = models.ForeignKey(
        Liste,
        on_delete=models.CASCADE,
        related_name='kommentare',
    )
    text = models.TextField()
    autor = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        related_name='kommentare',
    )

    def get_absolute_url(self):
        return self.liste.get_absolute_url()

    class Meta:
        verbose_name = 'Kommentar'
        verbose_name_plural = 'Kommentare'


class KommentareMetaklasse(ModelBase):
    """ Kann als Metaklasse in einer Klassendefinition
    angegeben werden, damit diese mit einer Kommentarliste
    verknüpft wird """
    def __new__(cls, name, parents, attribute):
        KlasseMitKommentaren = super().__new__(cls, name, parents, attribute)
        KlasseMitKommentaren.add_to_class(
            'kommentarliste',
            models.OneToOneField(
                Liste,
                null=True,
                blank=True,
                on_delete=models.CASCADE,
                related_name='objekt_%s' % name)
        )
        Liste.models_mit_kommentaren.append(KlasseMitKommentaren)

        return KlasseMitKommentaren

    class Meta:
        abstract = True

