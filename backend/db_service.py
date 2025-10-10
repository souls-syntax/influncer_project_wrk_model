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

def get_influencers_by_criteria(category="", min_subs=0, max_subs=0):
    collection = get_mongo_collection()
    if collection is None:
        return []

    try:
        query_parts = []
        
        # --- YAHAN BADLAV KIYA GAYA HAI ---
        # Subscribers ke liye min aur max, dono ko handle karne ka code
        sub_query = {}
        if min_subs > 0:
            sub_query['$gte'] = min_subs  # gte = Greater than or equal to
        if max_subs > 0:
            sub_query['$lte'] = max_subs  # lte = Less than or equal to
        if sub_query:
            query_parts.append({'subscribers': sub_query})
        
        # Category ke liye search query
        if category:
            # Humne '$or' hata diya hai taaki sirf category field mein search ho
            query_parts.append({'category': {"$regex": category, "$options": "i"}})

        # Final query banayein
        query = {}
        if query_parts:
            query['$and'] = query_parts

        results = list(collection.find(query))
        
        processed_results = []
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
            processed_results.append(doc)
            
        return processed_results

    except Exception as e:
        print(f"❌ Error fetching influencers: {e}")
        return []

def get_influencer_by_id(influencer_id):
    collection = get_mongo_collection()
    if collection is None:
        return None
    try:
        doc = collection.find_one({'id': influencer_id})
        if doc and '_id' in doc:
            doc['_id'] = str(doc['_id'])
        return doc
    except Exception as e:
        print(f"❌ Error fetching single influencer: {e}")
        return None