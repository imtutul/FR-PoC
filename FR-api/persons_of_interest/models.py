from django.db import models

def poi_image_path(instance, filename):
    return f'poi_images/{instance.person.id}/{filename}'

class PersonOfInterest(models.Model):
    name = models.CharField(max_length=100)
    threat_level = models.CharField(max_length=50)  # e.g., "low", "medium", "high"
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.threat_level}"

class PersonOfInterestImage(models.Model):
    person = models.ForeignKey(PersonOfInterest, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=poi_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
