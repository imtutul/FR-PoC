from django.urls import path
from .views import ZoneCreateView

urlpatterns = [
    path('create/', ZoneCreateView.as_view(), name='zone-create')
]