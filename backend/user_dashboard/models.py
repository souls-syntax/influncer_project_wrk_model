from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class SavedCampaign(models.Model):
    """
    User ke dwara save ki gayi influencers ki list.
    """
    # Har campaign ek user se juda hoga
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Campaign/List ka naam
    name = models.CharField(max_length=100)
    # Influencer IDs ko comma-separated string ke roop mein save karenge
    # Example: "UC-lHJZR3Gqxm24_Vd_AJ5Yw,UC3N9w_7T92tC2q822aP_6g"
    influencer_ids = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"