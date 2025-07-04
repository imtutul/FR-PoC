from django.urls import path
from .views import AIWebhookView, SuspectCreateView

urlpatterns = [
    path('ai-webhook/', AIWebhookView.as_view(), name='ai_webhook'),
    path('suspects/', SuspectCreateView.as_view(), name='create_suspect'),
]