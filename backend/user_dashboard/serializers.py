from rest_framework import serializers
from .models import SavedCampaign

class SavedCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedCampaign
        fields = ['id', 'name', 'influencer_ids', 'date_created']