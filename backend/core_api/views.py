# influncer_project/backend/core_api/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from db_service import get_influencers_by_criteria, get_influencer_by_id

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def influencer_list(request):
    """API endpoint jo MongoDB se asli data laakar deta hai."""
    
    # --- YAHAN BADLAV KIYA GAYA HAI ---
    # Frontend se aa rahe sahi parameter naamo ko yahan get karein
    category = request.GET.get('category', '')
    try:
        min_subs = int(request.GET.get('min_subscribers', 0))
    except (ValueError, TypeError):
        min_subs = 0
    try:
        max_subs = int(request.GET.get('max_subscribers', 0))
    except (ValueError, TypeError):
        max_subs = 0
    
    # Sahi parameters ko database function mein pass karein
    influencers = get_influencers_by_criteria(
        category=category,
        min_subs=min_subs,
        max_subs=max_subs
    )
    return Response(influencers)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def influencer_detail(request, influencer_id):
    """Ek single influencer ki poori details deta hai."""
    influencer = get_influencer_by_id(influencer_id)
    if influencer:
        return Response(influencer)
    else:
        return Response({"error": "Influencer not found"}, status=404)