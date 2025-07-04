from django.db import models
from django.utils import timezone


class MockAIPayload(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    zone = models.CharField(max_length=10)
    camera = models.CharField(max_length=10)
    incident_id = models.CharField(max_length=100)

    assotiate_id = models.JSONField(default=list, blank=True)
    suspect_id = models.JSONField(default=list, blank=True)
    poi_id = models.JSONField(default=list, blank=True)

    img = models.CharField(max_length=255)
    video_clip = models.CharField(max_length=255, blank=True, null=True)
    capture_no = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, default="open")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mock AI Data ({self.incident_id}) @ {self.timestamp}"
