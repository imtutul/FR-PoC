from django.urls import path
from .views import CameraCreateView

urlpatterns = [
    path('create/', CameraCreateView.as_view(), name='create_camera'),
]