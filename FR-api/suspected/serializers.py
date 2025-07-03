from rest_framework import serializers
from .models import SuspectedMatch

class SuspectedMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspectedMatch
        fields = [
            'id', 'person', 'camera_id', 'timestamp',
            'snapshot', 'video_clip', 'notes', 'created_at'
        ]
