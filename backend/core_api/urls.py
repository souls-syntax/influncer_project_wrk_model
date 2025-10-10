from django.urls import path
from .views import influencer_list, influencer_detail

urlpatterns = [
    path('influencers/', influencer_list, name='influencer-list'),
    path('influencers/<str:influencer_id>/', influencer_detail, name='influencer-detail'),
]