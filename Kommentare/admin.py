from django.contrib import admin
from django.db import models as django_models

from martor.widgets import AdminMartorWidget

from . import models

class KommentarAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django_models.TextField: {'widget': AdminMartorWidget},
    }

class KommentareInline(admin.TabularInline):
    model = models.Kommentar
    fields = ('autor', 'text')
    extra = 1


class ListeAdmin(admin.ModelAdmin):
    inlines = [KommentareInline]

admin.site.register(models.Kommentar, KommentarAdmin)
admin.site.register(models.Liste, ListeAdmin)

