from youtube_api import fetch_comments
from db import save_comments, get_comments
from analysis import process_comments, get_keywords, engagement_rate
from visualize import plot_keywords, plot_sentiment

def run(video_id):
    # Step 1: Fetch
    print(f"Youtube Comment Analysis")
    comments = fetch_comments(video_id)
    print(f"Fetched {len(comments)} comments")

    # Step 2: Store
    save_comments(video_id, comments)

    # Step 3: Load + Analyze
    stored_comments = get_comments(video_id)
    df = process_comments(stored_comments)

    # Step 4: Keywords
    keywords = get_keywords(df)
    print("Top keywords:", keywords)

    # Step 5: Engagement
    print("Engagement rate:", engagement_rate(df))

    # Step 6: Visualize
    plot_keywords(keywords)
    plot_sentiment(df, video_id)

if __name__ == "__main__":
    # Replace with a real YouTube video ID
    run("jNQXAC9IVRw")