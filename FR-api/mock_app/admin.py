from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export import resources

from .models import MockAIPayload


class MockAIPayloadResource(resources.ModelResource):
    class Meta:
        model = MockAIPayload
        skip_unchanged = True
        report_skipped = True


@admin.register(MockAIPayload)
class MockAIPayloadAdmin(ImportExportModelAdmin):
    resource_class = MockAIPayloadResource
    list_display = ('timestamp', 'incident_id', 'camera', 'status')
    list_filter = ('status', 'camera')
    search_fields = ('incident_id',)
