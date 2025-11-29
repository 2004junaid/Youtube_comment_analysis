import pandas as pd
from textblob import TextBlob
import re
from collections import Counter

def analyze_sentiment(text: str) -> float:
    blob = TextBlob(text)
    return blob.sentiment.polarity

def process_comments(comments):
    # Handle empty list of comments
    if not comments:
        return pd.DataFrame(columns=["text", "likes", "sentiment"])

    df = pd.DataFrame(comments)

    # Ensure the expected 'text' field exists
    if "text" not in df.columns:
        raise ValueError("Expected 'text' field in comments, but none found")

    # Add sentiment analysis
    df['sentiment'] = df['text'].apply(analyze_sentiment)

    # Ensure 'likes' column exists for engagement_rate
    if "likes" not in df.columns:
        df['likes'] = 0

    return df

def get_keywords(df, top_n=20):
    if "text" not in df.columns or df.empty:
        return []
    words = []
    for text in df['text']:
        words.extend(re.findall(r'\w+', text.lower()))
    return Counter(words).most_common(top_n)

def engagement_rate(df):
    if df.empty:
        return 0
    return df['likes'].sum() / len(df)