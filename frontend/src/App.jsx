import { useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from "recharts";
import "./App.css";

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  // Load historical water usage
  const loadHistory = async () => {
    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/ai/history"
      );

      console.log("HISTORY RESPONSE:", response.data);

      setHistory(response.data.history);

    } catch (err) {
      console.error("HISTORY ERROR:", err);
    }
  };

  // Analyze water usage
  const analyzeWaterUsage = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await axios.get(
        "http://127.0.0.1:8000/ai/analyze"
      );

      console.log("API RESPONSE:", response.data);

      setAnalysis(response.data.analysis);

      // Load chart data
      await loadHistory();

    } catch (err) {
      console.error("API ERROR:", err);

      setError(
        "Unable to get analysis from AquaGuard AI backend."
      );

    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      {/* HEADER */}
      <header className="header">
        <div>
          <h1>💧 AquaGuard AI</h1>
          <p>
            AI-Powered Water Consumption Monitoring
          </p>
        </div>
      </header>


      <main className="container">

        {/* HERO */}
        <section className="hero">

          <h2>Water Anomaly Detection</h2>

          <p>
            Detect unusual water consumption and get
            AI-powered explanations and recommendations.
          </p>

          <button
            className="analyze-button"
            onClick={analyzeWaterUsage}
            disabled={loading}
          >
            {loading
              ? "Analyzing..."
              : "Analyze Water Usage"}
          </button>

        </section>


        {/* ERROR */}
        {error && (
          <div className="error">
            {error}
          </div>
        )}


        {/* RESULTS */}
        {analysis && (
          <div className="results">

            {/* WATER USAGE ANALYSIS */}
            <section className="panel">

              <h2>📊 Water Usage Analysis</h2>

              <div className="info-grid">

                <div className="info-item">
                  <span>Date & Time</span>
                  <strong>
                    {analysis.datetime}
                  </strong>
                </div>

                <div className="info-item">
                  <span>Actual Usage</span>
                  <strong>
                    {analysis.actual_usage} units
                  </strong>
                </div>

                <div className="info-item">
                  <span>Expected Usage</span>
                  <strong>
                    {Number(
                      analysis.predicted_usage
                    ).toFixed(2)} units
                  </strong>
                </div>

                <div className="info-item">
                  <span>Deviation</span>
                  <strong>
                    {Number(
                      analysis.deviation
                    ).toFixed(2)}%
                  </strong>
                </div>

                <div className="info-item">
                  <span>Consecutive Anomalies</span>
                  <strong>
                    {analysis.consecutive_anomalies}
                  </strong>
                </div>

              </div>

            </section>


            {/* ACTUAL VS EXPECTED CHART */}
            <section className="panel chart-panel">

              <h2>
                📈 Actual vs Expected Water Usage
              </h2>

              <p className="chart-description">
                Comparison of measured water consumption
                with the expected usage predicted by the
                AquaGuard AI model.
              </p>

              {history.length > 0 ? (

                <div className="chart-container">

                  <ResponsiveContainer
                    width="100%"
                    height={400}
                  >

                    <LineChart
                      data={history}
                      margin={{
                        top: 20,
                        right: 30,
                        left: 10,
                        bottom: 20
                      }}
                    >

                      <CartesianGrid
                        strokeDasharray="3 3"
                      />

                      <XAxis
                        dataKey="datetime"
                        tick={{ fontSize: 11 }}
                        angle={-35}
                        textAnchor="end"
                        height={80}
                      />

                      <YAxis
                        label={{
                          value: "Water Usage",
                          angle: -90,
                          position: "insideLeft"
                        }}
                      />

                      <Tooltip />

                      <Legend />

                      <Line
                        type="monotone"
                        dataKey="actual"
                        name="Actual Usage"
                        strokeWidth={2}
                        dot={false}
                      />

                      <Line
                        type="monotone"
                        dataKey="predicted"
                        name="Expected Usage"
                        strokeWidth={2}
                        dot={false}
                      />

                    </LineChart>

                  </ResponsiveContainer>

                </div>

              ) : (

                <p>
                  Loading water usage history...
                </p>

              )}

            </section>


            {/* RISK CARDS */}
            <section className="cards">

              <div className="card">
                <h3>Risk Level</h3>

                <p
                  className={`risk ${analysis.risk_level?.toLowerCase()}`}
                >
                  {analysis.risk_level}
                </p>
              </div>


              <div className="card">
                <h3>Risk Score</h3>

                <p>
                  {Number(
                    analysis.risk_score
                  ).toFixed(1)}
                </p>
              </div>


              <div className="card">
                <h3>Positive Deviation</h3>

                <p>
                  {Number(
                    analysis.deviation
                  ).toFixed(2)}%
                </p>
              </div>


              <div className="card">
                <h3>Consecutive Readings</h3>

                <p>
                  {analysis.consecutive_anomalies}
                </p>
              </div>

            </section>


            {/* GEMINI AI ANALYSIS */}
            {analysis.ai_response && (
              <>

                {/* EXPLANATION */}
                <section className="panel ai-panel">

                  <h2>
                    🤖 AI Anomaly Explanation
                  </h2>

                  <p>
                    {
                      analysis.ai_response
                        .anomaly_explanation
                    }
                  </p>

                </section>


                {/* POSSIBLE CAUSES */}
                <section className="panel">

                  <h2>
                    🔍 Possible Causes
                  </h2>

                  <ul className="recommendation-list">

                    {analysis.ai_response
                      .possible_causes
                      ?.map((cause, index) => (
                        <li key={index}>
                          {cause}
                        </li>
                      ))}

                  </ul>

                </section>


                {/* RECOMMENDED CHECKS */}
                <section className="panel">

                  <h2>
                    🛠️ Recommended Checks
                  </h2>

                  <ul className="recommendation-list">

                    {analysis.ai_response
                      .recommended_checks
                      ?.map((check, index) => (
                        <li key={index}>
                          {check}
                        </li>
                      ))}

                  </ul>

                </section>


                {/* IMMEDIATE ACTION */}
                <section className="panel action-panel">

                  <h2>
                    ⚡ Immediate Action
                  </h2>

                  <p>
                    {
                      analysis.ai_response
                        .immediate_action
                    }
                  </p>

                </section>


                {/* LONG TERM RECOMMENDATION */}
                <section className="panel">

                  <h2>
                    🌱 Long-Term Recommendation
                  </h2>

                  <p>
                    {
                      analysis.ai_response
                        .long_term_recommendation
                    }
                  </p>

                </section>

              </>
            )}


            {/* RAG CONTEXT */}
            <section className="panel">

              <h2>
                📚 AI Knowledge Context
              </h2>

              <p className="context-text">

                {analysis.context ||
                  "RAG knowledge context is available in the backend analysis pipeline."}

              </p>

            </section>

          </div>
        )}

      </main>


      {/* FOOTER */}
      <footer>

        <p>
          AquaGuard AI • AI for Sustainable Water Management
        </p>

      </footer>

    </div>
  );
}

export default App;