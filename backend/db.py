from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client['youtube_analysis']
collection = db['comments']

def save_comments(video_id, comments):
    for c in comments:
        c['video_id'] = video_id
    if comments:
        collection.insert_many(comments)

def get_comments(video_id):
    return list(collection.find({"video_id": video_id}))