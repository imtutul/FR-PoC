from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from .models import Suspect, SuspectImage
from .serializers import SuspectSerializer


class SuspectCreateView(generics.CreateAPIView):
    queryset = Suspect.objects.all()
    serializer_class = SuspectSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 201,
            "message": "Suspect created successfully",
            "data": response.data
        })


class SuspectListView(generics.ListAPIView):
    queryset = Suspect.objects.all()
    serializer_class = SuspectSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 200,
            "message": "List of suspects",
            "data": response.data
        })


class SuspectAddImagesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            suspect = Suspect.objects.get(pk=pk)
        except Suspect.DoesNotExist:
            return Response({
                "status": "error",
                "code": 404,
                "message": "Suspect not found"
            }, status=404)

        images = request.FILES.getlist('images')
        if not images:
            return Response({
                "status": "error",
                "code": 400,
                "message": "No images submitted"
            }, status=400)

        for image in images:
            SuspectImage.objects.create(suspect=suspect, image=image)

        return Response({
            "status": "success",
            "code": 201,
            "message": "Images uploaded successfully",
            "data": {
                "suspect_id": suspect.id,
                "files_uploaded": len(images)
            }
        })


class SuspectDetailView(generics.RetrieveAPIView):
    queryset = Suspect.objects.all()
    serializer_class = SuspectSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 200,
            "message": "Suspect details fetched",
            "data": response.data
        })
