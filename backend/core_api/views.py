from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from db_service import get_influencers_by_criteria, get_influencer_by_id

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def influencer_list(request):
    """API endpoint jo MongoDB se asli data laakar deta hai."""
    search_term = request.GET.get('search_term', '')
    location = request.GET.get('location', '') # Location parameter ko get karein
    try:
        min_subs = int(request.GET.get('min_subs', 0))
    except (ValueError, TypeError):
        min_subs = 0
    
    influencers = get_influencers_by_criteria(
        search_term=search_term,
        min_subs=min_subs,
        location=location # Function ko location pass karein
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