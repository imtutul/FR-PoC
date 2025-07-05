from django.db import models
from django.utils.timezone import now

class Human(models.Model):
    EMPLOYEE = 0
    PERSON_OF_INTEREST = 1
    SUSPECTED = 2
    
    HUMAN_TYPE_CHOICES = (
        (EMPLOYEE, 'Employee'),
        (PERSON_OF_INTEREST, 'Person of Interest'),
        (SUSPECTED, 'Suspected'),
    )
    
    human_type = models.IntegerField(choices=HUMAN_TYPE_CHOICES)
    name = models.CharField(max_length=255, null=True, blank=True)
    profile_pic = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.get_human_type_display()}: {self.name or 'Unknown'}"

class Image(models.Model):
    PROFILE_IMAGE = 0
    INCIDENT_IMAGE = 1
    
    IMAGE_TYPE_CHOICES = (
        (PROFILE_IMAGE, 'Profile Image'),
        (INCIDENT_IMAGE, 'Incident Image'),
    )
    
    human = models.ForeignKey(Human, on_delete=models.CASCADE, null=True, blank=True)
    image_url = models.URLField()
    image_type = models.IntegerField(choices=IMAGE_TYPE_CHOICES)
    added_on = models.DateTimeField(auto_now_add=True)
    incident = models.ForeignKey('Incident', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.image_url


class Incident(models.Model):
    STATUS_CHOICES = (
        (0, 'Closed'),
        (1, 'Open'),
    )

    start_on = models.DateTimeField(default=now)
    end_on = models.DateTimeField(null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    humans = models.ManyToManyField("Human", blank=True, related_name="incidents")
    video_clip = models.URLField(null=True, blank=True)
    best_image = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Incident {self.id} ({self.get_status_display()})"


class IncidentDetail(models.Model):
    STATUS_CHOICES = (
        (0, 'Closed'),
        (1, 'Open'),
    )

    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name="details")
    timestamp = models.DateTimeField(default=now)
    status = models.IntegerField(choices=STATUS_CHOICES)
    humans = models.ManyToManyField("Human", blank=True, related_name="incident_details")
    image = models.URLField()

    def __str__(self):
        return f"Detail at {self.timestamp} for Incident {self.incident_id}"