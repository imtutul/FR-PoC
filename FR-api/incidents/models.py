from django.db import models
from django.utils import timezone
from datetime import timedelta
from persons_of_interest.models import PersonOfInterest
from employees.models import Employee
from suspected.models import Suspect 


def _media_path(kind: str, incident_id: str, filename: str) -> str:
    return f"incidents/{incident_id}/{kind}/{filename}"


def suspect_img_path(instance, filename):
    return _media_path("suspects", instance.incident.incident_id, filename)


def association_img_path(instance, filename):
    return _media_path("associations", instance.incident.incident_id, filename)


def association_vid_path(instance, filename):
    return _media_path("associations/videos", instance.incident.incident_id, filename)


class Incident(models.Model):
    incident_id = models.CharField(max_length=100, unique=True, db_index=True)
    camera_id = models.CharField(max_length=50)
    zone = models.CharField(max_length=50, blank=True)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    status = models.CharField(max_length=10, default="open")
    video_clip = models.CharField(max_length=255, blank=True, null=True)
    finalised = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-time_start"]

    def __str__(self):
        return f"Incident {self.incident_id} ({self.status})"

    def touch(self, new_ts):
        self.time_end = new_ts
        self.save(update_fields=["time_end", "updated_at"])

    def auto_close_if_idle(self, minutes: int = 10):
        if not self.finalised and timezone.now() > self.time_end + timedelta(minutes=minutes):
            self.finalised = True
            self.status = "close"
            self.save(update_fields=["finalised", "status", "updated_at"])


class POIMatch(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="poi_matches")
    poi = models.ForeignKey(PersonOfInterest, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    capture_no = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]


class SuspectedMatch(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="suspects")
    suspect = models.ForeignKey(Suspect, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=255)
    video_clip = models.CharField(max_length=255, blank=True, null=True)
    capture_no = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]


class EmployeeAssociationLog(models.Model):
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="associations")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    suspect_id = models.CharField(max_length=100, blank=True)
    image_path = models.CharField(max_length=255)
    video_clip = models.CharField(max_length=255, blank=True, null=True)
    capture_no = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]
