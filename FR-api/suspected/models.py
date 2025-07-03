from django.db import models

def suspect_image_path(instance, filename):
    return f'suspect_images/{instance.suspect.id}/{filename}'


class Suspect(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.id}"


class SuspectImage(models.Model):
    suspect = models.ForeignKey(Suspect, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=suspect_image_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.suspect.name} - {self.suspect.id}"
