from django.contrib import admin
from .models import PersonOfInterest, PersonOfInterestImage

admin.site.register(PersonOfInterest)
admin.site.register(PersonOfInterestImage)