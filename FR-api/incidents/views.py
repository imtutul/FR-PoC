from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.dateparse import parse_datetime
from .models import Incident, POIMatch, SuspectedMatch, EmployeeAssociationLog
from persons_of_interest.models import PersonOfInterest
from employees.models import Employee
from suspected.models import Suspect
from .serializers import IncidentSerializer


class IncidentListView(generics.ListAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class IncidentDetailView(generics.RetrieveAPIView):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer


class AILogView(APIView):
    def post(self, request):
        data = request.data
        try:
            inc_id = data["incident_id"]
            ts = parse_datetime(data["timestamp"])
            camera = data["camera"]
            image = data["img"]
            video = data.get("video_clip", "")
            capture_no = data.get("capture_no", None)
            status_flag = data.get("status", "open")

            incident, created = Incident.objects.get_or_create(
                incident_id=inc_id,
                defaults={
                    "camera_id": camera,
                    "time_start": ts,
                    "time_end": ts,
                    "status": status_flag,
                },
            )
            if not created:
                incident.touch(ts)
                incident.status = status_flag

            if status_flag == "close" or video:
                incident.finalised = True
                incident.status = "close"
            incident.save()

            for poi_id in data.get("poi_id", []):
                try:
                    poi = PersonOfInterest.objects.get(id=poi_id)
                    POIMatch.objects.create(
                        incident=incident,
                        poi=poi,
                        capture_no=capture_no,
                        image_path=image,
                        timestamp=ts,
                    )
                except PersonOfInterest.DoesNotExist:
                    continue

            for sid in data.get("suspect_id", []):
                suspect, _ = Suspect.objects.get_or_create(id=sid)
                SuspectedMatch.objects.create(
                    incident=incident,
                    suspect=suspect,
                    capture_no=capture_no,
                    image_path=image,
                    video_clip=video,
                    timestamp=ts,
                )

            for eid in data.get("assotiate_id", []):
                try:
                    emp = Employee.objects.get(id=eid)
                    EmployeeAssociationLog.objects.create(
                        incident=incident,
                        employee=emp,
                        capture_no=capture_no,
                        image_path=image,
                        video_clip=video,
                        timestamp=ts,
                    )
                except Employee.DoesNotExist:
                    continue

            return Response({"message": "AI log processed"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)