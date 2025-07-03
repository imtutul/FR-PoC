from django.contrib import admin
from .models import Incident, SuspectedMatch, EmployeeAssociationLog


class SuspectedMatchInline(admin.TabularInline):
    model = SuspectedMatch
    extra = 0
    readonly_fields = ['external_id', 'camera_id', 'time_start', 'time_end', 'snapshot', 'video_clip', 'movement', 'created_at']
    can_delete = False


class EmployeeAssociationInline(admin.TabularInline):
    model = EmployeeAssociationLog
    extra = 0
    readonly_fields = ['employee', 'suspect_id', 'camera_id', 'time_start', 'time_end', 'snapshot', 'video_clip', 'movement', 'created_at']
    can_delete = False


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('incident_id', 'poi', 'camera_id', 'time_start', 'time_end', 'finalised', 'created_at')
    search_fields = ('incident_id', 'poi__name', 'camera_id')
    list_filter = ('finalised', 'camera_id', 'poi__threat_level')
    inlines = [SuspectedMatchInline, EmployeeAssociationInline]


admin.site.register(SuspectedMatch)
admin.site.register(EmployeeAssociationLog)
