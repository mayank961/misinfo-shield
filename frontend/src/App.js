import { useState, useRef } from "react";
import AdminDashboard from "./AdminDashboard";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

  *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --bg: #06060a;
    --surface: #0e0e16;
    --surface2: #13131e;
    --border: #1c1c2e;
    --border2: #252538;
    --text: #f0f0fa;
    --muted: #6b6b8a;
    --fake: #ff3355;
    --real: #00e87a;
    --unverified: #ffb020;
    --accent: #5b6af0;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Outfit', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* GRID BACKGROUND */
  .grid-bg {
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(91,106,240,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(91,106,240,0.04) 1px, transparent 1px);
    background-size: 48px 48px;
    pointer-events: none;
    z-index: 0;
  }

  .noise {
    position: fixed;
    inset: 0;
    opacity: 0.025;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
  }

  .shield-app {
    position: relative;
    z-index: 1;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 24px 80px;
  }

  /* HEADER */
  .header {
    text-align: center;
    margin-bottom: 52px;
    animation: fadeUp 0.6s ease both;
  }

  .shield-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(91,106,240,0.1);
    border: 1px solid rgba(91,106,240,0.25);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8090f8;
    margin-bottom: 24px;
  }

  .shield-dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(91,106,240,0.4); }
    50% { opacity: 0.7; box-shadow: 0 0 0 6px rgba(91,106,240,0); }
  }

  .title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(36px, 6vw, 64px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.02em;
    color: var(--text);
    margin-bottom: 16px;
  }

  .title span {
    background: linear-gradient(135deg, #5b6af0, #a78bfa, #5b6af0);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 4s linear infinite;
  }

  @keyframes shimmer {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
  }

  .subtitle {
    font-size: 16px;
    color: var(--muted);
    font-weight: 400;
    max-width: 440px;
    margin: 0 auto;
    line-height: 1.6;
  }

  /* MAIN CARD */
  .main-card {
    width: 100%;
    max-width: 680px;
    animation: fadeUp 0.6s 0.15s ease both;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  /* TEXTAREA */
  .input-wrap {
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 16px;
    transition: border-color 0.2s, box-shadow 0.2s;
  }

  .input-wrap:focus-within {
    border-color: rgba(91,106,240,0.5);
    box-shadow: 0 0 0 4px rgba(91,106,240,0.08);
  }

  .input-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  textarea {
    width: 100%;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text);
    font-family: 'Outfit', sans-serif;
    font-size: 15px;
    line-height: 1.6;
    resize: none;
    min-height: 120px;
  }

  textarea::placeholder { color: var(--muted); }

  .char-count {
    text-align: right;
    font-size: 11px;
    color: var(--muted);
    margin-top: 8px;
    font-family: monospace;
  }

  /* QUICK EXAMPLES */
  .examples {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }

  .example-btn {
    background: var(--surface2);
    border: 1px solid var(--border2);
    color: var(--muted);
    padding: 7px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s;
    font-family: 'Outfit', sans-serif;
  }

  .example-btn:hover {
    border-color: var(--accent);
    color: var(--text);
    background: rgba(91,106,240,0.08);
  }

  /* ANALYZE BUTTON */
  .analyze-btn {
    width: 100%;
    padding: 16px;
    background: var(--accent);
    border: none;
    border-radius: 14px;
    color: white;
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: 0.05em;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
  }

  .analyze-btn::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.1), transparent);
    opacity: 0;
    transition: opacity 0.2s;
  }

  .analyze-btn:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(91,106,240,0.4); }
  .analyze-btn:hover::before { opacity: 1; }
  .analyze-btn:active { transform: translateY(0); }
  .analyze-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

  /* LOADING */
  .loading-state {
    text-align: center;
    padding: 48px 0;
    animation: fadeUp 0.3s ease both;
  }

  .loading-ring {
    width: 40px; height: 40px;
    border: 2px solid var(--border2);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .loading-text {
    font-size: 13px;
    color: var(--muted);
    letter-spacing: 0.08em;
  }

  /* RESULT CARD */
  .result-card {
    margin-top: 20px;
    background: var(--surface);
    border: 1px solid var(--border2);
    border-radius: 20px;
    overflow: hidden;
    animation: fadeUp 0.4s ease both;
  }

  .result-header {
    padding: 28px 28px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }

  .verdict-block {
    display: flex;
    align-items: center;
    gap: 14px;
  }

  .verdict-icon {
    width: 52px; height: 52px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
  }

  .verdict-label {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1;
    margin-bottom: 4px;
  }

  .verdict-sub {
    font-size: 12px;
    color: var(--muted);
  }

  /* SCORE RING */
  .score-ring-wrap {
    text-align: center;
    flex-shrink: 0;
  }

  .score-ring {
    position: relative;
    width: 72px; height: 72px;
  }

  .score-ring svg {
    transform: rotate(-90deg);
  }

  .score-ring-num {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
  }

  .score-label {
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-top: 4px;
  }

  /* META PILLS */
  .meta-row {
    padding: 16px 28px;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    border-bottom: 1px solid var(--border);
  }

  .meta-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: var(--surface2);
    border: 1px solid var(--border2);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 12px;
    color: var(--muted);
  }

  .meta-pill-icon { font-size: 13px; }
  .meta-pill-val { color: var(--text); font-weight: 500; }

  /* EXPLANATION */
  .explanation {
    padding: 20px 28px 28px;
  }

  .explanation-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
  }

  .explanation-text {
    font-size: 14px;
    line-height: 1.7;
    color: #b0b0c8;
  }

  /* VERDICT COLORS */
  .verdict-fake { color: var(--fake); }
  .verdict-real { color: var(--real); }
  .verdict-unverified { color: var(--unverified); }

  .icon-fake { background: rgba(255,51,85,0.12); }
  .icon-real { background: rgba(0,232,122,0.1); }
  .icon-unverified { background: rgba(255,176,32,0.1); }

  .border-fake { border-top: 2px solid var(--fake); }
  .border-real { border-top: 2px solid var(--real); }
  .border-unverified { border-top: 2px solid var(--unverified); }

  /* ADMIN TOGGLE */
  .admin-toggle {
    position: fixed;
    top: 16px; right: 16px;
    z-index: 999;
    background: var(--surface);
    border: 1px solid var(--border2);
    color: var(--muted);
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 12px;
    font-weight: 500;
    transition: all 0.15s;
    font-family: 'Outfit', sans-serif;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .admin-toggle:hover {
    border-color: var(--accent);
    color: var(--text);
  }

  /* FOOTER */
  .footer {
    margin-top: 48px;
    text-align: center;
    font-size: 12px;
    color: var(--muted);
    animation: fadeUp 0.6s 0.3s ease both;
  }
`;

function getVerdict(label) {
  const l = (label || "").toLowerCase();
  if (l === "fake" || l === "गलत") return "fake";
  if (l === "real" || l === "सही") return "real";
  return "unverified";
}

function ScoreRing({ score, verdict }) {
  const color = verdict === "fake" ? "#ff3355" : verdict === "real" ? "#00e87a" : "#ffb020";
  const r = 30;
  const circ = 2 * Math.PI * r;
  const dash = (score / 100) * circ;

  return (
    <div className="score-ring-wrap">
      <div className="score-ring">
        <svg width="72" height="72" viewBox="0 0 72 72">
          <circle cx="36" cy="36" r={r} fill="none" stroke="#1c1c2e" strokeWidth="5" />
          <circle
            cx="36" cy="36" r={r}
            fill="none"
            stroke={color}
            strokeWidth="5"
            strokeDasharray={`${dash} ${circ}`}
            strokeLinecap="round"
          />
        </svg>
        <div className="score-ring-num" style={{ color }}>{score}</div>
      </div>
      <div className="score-label">Trust Score</div>
    </div>
  );
}

function DetectApp() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const textareaRef = useRef(null);

  const analyzeText = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch("https://mayankbh765-misinfo-shield.hf.space/detect",  {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await response.json();
      setResult(data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleKey = (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) analyzeText();
  };

  const examples = [
    { label: "🧪 Fake example", text: "Breaking news! Miracle cure found!" },
    { label: "✅ Real example", text: "Water boils at 100 degrees Celsius" },
    { label: "🦠 Health myth", text: "Drinking hot water cures COVID" },
    { label: "📡 5G myth", text: "5G towers spread coronavirus" },
  ];

  const verdict = result ? getVerdict(result.label_en) : null;
  const verdictIcons = { fake: "⚠", real: "✓", unverified: "?" };

  return (
    <>
      <style>{styles}</style>
      <div className="grid-bg" />
      <div className="noise" />

      <div className="shield-app">
        <header className="header">
          <div className="shield-badge">
            <span className="shield-dot" />
            AI-Powered Detection
          </div>
          <h1 className="title">
            Misinformation<br /><span>Shield</span>
          </h1>
          <p className="subtitle">
            Detect fake news, health myths, and viral misinformation in seconds — powered by AI and real-time fact checking.
          </p>
        </header>

        <div className="main-card">
          <div className="input-wrap">
            <div className="input-label">
              <span>📋</span> Paste claim or message
            </div>
            <textarea
              ref={textareaRef}
              placeholder="Paste a WhatsApp forward, news headline, or any claim here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
              onKeyDown={handleKey}
            />
            <div className="char-count">{text.length} chars · Ctrl+Enter to analyze</div>
          </div>

          <div className="examples">
            {examples.map(ex => (
              <button key={ex.label} className="example-btn" onClick={() => setText(ex.text)}>
                {ex.label}
              </button>
            ))}
          </div>

          <button
            className="analyze-btn"
            onClick={analyzeText}
            disabled={loading || !text.trim()}
          >
            {loading ? "Analyzing..." : "Analyze Claim →"}
          </button>

          {loading && (
            <div className="loading-state">
              <div className="loading-ring" />
              <div className="loading-text">Running AI analysis...</div>
            </div>
          )}

          {result && !loading && (
            <div className={`result-card border-${verdict}`}>
              <div className="result-header">
                <div className="verdict-block">
                  <div className={`verdict-icon icon-${verdict}`}>
                    {verdictIcons[verdict]}
                  </div>
                  <div>
                    <div className={`verdict-label verdict-${verdict}`}>
                      {result.label}
                    </div>
                    <div className="verdict-sub">
                      {verdict === "fake" && "This claim appears to be misinformation"}
                      {verdict === "real" && "This claim appears to be accurate"}
                      {verdict === "unverified" && "Could not verify this claim with confidence"}
                    </div>
                  </div>
                </div>
                <ScoreRing score={result.score} verdict={verdict} />
              </div>

              <div className="meta-row">
                <div className="meta-pill">
                  <span className="meta-pill-icon">{result.flag || "🌐"}</span>
                  <span className="meta-pill-val">
                    {result.language_name || result.language?.toUpperCase() || "EN"}
                  </span>
                </div>
                <div className="meta-pill">
                  <span className="meta-pill-icon">🔍</span>
                  Fact Checked: <span className="meta-pill-val">&nbsp;{result.fact_checked ? "Yes" : "No"}</span>
                </div>
                {result.fact_confidence && (
                  <div className="meta-pill">
                    <span className="meta-pill-icon">📊</span>
                    Match Confidence: <span className="meta-pill-val">&nbsp;{Math.round(result.fact_confidence * 100)}%</span>
                  </div>
                )}
              </div>

              <div className="explanation">
                <div className="explanation-label">Analysis</div>
                <div className="explanation-text">{result.reason}</div>
              </div>
            </div>
          )}
        </div>

        <footer className="footer">
          Powered by XLM-RoBERTa · Semantic Fact Matching · Google Fact Check API
        </footer>
      </div>
    </>
  );
}

export default function App() {
  const [isAdmin, setIsAdmin] = useState(false);

  return (
    <>
      <button className="admin-toggle" onClick={() => setIsAdmin(!isAdmin)}>
        {isAdmin ? "← Shield" : "⚙ Admin"}
      </button>
      {isAdmin ? <AdminDashboard /> : <DetectApp />}
    </>
  );
}