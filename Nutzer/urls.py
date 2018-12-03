from django.urls import path

from .views import UpdateProfileView, UpdateEmailView, CreateUserView, CreateProfileView, ProfileView, CreatedUserView
from authtools.views import LoginView, LogoutView

from vanilla.model_views import UpdateView, DetailView
from Nutzer.models import Nutzerprofil

app_name = 'Nutzer'

auth_urls = ([
    path('registrieren/', CreateUserView.as_view(), name='registrieren'),
    path('anmelden/', 
        LoginView.as_view(template_name='Nutzer/anmelden.html', success_url='/'), 
        name='anmelden'),
    path('abmelden/',
        LogoutView.as_view(success_url='/'),
        name='abmelden'),
], 'Nutzer')

profil_urls = ([
    path('meine_daten/', ProfileView.as_view(), name='meine_daten'),
    path('<pk>/', DetailView.as_view(model=Nutzerprofil, template_name='Nutzer/profil.html'), name='profilansicht'),
], 'Nutzer')

