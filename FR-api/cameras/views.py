from rest_framework import generics, status
from rest_framework.response import Response
from .models import Camera
from .serializers import CameraSerializer

class CameraCreateView(generics.CreateAPIView):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 201,
            "message": "Camera created and mapped to zone successfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)