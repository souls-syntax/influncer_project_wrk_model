import sys
import re
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import YOUTUBE_API_KEY
from db_service import get_mongo_collection
from ai_service import classify_influencer

TARGET_CATEGORIES = {
    "Gaming": "game walkthrough OR twitch highlights OR esports review",
    "Fitness": "workout routine OR healthy eating OR fitness tips",
    "Food Vlogging": "easy recipes OR cooking challenge OR street food review",
}
COUNT_PER_CATEGORY = 3

def get_youtube_client():
    try:
        return build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    except Exception as e:
        print(f"❌ Failed to initialize YouTube Client: {e}")
        sys.exit(1)

def clean_text(text: str) -> str:
    if not text: return ""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'<.*?>', '', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = ' '.join(text.split()).strip().lower()
    return text

def fetch_channel_details(youtube_client, channel_id):
    try:
        channel_request = youtube_client.channels().list(
            part="snippet,statistics,contentDetails", id=channel_id
        ).execute()
        if not channel_request.get('items'): return None, []
        item = channel_request['items'][0]
        channel_info = {
            'id': item['id'], 'name': item['snippet']['title'],
            'description': item['snippet'].get('description', ''),
            'subscribers': int(item['statistics'].get('subscriberCount', 0)),
            'total_views': int(item['statistics'].get('viewCount', 0)),
            'photo_url': item['snippet']['thumbnails']['default']['url'],
            'channel_url': f"https://www.youtube.com/channel/{item['id']}",
            'uploads_playlist_id': item['contentDetails']['relatedPlaylists']['uploads']
        }
        playlist_items_request = youtube_client.playlistItems().list(
            part="contentDetails", playlistId=channel_info['uploads_playlist_id'], maxResults=5
        ).execute()
        video_ids = [item['contentDetails']['videoId'] for item in playlist_items_request.get('items', [])]
        videos_data = []
        if video_ids:
            videos_request = youtube_client.videos().list(
                part="snippet,statistics", id=",".join(video_ids)
            ).execute()
            for video_item in videos_request.get('items', []):
                stats = video_item.get('statistics', {})
                videos_data.append({
                    'title': video_item['snippet'].get('title', ''),
                    'description': video_item['snippet'].get('description', ''),
                    'view_count': int(stats.get('viewCount', 0)),
                    'like_count': int(stats.get('likeCount', 0)),
                    'comment_count': int(stats.get('commentCount', 0))
                })
        return channel_info, videos_data
    except HttpError:
        return None, []

def prepare_data_for_db(channel_info, videos_data, category):
    total_likes = sum(video.get('like_count', 0) for video in videos_data)
    total_comments = sum(video.get('comment_count', 0) for video in videos_data)
    total_views = sum(video.get('view_count', 0) for video in videos_data)
    engagement_rate = (total_likes + total_comments) / total_views if total_views > 0 else 0
    cleaned_bio = clean_text(channel_info['description'])
    video_titles = " | ".join([clean_text(v['title']) for v in videos_data])
    ai_prompt = f"CHANNEL BIO: {cleaned_bio}\nRECENT VIDEO TOPICS: {video_titles}"
    db_document = {
        'id': channel_info['id'], 'name': channel_info['name'],
        'description': channel_info['description'], 'subscribers': channel_info['subscribers'],
        'total_views': channel_info['total_views'], 'photo_url': channel_info['photo_url'],
        'channel_url': channel_info['channel_url'], 'category': category,
        'engagement_rate': round(engagement_rate, 4),
        'ai_prompt_text': ai_prompt,
    }
    return db_document

def run_data_collection():
    youtube = get_youtube_client()
    mongo_collection = get_mongo_collection()
    
    if mongo_collection is None: 
        print("❌ Cannot proceed without MongoDB connection.")
        return

    for category, query in TARGET_CATEGORIES.items():
        print(f"\n🚀 Starting search for category: '{category}'...")
        search_request = youtube.search().list(
            q=query, type='channel', part='id', maxResults=COUNT_PER_CATEGORY
        ).execute()
        for item in search_request.get('items', []):
            channel_id = item['id']['channelId']
            channel_info, videos_data = fetch_channel_details(youtube, channel_id)
            if channel_info:
                print(f"  - Found channel: {channel_info['name']}")
                db_document = prepare_data_for_db(channel_info, videos_data, category)
                
                print(f"    🧠 Analyzing with AI...")
                ai_results = classify_influencer(db_document['ai_prompt_text'])
                
                # AI se mile naye data ko add karein
                db_document['ai_niche'] = ai_results.get('primary_niche', 'AI_Failed')
                db_document['ai_safety_score'] = ai_results.get('brand_safety_score_1_to_10', 0)
                db_document['ai_risk_summary'] = ai_results.get('risk_summary', '')
                db_document['ai_keywords'] = ai_results.get('keywords', [])
                db_document['ai_recommendation'] = ai_results.get('recommendation', 'Not Recommended')
                
                mongo_collection.update_one({'id': db_document['id']}, {'$set': db_document}, upsert=True)
                print(f"    ✅ Saved to database with AI analysis.")
            time.sleep(1)
    print("\n\n✨ Data collection complete! ✨")

if __name__ == '__main__':
    run_data_collection()