from django.urls import path
from .views import PersonOfInterestCreateView, PersonOfInterestListView, POIAddImagesView, PersonOfInterestDetailView

urlpatterns = [
    path('create/', PersonOfInterestCreateView.as_view(), name='poi-create'),
    path('list/', PersonOfInterestListView.as_view(), name='poi-list'),
    path('<int:pk>/add-images/', POIAddImagesView.as_view(), name='poi-add-images'),
    path('<int:pk>/', PersonOfInterestDetailView.as_view(), name='poi-detail'),
]
