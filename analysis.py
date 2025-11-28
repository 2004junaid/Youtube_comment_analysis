import pandas as pd
from textblob import TextBlob
import re
from collections import Counter

def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def process_comments(comments):
    df = pd.DataFrame(comments)
    df['sentiment'] = df['text'].apply(analyze_sentiment)
    return df

def get_keywords(df, top_n=20):
    words = []
    for text in df['text']:
        words.extend(re.findall(r'\w+', text.lower()))
    return Counter(words).most_common(top_n)

def engagement_rate(df):
    return df['likes'].sum() / len(df) if len(df) > 0 else 0