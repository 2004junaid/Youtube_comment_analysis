from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_comments_in_batches(video_id, batch_size=500, max_comments=10000):
    """
    Fetch comments in batches for faster incremental analysis.
    """
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )

    while request and len(comments) < max_comments:
        response = request.execute()
        batch = []
        for item in response['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            batch.append({
                "user": snippet['authorDisplayName'],
                "text": snippet['textDisplay'],
                "likes": snippet['likeCount'],
                "time": snippet['publishedAt']
            })

        comments.extend(batch)

        # Yield batch for immediate analysis
        if len(comments) % batch_size == 0 or len(comments) >= max_comments:
            yield batch

        request = youtube.commentThreads().list_next(request, response)