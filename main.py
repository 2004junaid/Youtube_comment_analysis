from youtube_api import fetch_comments_in_batches
from db import save_comments, get_comments
from analysis import process_comments, get_keywords, engagement_rate
from visualize import plot_keywords, plot_sentiment

def run(video_id):
    total_comments = 0
    for batch in fetch_comments_in_batches(video_id, batch_size=1000, max_comments=10000):
        # Step 1: Store batch
        save_comments(video_id, batch)
        total_comments += len(batch)
        print(f"Stored {total_comments} comments so far...")

        # Step 2: Analyze batch immediately
        df = process_comments(batch)
        keywords = get_keywords(df)
        print("Batch keywords:", keywords[:5])  # show top 5 for quick feedback
        print("Batch engagement rate:", engagement_rate(df))

    # Final full analysis after all batches
    print(f"\n Finished fetching {total_comments} comments")
    # You can reload all from DB for complete visualization
    from db import get_comments
    all_comments = get_comments(video_id)
    df_all = process_comments(all_comments)
    plot_keywords(get_keywords(df_all))
    plot_sentiment(df_all, video_id)


if __name__ == "__main__":
    # Replace with a real YouTube video ID
    run("jNQXAC9IVRw")