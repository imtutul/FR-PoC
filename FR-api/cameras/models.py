from django.db import models
from zones.models import Zone

class Camera(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name