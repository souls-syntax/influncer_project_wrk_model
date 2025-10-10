# influncer_project/backend/db_service.py

from pymongo import MongoClient
import sys

MONGO_URI = "mongodb+srv://vishal:iS0ixgTdJ7BZg3Cc@vv.up8f99f.mongodb.net/?retryWrites=true&w=majority&appName=vv"
DB_NAME = "vishal"
COLLECTION_NAME = "influencers"

def get_mongo_collection():
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client[DB_NAME]
        print("✅ MongoDB Connection Successful!")
        return db[COLLECTION_NAME]
    except Exception as e:
        print(f"❌ FATAL ERROR: Could not connect to MongoDB. {e}")
        return None

def get_influencers_by_criteria(search_term="", min_subs=0, location=""):
    collection = get_mongo_collection()
    if collection is None:
        return []

    try:
        query_parts = []
        
        # --- YAHAN BADLAV KIYA GAYA HAI ---
        # Har filter ke liye alag-alag conditions banayein
        if min_subs > 0:
            query_parts.append({'subscribers': {'$gte': min_subs}})
        
        if location:
            query_parts.append({'location': {"$regex": location, "$options": "i"}})

        if search_term:
            regex = {"$regex": search_term, "$options": "i"}
            # Search term ko naam, category, ya niche mein dhoondhein
            query_parts.append({
                '$or': [
                    {'category': regex}, 
                    {'name': regex},
                    {'ai_niche': regex}
                ]
            })

        # Saari conditions ko milakar final query banayein
        query = {}
        if query_parts:
            query['$and'] = query_parts

        results = list(collection.find(query, {'_id': 0}))
        return results

    except Exception as e:
        print(f"❌ Error fetching influencers: {e}")
        return []

def get_influencer_by_id(influencer_id):
    collection = get_mongo_collection()
    if collection is None:
        return None
    try:
        doc = collection.find_one({'id': influencer_id}, {'_id': 0})
        return doc
    except Exception as e:
        print(f"❌ Error fetching single influencer: {e}")
        return None