from rest_framework import serializers
from .models import Suspect, SuspectImage


class SuspectImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = SuspectImage
        fields = ['id', 'image', 'uploaded_at']


class SuspectSerializer(serializers.ModelSerializer):
    images = SuspectImageSerializer(many=True, read_only=True)

    # Optional image upload while creating
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Suspect
        fields = [
            'id', 'name', 'notes',
            'images',          # for GET
            'upload_images'    # for POST/PUT
        ]

    def create(self, validated_data):
        files = validated_data.pop('upload_images', [])
        suspect = Suspect.objects.create(**validated_data)
        for f in files:
            SuspectImage.objects.create(suspect=suspect, image=f)
        return suspect
