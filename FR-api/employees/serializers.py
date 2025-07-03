from rest_framework import serializers
from .models import Employee, EmployeeImage

class EmployeeImageSerializer(serializers.ModelSerializer):
    # ensure URLs returned, not just relative paths
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = EmployeeImage
        fields = ['id', 'image']

class EmployeeSerializer(serializers.ModelSerializer):
    images = EmployeeImageSerializer(many=True, read_only=True)

    # write‑only field: incoming files for CREATE / ADD‑IMAGES
    upload_images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Employee
        fields = ['id', 'name', 'designation', 'images', 'upload_images']

    def create(self, validated_data):
        files = validated_data.pop('upload_images', [])
        employee = Employee.objects.create(**validated_data)
        for file in files:
            EmployeeImage.objects.create(employee=employee, image=file)
        return employee
