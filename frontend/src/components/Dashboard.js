import React, { useState } from "react";
import axios from "axios";
import Chart from "./Chart";

function Dashboard() {
  const [videoId, setVideoId] = useState("");
  const [maxComments, setMaxComments] = useState(1000);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const res = await axios.post("http://127.0.0.1:8000/analyze", {
      video_id: videoId,
      max_comments: parseInt(maxComments)
    });
    setResult(res.data);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="YouTube Video ID"
        value={videoId}
        onChange={(e) => setVideoId(e.target.value)}
      />
      <input
        type="number"
        placeholder="Number of comments"
        value={maxComments}
        onChange={(e) => setMaxComments(e.target.value)}
      />
      <button onClick={handleSubmit}>Analyze</button>

      {result && (
        <div>
          <h2>Results for Video: {result.video_id}</h2>
          <p>Total Comments: {result.total_comments}</p>
          <p>Average Sentiment: {result.avg_sentiment.toFixed(2)}</p>
          <p>Engagement Rate: {result.engagement_rate.toFixed(2)}</p>
          <Chart keywords={result.keywords} />
        </div>
      )}
    </div>
  );
}

export default Dashboard;