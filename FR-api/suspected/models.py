from django.db import models
from persons_of_interest.models import PersonOfInterest
from employees.models import Employee  # Optional, if correlated later

def snapshot_upload_path(instance, filename):
    return f'suspected/{instance.id}/snapshots/{filename}'

def video_upload_path(instance, filename):
    return f'suspected/{instance.id}/videos/{filename}'

class SuspectedMatch(models.Model):
    person = models.ForeignKey(PersonOfInterest, on_delete=models.CASCADE)
    camera_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    snapshot = models.ImageField(upload_to=snapshot_upload_path)
    video_clip = models.FileField(upload_to=video_upload_path, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SuspectedMatch: {self.person.name} at {self.timestamp}"
