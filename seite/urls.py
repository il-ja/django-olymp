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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from Grundgeruest import views as grundgeruest

slug_nutzer = settings.SLUG_NUTZER
urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^' + slug_nutzer, include('userena.urls')),
    url(r'^olymp/', include('Wettbewerbe.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^kommentare/', include('Kommentare.urls')),
    url(r'^$',
        grundgeruest.IndexView.as_view(
            template_name='Grundgeruest/startseite.html'
        ),
        name='startseite',
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
