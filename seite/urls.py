"""seite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.views.generic import TemplateView
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from Nutzer.urls import auth_urls, profil_urls
from Grundgeruest import views as grundgeruest

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^auth2/', include('authtools.urls')),
    url(r'^auth/', include(auth_urls)),
    url(r'^nutzer/', include(profil_urls)),
    url(r'^olymp/', include('Wettbewerbe.urls')),
    url(r'^martor/', include('martor.urls')),
    url(r'^kommentare/', include('Kommentare.urls')),
    url(r'^impressum/$', TemplateView.as_view(template_name="impressum.html"), name='startseite'),
    url(r'^linkus-randomus/$', grundgeruest.RandomusView.as_view(), name='linkus-randomus'),
    url(r'^$', grundgeruest.IndexView.as_view(), name='startseite'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
