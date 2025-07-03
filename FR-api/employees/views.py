from rest_framework import generics, permissions
from .models import Employee, EmployeeImage
from .serializers import EmployeeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import RetrieveAPIView
from rest_framework import status

class EmployeeCreateView(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 201,
            "message": "Employee created successfully",
            "data": response.data
        }, status=201)


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 200,
            "message": "List of employee",
            "data": response.data
        })


class EmployeeAddImagesView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({
                "status": "error",
                "code": 404,
                "message": "Employee not found"
            }, status=404)

        images = request.FILES.getlist('images')
        if not images:
            return Response({
                "status": "error",
                "code": 400,
                "message": "No images submitted"
            }, status=400)

        for image in images:
            EmployeeImage.objects.create(employee=employee, image=image)

        return Response({
            "status": "success",
            "code": 201,
            "message": "Images uploaded successfully",
            "data": {
                "poi_id": employee.id,
                "files_uploaded": len(images)
            }
        }, status=201)
    

class EmployeeDetailView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({
            "status": "success",
            "code": 200,
            "message": "Employee details fetched",
            "data": response.data
        })