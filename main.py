from youtube_api import fetch_comments_in_batches
from db import save_comments, get_comments
from analysis import process_comments, get_keywords, engagement_rate
from visualize import plot_keywords, plot_sentiment

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
    # Replace with a real YouTube video ID
    run("jNQXAC9IVRw")