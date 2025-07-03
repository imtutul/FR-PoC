from django.urls import path
from .views import SuspectedMatchCreateView, SuspectedMatchListView

urlpatterns = [
    path('create/', SuspectedMatchCreateView.as_view(), name='suspected-create'),
    path('list/', SuspectedMatchListView.as_view(), name='suspected-list'),
]
