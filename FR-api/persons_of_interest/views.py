from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics, status
from .models import PersonOfInterest, PersonOfInterestImage
from .serializers import PersonOfInterestSerializer
from rest_framework.generics import RetrieveAPIView


class PersonOfInterestCreateView(generics.CreateAPIView):
    queryset = PersonOfInterest.objects.all()
    serializer_class = PersonOfInterestSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 201,
            "message": "Person of Interest created successfully",
            "data": response.data
        }, status=201)

class PersonOfInterestListView(generics.ListAPIView):
    queryset = PersonOfInterest.objects.all()
    serializer_class = PersonOfInterestSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 200,
            "message": "List of persons of interest",
            "data": response.data
        })
    

class POIAddImagesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            poi = PersonOfInterest.objects.get(pk=pk)
        except PersonOfInterest.DoesNotExist:
            return Response({
                "status": "error",
                "code": 404,
                "message": "Person of Interest not found"
            }, status=404)

        images = request.FILES.getlist('images')
        if not images:
            return Response({
                "status": "error",
                "code": 400,
                "message": "No images submitted"
            }, status=400)

        for image in images:
            PersonOfInterestImage.objects.create(person=poi, image=image)

        return Response({
            "status": "success",
            "code": 201,
            "message": "Images uploaded successfully",
            "data": {
                "poi_id": poi.id,
                "files_uploaded": len(images)
            }
        }, status=201)


class PersonOfInterestDetailView(RetrieveAPIView):
    queryset = PersonOfInterest.objects.all()
    serializer_class = PersonOfInterestSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 200,
            "message": "Person of Interest details fetched",
            "data": response.data
        })