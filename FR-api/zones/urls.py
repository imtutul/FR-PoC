from django.urls import path
from .views import ZoneCreateView

urlpatterns = [
    path('zone/create/', ZoneCreateView.as_view(), name='create_zone'),
]