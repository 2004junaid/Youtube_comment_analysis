// ...existing code...
import React, { useState } from "react";
import axios from "axios";
import Chart from "./Chart";
import "./Dashboard.css";
// ...existing code...

function Dashboard() {
  const [videoId, setVideoId] = useState("");
  const [maxComments, setMaxComments] = useState(500);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const validate = () => {
    if (!videoId.trim()) {
      setError("Please enter a YouTube video ID.");
      return false;
    }
    if (isNaN(maxComments) || maxComments <= 0) {
      setError("Number of comments must be a positive number.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSubmit = async () => {
    if (!validate()) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze", {
        video_id: videoId.trim(),
        max_comments: parseInt(maxComments, 10)
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze. Check backend or network.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">
      <div className="panel">
        <h2 className="panel-title">YouTube Comments Analysis</h2>

        <label className="field">
          <span className="label">Video ID</span>
          <input
            className="input"
            type="text"
            placeholder="e.g. dQw4w9WgXcQ"
            value={videoId}
            onChange={(e) => setVideoId(e.target.value)}
            disabled={loading}
          />
        </label>

        <label className="field">
          <div className="label-with-value">
            <span className="label">Max comments</span>
            <span className="small">{maxComments}</span>
          </div>
          <input
            className="slider"
            type="range"
            min="10"
            max="2000"
            step="10"
            value={maxComments}
            onChange={(e) => setMaxComments(Number(e.target.value))}
            disabled={loading}
          />
        </label>

        <div className="actions">
          <button
            className={`btn ${loading ? "btn-loading" : ""}`}
            onClick={handleSubmit}
            disabled={loading}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {error && <div className="error">{error}</div>}
      </div>

      {result && (
        <div className="results">
          <div className="result-card">
            <div className="result-header">
              <h3>Results — {result.video_id}</h3>
              <div className="meta">Total comments: {result.total_comments}</div>
            </div>

            <div className="stats">
              <div className="stat">
                <div className="stat-title">Average sentiment</div>
                <div className="stat-value">{result.avg_sentiment.toFixed(2)}</div>
                <div className="stat-bar">
                  <div
                    className="stat-fill sentiment"
                    style={{ width: `${Math.min(100, Math.abs(result.avg_sentiment) * 20)}%` }}
                  />
                </div>
              </div>

              <div className="stat">
                <div className="stat-title">Engagement rate</div>
                <div className="stat-value">{(result.engagement_rate * 100).toFixed(2)}%</div>
                <div className="stat-bar">
                  <div
                    className="stat-fill engagement"
                    style={{ width: `${Math.min(100, result.engagement_rate * 100)}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="chart-wrap">
              <Chart keywords={result.keywords} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
// ...existing code...