from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_api import fetch_comments_in_batches
from db import save_comments, get_comments
from analysis import process_comments, get_keywords, engagement_rate
from visualize import plot_keywords, plot_sentiment

# FastAPI app for frontend dashboard
app = FastAPI()

# Allow React frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RequestData(BaseModel):
    video_id: str
    max_comments: int

@app.post("/analyze")
def analyze_video(data: RequestData):
    """
    API endpoint: analyze YouTube comments for a given video.
    Returns JSON with keywords, sentiment, and engagement.
    """
    video_id = data.video_id
    max_comments = data.max_comments

    total_comments = 0
    for batch in fetch_comments_in_batches(video_id, batch_size=1000, max_comments=max_comments):
        save_comments(video_id, batch)
        total_comments += len(batch)

    all_comments = get_comments(video_id)
    df_all = process_comments(all_comments)

    keywords_all = get_keywords(df_all)
    sentiment_avg = df_all['sentiment'].mean()
    engagement = engagement_rate(df_all)

    return {
        "video_id": video_id,
        "total_comments": total_comments,
        "keywords": keywords_all,
        "avg_sentiment": sentiment_avg,
        "engagement_rate": engagement
    }

# Standalone mode for local debugging with charts
def run(video_id):
    total_comments = 0

    # Process each batch incrementally
    for batch in fetch_comments_in_batches(video_id, batch_size=1000, max_comments=10000):
        save_comments(video_id, batch)
        total_comments += len(batch)
        print(f"Stored {total_comments} comments so far...")

        # Quick batch analysis
        df_batch = process_comments(batch)
        keywords_batch = get_keywords(df_batch)
        print("Batch keywords (top 5):", keywords_batch[:5])
        print("Batch engagement rate:", engagement_rate(df_batch))

    # Final full analysis after all batches
    print(f"\n✅ Finished fetching {total_comments} comments")

    all_comments = get_comments(video_id)
    df_all = process_comments(all_comments)

    # Final keyword chart
    keywords_all = get_keywords(df_all)
    plot_keywords(keywords_all)

    # Final sentiment chart
    plot_sentiment(df_all, video_id)

    # Final engagement metric
    print("Final engagement rate:", engagement_rate(df_all))

if __name__ == "__main__":
    # Run standalone mode (charts + console output)
    run("Ah_uuTwGOYU")  # Replace with a real YouTube video ID