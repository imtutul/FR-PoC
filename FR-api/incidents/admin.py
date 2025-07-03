from django.contrib import admin
from .models import Incident, POIMatch, SuspectedMatch, EmployeeAssociationLog


class POIMatchInline(admin.TabularInline):
    model = POIMatch
    extra = 0
    readonly_fields = ('poi', 'image_path', 'capture_no', 'timestamp')
    can_delete = False


class SuspectedMatchInline(admin.TabularInline):
    model = SuspectedMatch
    extra = 0
    readonly_fields = ('suspect', 'image_path', 'video_clip', 'capture_no', 'timestamp')
    can_delete = False


class EmployeeAssociationInline(admin.TabularInline):
    model = EmployeeAssociationLog
    extra = 0
    readonly_fields = ('employee', 'suspect_id', 'image_path', 'video_clip', 'capture_no', 'timestamp')
    can_delete = False


@admin.register(Incident)
class IncidentAdmin(admin.ModelAdmin):
    list_display = ('incident_id', 'camera_id', 'time_start', 'time_end', 'status', 'finalised')
    search_fields = ('incident_id', 'camera_id', 'status')
    list_filter = ('status', 'finalised')
    inlines = [POIMatchInline, SuspectedMatchInline, EmployeeAssociationInline]
