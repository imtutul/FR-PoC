from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime

from persons_of_interest.models import PersonOfInterest
from employees.models import Employee
from .models import Incident, SuspectedMatch, EmployeeAssociationLog
from .serializers import (
    IncidentSerializer,
    SuspectedMatchSerializer,
    EmployeeAssociationSerializer,
)


# ── Standard CRUD endpoints ──────────────────────────────────────────
class IncidentListView(generics.ListAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class IncidentDetailView(generics.RetrieveAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


# ── AI callback endpoint ─────────────────────────────────────────────
class AILogView(APIView):
    """
    Accepts the AI payloads you described and stores/updates an Incident.
    """

    def post(self, request):
        data = request.data

        # 1) Parse / get-or-create Incident
        inc_id = data["incident_id"]
        ts_now = parse_datetime(data["time_now"])
        poi = PersonOfInterest.objects.get(id=data["poi_id"])

        incident, created = Incident.objects.get_or_create(
            incident_id=inc_id,
            defaults=dict(
                poi=poi,
                camera_id=data["camera_sn"],
                time_start=ts_now,
                time_end=ts_now,
            ),
        )
        if not created:
            incident.touch(ts_now)

        # 2) Store POI snapshot (optional)
        if "image" in data:
            SuspectedMatch.objects.create(
                incident=incident,
                external_id=data["poi_id"],
                camera_id=data["camera_sn"],
                time_start=ts_now,
                time_end=ts_now,
                snapshot=data["image"],
                video_clip=data.get("video_clip"),
                movement=data.get("movement"),
            )

        # 3) Handle suspect_log bulk
        for item in data.get("incident_details", []):
            SuspectedMatch.objects.create(
                incident=incident,
                external_id=item["suspect_id"],
                camera_id=item["camera_sn"],
                time_start=parse_datetime(item["time_start"]),
                time_end=parse_datetime(item["time_end"]),
                snapshot=item["image"],
                video_clip=item.get("video_clip"),
                movement=item.get("movement"),
            )

        # 4) Handle employee_association_log
        if data.get("employee_id"):
            EmployeeAssociationLog.objects.create(
                incident=incident,
                employee=Employee.objects.get(id=data["employee_id"]),
                suspect_id=data["assosicated_suspect_id"],
                camera_id=data["camera_sn"],
                time_start=parse_datetime(data["time_start"]),
                time_end=parse_datetime(data["time_end"]),
                snapshot=data["image"],
                video_clip=data.get("video_clip"),
                movement=data.get("movement"),
            )

        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
