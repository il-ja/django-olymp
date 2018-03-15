from django.conf.urls import url, include
from . import views

app_name = 'Kommentare'

urlpatterns = [
    url(r'^erstellen/(?P<pk>[\w-]+)/$',
        views.NeuerKommentar.as_view(), 
        name='erstellen',
    ),
]
