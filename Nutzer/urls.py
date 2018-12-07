from django.urls import path, include

from .views import UpdateEmailView, CreateUserView, ProfileView
from authtools.views import LoginView, LogoutView

from vanilla import TemplateView#, UpdateView, DetailView
from Nutzer.models import Nutzerprofil

app_name = 'Nutzer'

auth_urls = ([
    path('registrieren/', CreateUserView.as_view(), name='registrieren'),
    path('anmelden/', 
        LoginView.as_view(template_name='Nutzer/anmelden.html', success_url='/'), 
        name='anmelden'),
    path('abmelden/',
        LogoutView.as_view(template_name='Nutzer/abgemeldet.html', success_url='/'),
        name='abmelden'),
    path('/', include('authtools.urls'))
], 'auth')

profil_urls = ([
    path('meine_daten/', ProfileView.as_view(), name='meine_daten'),
    path('mail_wurde_versandt/', TemplateView.as_view(template_name='Nutzer/info_mail_versandt.html'), name='mail_wurde_versandt'),
    path('meine_email_aendern/', UpdateEmailView.as_view(), name='email_aendern'),
    #path('<pk>/', DetailView.as_view(model=Nutzerprofil, template_name='Nutzer/profil.html'), name='profilansicht'),
], 'Nutzer')

