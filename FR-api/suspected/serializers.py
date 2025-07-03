from rest_framework import serializers
from .models import Incident, SuspectedMatch, EmployeeAssociationLog

class SuspectedMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuspectedMatch
        fields = "__all__"


class EmployeeAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAssociationLog
        fields = "__all__"


class IncidentSerializer(serializers.ModelSerializer):
    suspects = SuspectedMatchSerializer(many=True, read_only=True)
    associations = EmployeeAssociationSerializer(many=True, read_only=True)

    class Meta:
        model = Incident
        fields = [
            "id",
            "incident_id",
            "poi",
            "camera_id",
            "time_start",
            "time_end",
            "finalised",
            "suspects",
            "associations",
        ]
