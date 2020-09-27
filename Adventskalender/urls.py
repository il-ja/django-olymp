from django.conf.urls import url, include
from Kommentare import views

app_name = 'Kommentare'

urlpatterns = [
    url(r'^erstellen/(?P<pk>[\w-]+)/$',
        views.NeuerKommentar.as_view(), 
        name='erstellen',
    ),
    url(r'^editieren/(?P<pk>[\w-]+)/$',
        views.KommentarEditieren.as_view(),
        name='editieren',
    ),
    url(r'^loeschen/(?P<pk>[\w-]+)/$',
        views.KommentarLoeschen.as_view(),
        name='loeschen',
    ),
]
