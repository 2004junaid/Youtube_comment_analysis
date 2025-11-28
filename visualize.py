import matplotlib.pyplot as plt

def plot_keywords(keywords):
    words, counts = zip(*keywords)
    plt.figure(figsize=(10,5))
    plt.bar(words, counts)
    plt.xticks(rotation=45)
    plt.title("Most Common Words")
    plt.show()

def plot_sentiment(df, video_id):
    avg_sentiment = df['sentiment'].mean()
    plt.bar([video_id], [avg_sentiment])
    plt.title("Average Sentiment per Video")
    plt.show()