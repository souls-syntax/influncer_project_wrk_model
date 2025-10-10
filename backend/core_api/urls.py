from django.urls import path,re_path
from .views import influencer_list, influencer_detail

urlpatterns = [
    path('influencers/', influencer_list, name='influencer-list'),
    re_path(r'^influencers/(?P<influencer_id>[^/]+)/?$', influencer_detail, name='influencer-detail')
]