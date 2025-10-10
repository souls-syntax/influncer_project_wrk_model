from django.urls import path
from .views import CampaignListCreateView, dashboard_home  # import the new view

urlpatterns = [
    path('', dashboard_home, name='dashboard-home'),  # handles /dashboard/
    path('campaigns/', CampaignListCreateView.as_view(), name='campaign-list-create'),
]
