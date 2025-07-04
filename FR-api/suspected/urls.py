from django.urls import path
from .views import (
    SuspectCreateView, SuspectListView,
    SuspectAddImagesView, SuspectDetailView
)

urlpatterns = [
    path('create/', SuspectCreateView.as_view(), name='suspect-create'),
    path('list/', SuspectListView.as_view(), name='suspect-list'),
    path('<int:pk>/', SuspectDetailView.as_view(), name='suspect-detail'),
    path('<int:pk>/add-images/', SuspectAddImagesView.as_view(), name='suspect-add-images'),
]
