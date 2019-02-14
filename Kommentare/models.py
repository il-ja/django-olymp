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
                    raise ValueError(
                        "Kommentarliste darf nur zu %s gehören!" % " *oder* ".join([cls.__name__ for cls in self.models_mit_kommentaren])
                    )
                else:
                    objekt = getattr(self, 'objekt_%s' % model.__name__)
        return objekt

    def save(self, *args, **kwargs):
        """ soll verhindern, dass man eine Liste mit mehreren verknüpften
        Objekten speichern kann. Funktioniert irgendwie nicht^^ also es
        geht trotzdem in der shell. also: TODO """
        attrs = [model.__name__ for model in self.models_mit_kommentaren]
        if sum(hasattr(self, attr) for attr in attrs) > 1:
            raise ValueError("Kommentarliste %s ist mit mehr als einem Objekt verknüpft!" % self.pk)
        super().save(*args, **kwargs)

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
                on_delete=models.SET_NULL,
                related_name='objekt_%s' % name)
        )
        Liste.models_mit_kommentaren.append(KlasseMitKommentaren)
        KlasseMitKommentaren.add_to_class(
            'kommentarliste_erstellen',
            models.BooleanField(default=False),
        )

        # diese Methode sollen Instanzen von KlasseMitKommentaren haben
        def goc(self):
            """ gibt die Kommentarliste zurück, falls das Objekt schon eine
            hat, erstellt sonst eine neue und gibt die zurück """
            if not self.kommentarliste is None:
                return self.kommentarliste
            else:
                liste = Liste.objects.create()
                self.kommentarliste = liste
                self.save()
                return liste
        KlasseMitKommentaren.get_or_create_kommentarliste = goc

        def speichern(self, *args, **kwargs):
            if self.kommentarliste_erstellen:
                self.kommentarliste_erstellen = False
                self.get_or_create_kommentarliste()
            return super(KlasseMitKommentaren, self).save(*args, **kwargs)
        KlasseMitKommentaren.save = speichern

        return KlasseMitKommentaren

    class Meta:
        abstract = True

