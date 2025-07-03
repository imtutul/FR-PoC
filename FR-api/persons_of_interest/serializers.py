from rest_framework import serializers
from .models import PersonOfInterest, PersonOfInterestImage

class PersonOfInterestImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)   # return full URL

    class Meta:
        model = PersonOfInterestImage
        fields = ['id', 'image']

class PersonOfInterestSerializer(serializers.ModelSerializer):
    # READ‑ONLY list of saved images
    images = PersonOfInterestImageSerializer(many=True, read_only=True)

    # WRITE‑ONLY list of files when creating/updating
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = PersonOfInterest
        fields = [
            'id', 'name', 'threat_level', 'notes',
            'images',          # returned on GET
            'upload_images'    # accepted on POST/PUT
        ]

    # Create with bulk images
    def create(self, validated_data):
        files = validated_data.pop('upload_images', [])
        poi = PersonOfInterest.objects.create(**validated_data)
        for f in files:
            PersonOfInterestImage.objects.create(person=poi, image=f)
        return poi
