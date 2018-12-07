import logging
logger = logging.getLogger(__name__)

from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.urls import reverse
from django.conf import settings
import random
import string
from authtools.models import AbstractEmailUser
from django.contrib import auth

def knoepfe_kopf(user):
    """ gibt Knöpfe für Kopfleiste als Liste von Tupeln zurück """
    spam = ('spam', 'spam') 
    admin = ('/admin/', 'admin')
    anmelden = (reverse('auth:anmelden'), 'Anmelden')
    abmelden = (reverse('auth:abmelden'), 'Abmelden')
    register = (reverse('auth:registrieren'), 'Registrieren')
    profil = (reverse('Nutzer:meine_daten'), 'Profil')
    
    if user.is_authenticated:
        liste = [abmelden, profil]
    else:
        liste = [anmelden, register]
    if user.is_staff and user.get_all_permissions():
        liste.append(admin)
    
    return liste

def knoepfe_menü(user):
    """ gibt Knöpfe für Menüleiste als Liste von Tupeln zurück """
    links = {
        'index': ('/', 'Startseite'), 
        'db': ('/static/Grundgeruest/db_olymp.pdf', 'Datenbanklayout'), # quick and very dirty :)
        'todo': ('/todo/', 'ToDo-Liste'),
        'olymp': ('/olymp/', 'Wettbewerbe'),
        'impressum': ('/impressum/', 'Impressum'),
        'randomus': ('/linkus-randomus/', 'linkus randomus'),
    }

    if user.is_superuser:
        return [links[name] for name in ('olymp', 'db', 'todo', 'impressum')]
    else:
        return [links[name] for name in ('olymp', 'impressum', 'randomus')]


class Nutzerzugang(AbstractEmailUser, TimeStampedModel):
    """ Klasse für den Nutzer, das was get_user_model() ausspuckt.
    Zuständig für Authentifikation (Mail+Passwort) und permissions """

    def send_activation_mail(self):
        # PW reset mail won't be send when password is None
        if not self.password:
            self.set_password(random.sample(string.ascii_lowercase, 6))
            self.save()

        reset_form = auth.forms.PasswordResetForm({'email': self.email})
        if not reset_form.is_valid():
            logger.error('Sending of activation mail to {} failed: {}'.format(self.email, reset_form.errors))
        reset_form.save(
            subject_template_name='Nutzer/mail_registrieren_betreff.txt',
            email_template_name='Nutzer/mail_registrieren_email.html',
            from_email=settings.EMAIL_HOST_USER)
        logger.info('Activation email send to {}'.format(self.email))

    class Meta(AbstractEmailUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Nutzerzugang'
        verbose_name_plural = 'Nutzerzugänge'

    def knoepfe_kopf(self):
        """ soll Liste von Paaren für Knöpfe der Kopfleiste ausgeben 
        Nutzt im Moment die module-fkt gleichen Namens, könnte später vll
        die Gruppenzugehörigkeit heranziehen, etc, ist flexibel """
        return knoepfe_kopf(self)

    def knoepfe_menü(self):
        """ soll Liste von Paaren für Knöpfe der Menüleiste ausgeben 
        Nutzt im Moment die module-fkt gleichen Namens, könnte später vll
        die Gruppenzugehörigkeit heranziehen, etc, ist flexibel """
        return knoepfe_menü(self)

    def __str__(self):
        return 'Nutzer %s' % self.email


class Nutzerprofil(TimeStampedModel):
    nutzer = models.OneToOneField(
        Nutzerzugang,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name='Nutzerzugang',
        related_name='profil',
    )
    anrede_choices = [('m', 'Herr'), ('w', 'Frau'), ('', 'N/A')]
    farbschema_choices = [
        ('/static/Grundgeruest/css/w3-theme-amber.css', 'Zeus'),
        ('/static/Grundgeruest/css/w3-theme-blue.css', 'Poseidon'),
        ('/static/Grundgeruest/css/w3-theme-indigo.css', 'Hera'),
        ('/static/Grundgeruest/css/w3-theme-brown.css', 'Demeter'),
        ('/static/Grundgeruest/css/w3-theme-yellow.css', 'Apollo'),
        ('/static/Grundgeruest/css/w3-theme-light-green.css', 'Artemis'),
        ('/static/Grundgeruest/css/w3-theme-dark-grey.css', 'Athene'),
        ('/static/Grundgeruest/css/w3-theme-red.css', 'Ares'),
        ('/static/Grundgeruest/css/w3-theme-pink.css', 'Aphrodite'),
        ('/static/Grundgeruest/css/w3-theme-grey.css', 'Hermes'),
        ('/static/Grundgeruest/css/w3-theme-orange.css', 'Hephaistos'),
        ('/static/Grundgeruest/css/w3-theme-cyan.css', 'Dionysus')
    ]

    anrede = models.CharField(
        max_length=1,
        choices=anrede_choices,
        default='',
    )
    vorname = models.CharField(max_length=99)
    nachname = models.CharField(max_length=99)
    strasse = models.CharField(max_length=99)
    plz = models.CharField(max_length=5)
    stadt = models.CharField(max_length=99)
    farbschema = models.CharField(
	max_length=255,
	choices=farbschema_choices,
	default='/static/Grundgeruest/css/w3-theme-dark-grey.css'
    )

    class Meta:
        verbose_name_plural = 'Profile'
        verbose_name = 'Nutzerprofil'
