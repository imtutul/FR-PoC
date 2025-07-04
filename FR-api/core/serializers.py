from rest_framework import serializers
from datetime import timezone as dt_timezone
from .models import Human

class AIWebhookSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    camera = serializers.CharField()
    incident_id = serializers.CharField()
    associate_id = serializers.ListField(child=serializers.CharField(), default=list)
    suspect_id = serializers.ListField(child=serializers.CharField(), default=list)
    poi_id = serializers.ListField(child=serializers.CharField(), default=list)
    img = serializers.URLField()
    video_clip = serializers.URLField(allow_blank=True, required=False)
    capture_no = serializers.CharField(required=False, allow_blank=True)
    status = serializers.IntegerField()

    def validate_status(self, value):
        if value not in [0, 1]:
            raise serializers.ValidationError("Status must be 0 (Closed) or 1 (Open)")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['status'] = "open" if data['status'] == 1 else "closed"
        return data

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        # Convert integer status to string to match model expectations
        ret['status'] = "open" if ret['status'] == 1 else "closed"
        return ret



class SuspectCreateSerializer(serializers.Serializer):
    image_url = serializers.URLField(required=True)
    camera_id = serializers.CharField(required=False, allow_null=True)
    detected_at = serializers.DateTimeField(required=False, default_timezone=dt_timezone.utc)



class SuspectResponseSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Human
        fields = ['id', 'name', 'profile_pic', 'human_type', 'type_display', 'created_on']
        read_only_fields = fields