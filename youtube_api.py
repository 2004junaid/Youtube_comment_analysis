from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_comments(video_id, max_comments=10000):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    
    while request and len(comments) < max_comments:
        response = request.execute()
        for item in response['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            comments.append({
                "user": snippet['authorDisplayName'],
                "text": snippet['textDisplay'],
                "likes": snippet['likeCount'],
                "time": snippet['publishedAt']
            })
        
        # Stop if we hit the limit
        if len(comments) >= max_comments:
            break
        
        # Get next page
        request = youtube.commentThreads().list_next(request, response)
    
    return comments