from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import SavedCampaign
from .serializers import SavedCampaignSerializer
from django.http import HttpResponse

def dashboard_home(request):
    return HttpResponse("Welcome to the Dashboard!")

class CampaignListCreateView(generics.ListCreateAPIView):
    """
    User ke saare campaigns ko list karta hai aur naye campaign banata hai.
    GET, POST /dashboard/campaigns/
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SavedCampaignSerializer

    def get_queryset(self):
        # Sirf uss user ke campaigns dikhao jo logged-in hai
        return SavedCampaign.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Naya campaign banate samay, user ko automatically set kar do
        serializer.save(user=self.request.user)