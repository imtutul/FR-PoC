from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from .models import Human, Image, Incident, IncidentDetail
from .serializers import AIWebhookSerializer, SuspectCreateSerializer, SuspectResponseSerializer, HumanSerializer, ImageCreateSerializer
from rest_framework import viewsets, permissions, generics
from .serializers import HumanCreateWithImagePathsSerializer
from django.utils.timezone import now
    

class AIWebhookView(APIView):
    serializer_class = AIWebhookSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        all_human_ids = data["associate_id"] + data["suspect_id"] + data["poi_id"]
        humans = Human.objects.filter(id__in=all_human_ids)

        with transaction.atomic():
            incident, created = Incident.objects.get_or_create(
                id=data["incident_id"],
                defaults={
                    "start_on": data["timestamp"],
                    "status": 1,
                },
            )

            # Always attach humans
            incident.humans.add(*humans)

            # Close handling
            if data["status"] == 0:
                incident.status = 0
                incident.end_on = data["timestamp"]
                incident.video_clip = data.get("video_clip", "")
                incident.best_image = data["img"]
                incident.save()

            # Create incident detail
            detail = IncidentDetail.objects.create(
                incident=incident,
                timestamp=data["timestamp"],
                status=data["status"],
                image=data["img"],
            )
            detail.humans.add(*humans)

            # Create image log
            image = Image.objects.create(
                image_url=data["img"],
                image_type=Image.INCIDENT_IMAGE,
                incident=incident,
            )

        return Response({
            "status": "success",
            "code": 200,
            "message": "Incident processed successfully.",
            "data": {
                "incident_id": str(incident.id),
                "incident_created": created,
                "status": incident.get_status_display().lower(),
                "humans_attached": humans.count(),
                "detail_logged": True,
                "image_logged": True
            }
        }, status=status.HTTP_200_OK)



class SuspectCreateView(generics.CreateAPIView):
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


class _BaseReadOnlyHumanViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HumanSerializer
    permission_classes = [permissions.AllowAny]
    target_type: int = None

    def get_queryset(self):
        return Human.objects.filter(human_type=self.target_type).order_by("id")

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "status": "success",
                "code": 200,
                "data": serializer.data,
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "success",
            "code": 200,
            "data": serializer.data,
            "timestamp": now().isoformat()
        }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "status": "success",
            "code": 200,
            "data": serializer.data,
            "timestamp": now().isoformat()
        }, status=status.HTTP_200_OK)


class EmployeeViewSet(_BaseReadOnlyHumanViewSet):
    target_type = Human.EMPLOYEE


class SuspectViewSet(_BaseReadOnlyHumanViewSet):
    target_type = Human.SUSPECTED


class PoIViewSet(_BaseReadOnlyHumanViewSet):
    target_type = Human.PERSON_OF_INTEREST



class EmployeeCreateView(generics.CreateAPIView):
    serializer_class = HumanCreateWithImagePathsSerializer

    def get_serializer_context(self):
        return {'human_type': Human.EMPLOYEE}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": "success",
            "code": status.HTTP_201_CREATED,
            "message": "Employee created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)


class PoICreateView(generics.CreateAPIView):
    serializer_class = HumanCreateWithImagePathsSerializer

    def get_serializer_context(self):
        return {'human_type': Human.PERSON_OF_INTEREST}

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "status": "success",
            "code": status.HTTP_201_CREATED,
            "message": "Person of Interest created successfully.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    


class ImageCreateView(generics.CreateAPIView):
    serializer_class = ImageCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "status": "success",
            "code": 201,
            "message": "Image successfully added.",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    