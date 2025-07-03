from rest_framework import serializers
from .models import Incident, POIMatch, SuspectedMatch, EmployeeAssociationLog
from suspected.serializers import SuspectSerializer
from suspected.models import Suspect


class SuspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suspect
        fields = "__all__"


class SuspectedMatchSerializer(serializers.ModelSerializer):
    suspect = SuspectSerializer(read_only=True) 

    class Meta:
        model = SuspectedMatch
        fields = '__all__'


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
            "camera_id",
            "zone",
            "time_start",
            "time_end",
            "status",
            "video_clip",
            "finalised",
            "created_at",
            "updated_at",
            "suspects",
            "associations",
        ]
