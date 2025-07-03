from django.urls import path
from .views import EmployeeCreateView, EmployeeListView, EmployeeAddImagesView, EmployeeDetailView

urlpatterns = [
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('list/', EmployeeListView.as_view(), name='employee-list'),
    path('<int:pk>/add-images/', EmployeeAddImagesView.as_view(), name='employee-add-images'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
]
