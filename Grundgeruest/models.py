
# Zuerst zwei Grund-Models, von denen der Rest erbt:
from django.db import models
from django.template.defaultfilters import slugify

class MinimalModel(models.Model):
    """ Gemeinsame Attribute, die alle Objekte haben sollen """

    zeit_erstellt = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    zeit_geaendert = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    nutzer_geaendert = models.TextField(
        editable=False,
        default='0',
    )
    def save(self, **kwargs):
        """ zusätzliche Metadaten setzen vor save

        falls nutzer_geaendert explizit übergeben wurde, trage ihn ein, 
        wenn nicht, trage null ein, falls es das nicht schon war
        """
        uebergeben = kwargs.get('nutzer_geaendert', False)
        if uebergeben:
            self.nutzer_geaendert += ', {}'.format(uebergeben)
            del(kwargs['nutzer_geaendert'])
        else:
            letzter_nutzer = int(self.nutzer_geaendert.split(',')[-1])
            if letzter_nutzer != 0:
                self.nutzer_geaendert += ', 0'
        
        super().save(**kwargs)

    class Meta:
        abstract = True
        ordering = ["-zeit_geaendert"]

    def __str__(self):
        return '{model}, geändert {zeit}'.format(
            model=self.__class__.__name__,
            zeit=str(self.zeit_geaendert),
        )


class Grundklasse(MinimalModel):
    """ Klasse für Objekte, die detail-view haben können """
    name = models.CharField(max_length=99)
    slug = models.SlugField(
        max_length=99,
        null=False,
        blank=True,
    )

    def save(self, **kwargs):
        """ Falls nicht gesetzt, slug autoausfüllen """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(**kwargs)

    class Meta:
        abstract = True
        ordering = ["name"]

    def get_absolute_url(self):
        """ Sollte überschrieben werden, für den Notfall so: """
        return '/{model}/{slug}/'.format(
            model=self.__class__.__name__.lower(),
            slug=self.slug,
        )

    def __str__(self):
        return str(self.name)


# Nutzer und Profile
from django.contrib.auth.models import AbstractUser
from userena.models import UserenaBaseProfile
from django.urls import reverse
import random, string

def knoepfe_kopf(user):
    """ gibt Knöpfe für Kopfleiste als Liste von Tupeln zurück """
    spam = ('spam', 'spam') 
    admin = ('/admin/', 'admin')
    anmelden = (reverse('userena_signin'), 'Anmelden')
    abmelden = (reverse('userena_signout'), 'Abmelden')
    register = (reverse('userena_signup'), 'Registrieren')
    profil = lambda nutzer: (reverse('userena_profile_edit', kwargs={'username':nutzer.username}), 'Profil')
    
    if user.username == 'admin':
        liste = [spam]        
    elif user.is_authenticated():
        liste = [abmelden, profil(user)]
    else:
        liste = [anmelden, register]
    if user.is_staff and user.get_all_permissions():
        liste.append(admin)
    
    return liste

def knoepfe_menü(user):
    """ gibt Knöpfe für Menüleiste als Liste von Tupeln zurück """
    alle = {
        'index': ('/', 'Startseite'), 
        'db': ('https://olymp.piokg.de/static/db.pdf', 'Datenbanklayout'), # quick and very dirty :)
        'todo': ('/todo/', 'ToDo-Liste'),
        'olymp': ('/olymp/', 'Wettbewerbe'),
    }
    
    if user.username == 'admin':
        return [alle[name] for name in ('olymp', 'index', 'todo', 'db')]
    else:
        return [alle[name] for name in ('olymp', 'index', 'db')]
        

class Nutzer(AbstractUser, MinimalModel):
    """ Nutzer-Klasse """
    def knoepfe_kopf(nutzer):
        """ soll Liste von Paaren für Knöpfe der Kopfleiste ausgeben 
        Nutzt im Moment die module-fkt gleichen Namens, könnte später vll
        die Gruppenzugehörigkeit heranziehen, etc, ist flexibel """
        return knoepfe_kopf(nutzer)

    def knoepfe_menü(self):
        """ soll Liste von Paaren für Knöpfe der Menüleiste ausgeben 
        Nutzt im Moment die module-fkt gleichen Namens, könnte später vll
        die Gruppenzugehörigkeit heranziehen, etc, ist flexibel """
        return knoepfe_menü(self)

    def save(self, *args, **kwargs):
        """ setzt bei Bedarf zufälligen Nutzernamen """
        if not self.username:
            self.username = ''.join(random.sample(string.ascii_lowercase, 20))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Nutzer'
        verbose_name = 'Nutzer'

    def __str__(self):
        return 'Nutzer %s (%s)' % (self.username, self.email)


class Profil(UserenaBaseProfile):
    user = models.OneToOneField(
        Nutzer,
        unique=True,
        verbose_name='Nutzer',
        related_name='profil',
    )

    @property
    def nutzer(self): # DB-Feld heißt user weil userena's sonst nicht versteht
        return self.user

    class Meta:
        verbose_name_plural = 'Profile'
        verbose_name = 'Nutzerprofil'
