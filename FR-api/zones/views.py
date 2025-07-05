from rest_framework import generics, status
from rest_framework.response import Response
from .models import Zone
from .serializers import ZoneSerializer

class ZoneCreateView(generics.CreateAPIView):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 201,
            "message": "Zone created successfully",
            "data": response.data
        }, status=status.HTTP_201_CREATED)