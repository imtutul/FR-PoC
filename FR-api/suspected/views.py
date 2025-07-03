from rest_framework import generics
from .models import SuspectedMatch
from .serializers import SuspectedMatchSerializer

class SuspectedMatchCreateView(generics.CreateAPIView):
    queryset = SuspectedMatch.objects.all()
    serializer_class = SuspectedMatchSerializer

class SuspectedMatchListView(generics.ListAPIView):
    queryset = SuspectedMatch.objects.all()
    serializer_class = SuspectedMatchSerializer
