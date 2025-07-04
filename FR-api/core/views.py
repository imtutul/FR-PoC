from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from .models import Human, Image, Incident, IncidentDetail
from .serializers import AIWebhookSerializer, SuspectCreateSerializer, SuspectResponseSerializer
from rest_framework.generics import CreateAPIView


class AIWebhookView(APIView):
    def post(self, request):
        serializer = AIWebhookSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Combine all human IDs
        all_human_ids = data['associate_id'] + data['suspect_id'] + data['poi_id']
        human_queryset = Human.objects.filter(id__in=all_human_ids)

        with transaction.atomic():
            # Get or create incident
            incident, created = Incident.objects.get_or_create(
                id=data['incident_id'],
                defaults={
                    'start_on': data['timestamp'],
                    'status': "open"
                }
            )

            # If not newly created, and human set needs updating
            if not created:
                incident.humans.add(*human_queryset)

            # If status == closed, update incident info
            if data['status'] == "closed" or data['status'] == 0:
                incident.status = "closed"
                incident.end_on = data['timestamp']
                incident.video_clip = data.get('video_clip', '')
                incident.best_image = data['img']
                incident.save()

            else:
                incident.humans.add(*human_queryset)

            # Create incident detail
            detail = IncidentDetail.objects.create(
                incident=incident,
                timestamp=data['timestamp'],
                status=data['status'],
                image=data['img']
            )
            detail.humans.add(*human_queryset)

            # Create image log
            Image.objects.create(
                image_url=data['img'],
                image_type="incident",
                added_on=timezone.now(),
                incident=incident
            )

        return Response({"status": "success"}, status=status.HTTP_200_OK)



class SuspectCreateView(CreateAPIView):
    serializer_class = SuspectCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Create human without name
            suspect = Human.objects.create(
                human_type=Human.SUSPECTED,
                profile_pic=serializer.validated_data['image_url']
            )
            
            # Generate name after ID is assigned
            suspect.name = f"Suspect #{suspect.id}"
            suspect.save()
            
            # Create profile image record
            Image.objects.create(
                human=suspect,
                image_url=serializer.validated_data['image_url'],
                image_type=Image.PROFILE_IMAGE
            )
        
        # Prepare response
        response_serializer = SuspectResponseSerializer(suspect)
        headers = self.get_success_headers(response_serializer.data)
        return Response(
            {
                'status': 'success',
                'message': 'Suspect created successfully',
                'data': response_serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )


