from django.contrib import admin

from . import models
from django.contrib import admin
from django.contrib.admin.models import LogEntry

admin.site.register(models.Nutzerprofil)
admin.site.register(models.Nutzerzugang)

class LogEntryAdmin(admin.ModelAdmin):
    pass
#    list_display = ('user__email', 'content_type', 'object_repr', 'action_time')
#
#    readonly_fields = (
#        'content_type',
#        'user',
#        'action_time',
#        'object_id',
#        'object_repr',
#        'action_flag',
#        'change_message'
#    )
#
#    def has_delete_permission(self, request, obj=None):
#        return False
#
#    def get_actions(self, request):
#        actions = super(LogEntryAdmin, self).get_actions(request)
#        del actions['delete_selected']
#        return actions

admin.site.register(LogEntry, LogEntryAdmin)
