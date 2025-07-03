from django.urls import path
from .views import IncidentListView, IncidentDetailView, AILogView

urlpatterns = [
    path("incidents/", IncidentListView.as_view(), name="incident-list"),
    path("incidents/<int:pk>/", IncidentDetailView.as_view(), name="incident-detail"),
    path("ai-log/", AILogView.as_view(), name="ai-log"),  # AI callback
]
