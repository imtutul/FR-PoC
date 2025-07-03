from django.db import models
from django.utils import timezone
from datetime import timedelta
from persons_of_interest.models import PersonOfInterest
from employees.models import Employee

def suspect_snapshot_path(instance, filename):
    return _media_path('suspects', instance.incident.incident_id, filename)

def suspect_video_path(instance, filename):
    return _media_path('suspects', instance.incident.incident_id, filename)

def association_snapshot_path(instance, filename):
    return _media_path('associations', instance.incident.incident_id, filename)

def association_video_path(instance, filename):
    return _media_path('associations/videos', instance.incident.incident_id, filename)



class Incident(models.Model):
    """
    One 10‑minute envelope around a primary POI detection.
    """

    incident_id = models.CharField(max_length=100, unique=True, db_index=True)
    poi = models.ForeignKey(PersonOfInterest, on_delete=models.CASCADE)
    camera_id = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    finalised = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-time_start"]

    def __str__(self):
        return f"Incident {self.incident_id} – {self.poi.name}"

    # extend the window when new evidence arrives
    def touch(self, new_ts):
        self.time_end = new_ts
        self.save(update_fields=["time_end", "updated_at"])

    # mark as done once idle for >10 min
    def check_auto_close(self):
        if not self.finalised and timezone.now() > self.time_end + timedelta(
            minutes=10
        ):
            self.finalised = True
            self.save(update_fields=["finalised"])


def _media_path(kind, incident_id, filename):
    return f"suspected/{incident_id}/{kind}/{filename}"


class SuspectedMatch(models.Model):
    incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name="suspects"
    )
    external_id = models.CharField(max_length=100)  # AI's suspect ID
    camera_id = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    snapshot = models.ImageField(upload_to=suspect_snapshot_path)
    video_clip = models.FileField(upload_to=suspect_video_path, blank=True, null=True)
    movement = models.CharField(max_length=10, blank=True, null=True)  # in / out
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_start"]

    def __str__(self):
        return f"Suspect {self.external_id} in {self.incident.incident_id}"


class EmployeeAssociationLog(models.Model):
    incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name="associations"
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    suspect_id = models.CharField(max_length=100)  # AI's suspect ID
    camera_id = models.CharField(max_length=100)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    snapshot = models.ImageField(upload_to=association_snapshot_path)
    video_clip = models.FileField(upload_to=association_video_path, blank=True, null=True)
    movement = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_start"]

    def __str__(self):
        return f"Emp {self.employee.id} ↔ Sus {self.suspect_id} in {self.incident.incident_id}"
