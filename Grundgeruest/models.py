from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from django.db import models 
from django.template.defaultfilters import slugify


class Grundklasse(TimeStampedModel, TitleSlugDescriptionModel):
    """ Klasse für Objekte, die detail-view haben können """
    def get_absolute_url(self):
        """ Sollte überschrieben werden, für den Notfall so: """
        return '/{model}/{slug}/'.format(
            model=self.__class__.__name__.lower(),
            slug=self.slug,
        )

    slug = models.SlugField(
        max_length=99,
        null=False,
        blank=True,
    )

    def save(self, **kwargs):
        """ Falls nicht gesetzt, slug autoausfüllen """
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(**kwargs)

    def __str__(self):
        return self.title

    class Meta:
        abstract=True
