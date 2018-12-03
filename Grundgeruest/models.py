from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel

class Grundklasse(TimeStampedModel, TitleSlugDescriptionModel):
    """ Klasse für Objekte, die detail-view haben können """
    def get_absolute_url(self):
        """ Sollte überschrieben werden, für den Notfall so: """
        return '/{model}/{slug}/'.format(
            model=self.__class__.__name__.lower(),
            slug=self.slug,
        )

    def __str__(self):
        return str(self.name)

    class Meta:
        abstract=True
