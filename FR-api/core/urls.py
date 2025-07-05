from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (
    AIWebhookView,
    SuspectCreateView,
    EmployeeViewSet,
    SuspectViewSet,
    PoIViewSet,
    EmployeeCreateView,
    PoICreateView,
    ImageCreateView
)

router = SimpleRouter()
router.register(r'employee', EmployeeViewSet, basename='employee')
router.register(r'suspect', SuspectViewSet, basename='suspect')
router.register(r'poi', PoIViewSet, basename='poi')

urlpatterns = [
    path('ai-webhook/', AIWebhookView.as_view(), name='ai_webhook'),
    path('new-suspect/', SuspectCreateView.as_view(), name='create_suspect'),
    path('new-employee/', EmployeeCreateView.as_view(), name='create_employee'),
    path('new-poi/', PoICreateView.as_view(), name='create_poi'),
    path('new-image/', ImageCreateView.as_view(), name='create_image'),
    *router.urls,
]
