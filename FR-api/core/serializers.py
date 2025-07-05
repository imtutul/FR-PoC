from rest_framework import serializers
from datetime import timezone as dt_timezone
from .models import Human, Image, Incident

class AIWebhookSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    camera = serializers.CharField()
    incident_id = serializers.CharField()
    associate_id = serializers.ListField(child=serializers.CharField(), default=list)
    suspect_id  = serializers.ListField(child=serializers.CharField(), default=list)
    poi_id      = serializers.ListField(child=serializers.CharField(), default=list)
    img = serializers.URLField()
    video_clip = serializers.URLField(allow_blank=True, required=False)
    capture_no = serializers.CharField(required=False, allow_blank=True)
    status = serializers.IntegerField()   # 0 = closed, 1 = open

    def validate_status(self, value):
        if value not in (0, 1):
            raise serializers.ValidationError("Status must be 0 (Closed) or 1 (Open).")
        return value



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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image_url", "image_type", "added_on"]

class HumanSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True, source="image_set")

    class Meta:
        model = Human
        fields = [
            "id",
            "name",
            "profile_pic",
            "email",
            "phone",
            "details",
            "human_type",
            "created_on",
            "updated_on",
            "images",
        ]


class HumanImageURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_url', 'image_type']


class HumanCreateWithImagePathsSerializer(serializers.ModelSerializer):
    images = HumanImageURLSerializer(many=True, required=False)

    class Meta:
        model = Human
        fields = ['name', 'profile_pic', 'email', 'phone', 'details', 'images']

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        validated_data['human_type'] = self.context['human_type']
        human = Human.objects.create(**validated_data)

        for image in images_data:
            Image.objects.create(human=human, **image)

        return human
    

class ImageCreateSerializer(serializers.ModelSerializer):
    # Accept either human ID or incident ID to attach the image
    human = serializers.PrimaryKeyRelatedField(queryset=Human.objects.all(), required=False, allow_null=True)
    incident = serializers.PrimaryKeyRelatedField(queryset=Incident.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Image
        fields = ['image_url', 'image_type', 'human', 'incident']

    def validate(self, data):
        # Require at least human or incident to be present
        if not data.get('human') and not data.get('incident'):
            raise serializers.ValidationError("Either 'human' or 'incident' must be provided.")
        return data
    