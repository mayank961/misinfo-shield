import { useState, useEffect } from "react";

const API = "http://127.0.0.1:8000";

const styles = `
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  :root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #00ff88;
    --accent2: #ff4466;
    --accent3: #4488ff;
    --text: #e8e8f0;
    --muted: #555570;
    --fake: #ff4466;
    --real: #00ff88;
    --unverified: #ffaa00;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    min-height: 100vh;
  }

  .dashboard {
    display: grid;
    grid-template-columns: 220px 1fr;
    min-height: 100vh;
  }

  /* SIDEBAR */
  .sidebar {
    background: var(--surface);
    border-right: 1px solid var(--border);
    padding: 32px 0;
    position: sticky;
    top: 0;
    height: 100vh;
    display: flex;
    flex-direction: column;
  }

  .logo {
    padding: 0 24px 32px;
    border-bottom: 1px solid var(--border);
  }

  .logo-icon {
    font-size: 24px;
    margin-bottom: 8px;
  }

  .logo-text {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: var(--accent);
    text-transform: uppercase;
  }

  .logo-sub {
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.05em;
    margin-top: 2px;
  }

  .nav {
    padding: 24px 12px;
    flex: 1;
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 500;
    color: var(--muted);
    transition: all 0.15s;
    margin-bottom: 4px;
    border: none;
    background: none;
    width: 100%;
    text-align: left;
  }

  .nav-item:hover { color: var(--text); background: var(--border); }
  .nav-item.active { color: var(--accent); background: rgba(0,255,136,0.08); }
  .nav-icon { font-size: 16px; width: 20px; text-align: center; }

  .status-dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    margin-left: auto;
    animation: pulse 2s infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }

  /* MAIN */
  .main {
    padding: 40px;
    overflow-y: auto;
  }

  .page-header {
    margin-bottom: 36px;
  }

  .page-title {
    font-family: 'Space Mono', monospace;
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 6px;
  }

  .page-subtitle {
    font-size: 13px;
    color: var(--muted);
  }

  /* STATS GRID */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 32px;
  }

  .stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
  }

  .stat-card:hover { border-color: var(--accent); }

  .stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent-color, var(--accent));
  }

  .stat-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
  }

  .stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 36px;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
    margin-bottom: 8px;
  }

  .stat-desc {
    font-size: 11px;
    color: var(--muted);
  }

  /* SECTION */
  .section {
    margin-bottom: 32px;
  }

  .section-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
  }

  .section-title {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: var(--text);
    text-transform: uppercase;
  }

  .section-count {
    font-size: 11px;
    color: var(--muted);
    background: var(--border);
    padding: 3px 10px;
    border-radius: 20px;
  }

  /* TABLE */
  .table-wrap {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }

  thead tr {
    background: rgba(255,255,255,0.02);
    border-bottom: 1px solid var(--border);
  }

  th {
    padding: 12px 16px;
    text-align: left;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
  }

  tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background 0.1s;
  }

  tbody tr:last-child { border-bottom: none; }
  tbody tr:hover { background: rgba(255,255,255,0.02); }

  td {
    padding: 12px 16px;
    color: var(--text);
    max-width: 300px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* BADGES */
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    font-family: 'Space Mono', monospace;
  }

  .badge-fake { background: rgba(255,68,102,0.15); color: var(--fake); }
  .badge-real { background: rgba(0,255,136,0.12); color: var(--real); }
  .badge-unverified { background: rgba(255,170,0,0.12); color: var(--unverified); }

  .score-bar {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .score-track {
    width: 60px;
    height: 4px;
    background: var(--border);
    border-radius: 2px;
    overflow: hidden;
  }

  .score-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 0.3s;
  }

  .score-num {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: var(--muted);
    min-width: 28px;
  }

  /* PENDING CARD */
  .pending-grid {
    display: grid;
    gap: 12px;
  }

  .pending-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    transition: border-color 0.2s;
  }

  .pending-card:hover { border-color: var(--accent3); }

  .pending-text {
    font-size: 14px;
    color: var(--text);
    margin-bottom: 6px;
    line-height: 1.4;
  }

  .pending-meta {
    font-size: 11px;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
  }

  .pending-actions {
    display: flex;
    gap: 8px;
    flex-shrink: 0;
  }

  .btn {
    padding: 7px 14px;
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: all 0.15s;
    font-family: 'DM Sans', sans-serif;
  }

  .btn-fake {
    background: rgba(255,68,102,0.15);
    color: var(--fake);
    border: 1px solid rgba(255,68,102,0.3);
  }

  .btn-fake:hover { background: rgba(255,68,102,0.25); }

  .btn-real {
    background: rgba(0,255,136,0.12);
    color: var(--real);
    border: 1px solid rgba(0,255,136,0.25);
  }

  .btn-real:hover { background: rgba(0,255,136,0.22); }

  /* EMPTY */
  .empty {
    padding: 48px;
    text-align: center;
    color: var(--muted);
    font-size: 13px;
  }

  /* LOADING */
  .loading {
    padding: 48px;
    text-align: center;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
  }

  /* REFRESH BTN */
  .refresh-btn {
    background: none;
    border: 1px solid var(--border);
    color: var(--muted);
    padding: 6px 12px;
    border-radius: 8px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.15s;
    font-family: 'DM Sans', sans-serif;
  }

  .refresh-btn:hover { border-color: var(--accent); color: var(--accent); }

  .approved-badge {
    font-size: 11px;
    color: var(--real);
    font-family: 'Space Mono', monospace;
    padding: 7px 14px;
  }

  /* FACTS PAGE */
  .facts-search {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 10px 16px;
    color: var(--text);
    font-size: 13px;
    width: 100%;
    max-width: 320px;
    outline: none;
    font-family: 'DM Sans', sans-serif;
    margin-bottom: 16px;
    transition: border-color 0.2s;
  }

  .facts-search:focus { border-color: var(--accent); }
  .facts-search::placeholder { color: var(--muted); }
`;

function getLabelBadge(label) {
  const l = (label || "").toLowerCase();
  if (l === "fake" || l === "गलत") return <span className="badge badge-fake">● Fake</span>;
  if (l === "real" || l === "सही") return <span className="badge badge-real">● Real</span>;
  return <span className="badge badge-unverified">● Unverified</span>;
}

function ScoreBar({ score }) {
  const color = score >= 70 ? "#00ff88" : score >= 50 ? "#ffaa00" : "#ff4466";
  return (
    <div className="score-bar">
      <div className="score-track">
        <div className="score-fill" style={{ width: `${score}%`, background: color }} />
      </div>
      <span className="score-num">{score}</span>
    </div>
  );
}

function formatTime(ts) {
  if (!ts) return "—";
  try {
    return new Date(ts).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" });
  } catch { return ts; }
}

// ===== PAGES =====

function StatsPage({ stats, loading }) {
  if (loading) return <div className="loading">LOADING STATS...</div>;
  if (!stats) return <div className="empty">No data available</div>;

  const cards = [
    { label: "Total Requests", value: stats.total_requests, desc: "All detections", color: "#4488ff" },
    { label: "Fake Detected", value: stats.fake, desc: "Misinformation caught", color: "#ff4466" },
    { label: "Real Content", value: stats.real, desc: "Verified as real", color: "#00ff88" },
    { label: "Unverified", value: stats.unverified, desc: "Uncertain predictions", color: "#ffaa00" },
    { label: "Pending Review", value: stats.pending_review, desc: "Awaiting your verdict", color: "#ff8844" },
    { label: "Facts in DB", value: stats.facts_in_db, desc: "Knowledge base size", color: "#aa44ff" },
  ];

  return (
    <>
      <div className="page-header">
        <div className="page-title">System Overview</div>
        <div className="page-subtitle">Real-time stats from your SQLite database</div>
      </div>
      <div className="stats-grid">
        {cards.map(c => (
          <div className="stat-card" key={c.label} style={{ "--accent-color": c.color }}>
            <div className="stat-label">{c.label}</div>
            <div className="stat-value" style={{ color: c.color }}>{c.value}</div>
            <div className="stat-desc">{c.desc}</div>
          </div>
        ))}
      </div>
    </>
  );
}

function LogsPage() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const load = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/admin/logs?limit=50`);
      const data = await res.json();
      setLogs(data);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  return (
    <>
      <div className="page-header">
        <div className="page-title">Detection Logs</div>
        <div className="page-subtitle">Every claim your system has analyzed</div>
      </div>
      <div className="section">
        <div className="section-header">
          <span className="section-title">Recent Activity</span>
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <span className="section-count">{logs.length} entries</span>
            <button className="refresh-btn" onClick={load}>↻ Refresh</button>
          </div>
        </div>
        <div className="table-wrap">
          {loading ? (
            <div className="loading">LOADING LOGS...</div>
          ) : logs.length === 0 ? (
            <div className="empty">No logs yet. Start analyzing claims!</div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Input</th>
                  <th>Label</th>
                  <th>Score</th>
                  <th>Language</th>
                  <th>Fact Checked</th>
                  <th>Time</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log, i) => (
                  <tr key={i}>
                    <td style={{ maxWidth: 260 }} title={log.input}>{log.input}</td>
                    <td>{getLabelBadge(log.label)}</td>
                    <td><ScoreBar score={log.score || 0} /></td>
                    <td style={{ fontFamily: "Space Mono", fontSize: 11, color: "var(--muted)" }}>
                      {log.language || "en"}
                    </td>
                    <td>
                      <span style={{ fontSize: 11, color: log.fact_checked ? "var(--real)" : "var(--muted)" }}>
                        {log.fact_checked ? "✓ Yes" : "— No"}
                      </span>
                    </td>
                    <td style={{ fontSize: 11, color: "var(--muted)", fontFamily: "Space Mono" }}>
                      {formatTime(log.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </>
  );
}

function PendingPage({ onApprove }) {
  const [pending, setPending] = useState([]);
  const [loading, setLoading] = useState(true);
  const [approved, setApproved] = useState({});

  const load = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/admin/pending`);
      const data = await res.json();
      setPending(data);
    } catch (e) { console.error(e); }
    setLoading(false);
  };

  useEffect(() => { load(); }, []);

  const approve = async (id, verdict) => {
    try {
      await fetch(`${API}/admin/pending/${id}/approve`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ verdict, explanation: `Manually marked as ${verdict}` })
      });
      setApproved(prev => ({ ...prev, [id]: verdict }));
      if (onApprove) onApprove();
    } catch (e) { console.error(e); }
  };

  return (
    <>
      <div className="page-header">
        <div className="page-title">Pending Review</div>
        <div className="page-subtitle">Claims the AI was uncertain about — your verdict improves the system</div>
      </div>
      <div className="section">
        <div className="section-header">
          <span className="section-title">Awaiting Verdict</span>
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <span className="section-count">{pending.length} claims</span>
            <button className="refresh-btn" onClick={load}>↻ Refresh</button>
          </div>
        </div>
        {loading ? (
          <div className="loading">LOADING PENDING CLAIMS...</div>
        ) : pending.length === 0 ? (
          <div className="empty" style={{ background: "var(--surface)", border: "1px solid var(--border)", borderRadius: 12 }}>
            🎉 No pending claims. System is confident in all predictions!
          </div>
        ) : (
          <div className="pending-grid">
            {pending.map(claim => (
              <div className="pending-card" key={claim.id}>
                <div style={{ flex: 1 }}>
                  <div className="pending-text">"{claim.text}"</div>
                  <div className="pending-meta">
                    Score: {claim.score} · {formatTime(claim.created_at)}
                  </div>
                </div>
                <div className="pending-actions">
                  {approved[claim.id] ? (
                    <span className="approved-badge">
                      ✓ Marked {approved[claim.id]}
                    </span>
                  ) : (
                    <>
                      <button className="btn btn-fake" onClick={() => approve(claim.id, "Fake")}>
                        Mark Fake
                      </button>
                      <button className="btn btn-real" onClick={() => approve(claim.id, "Real")}>
                        Mark Real
                      </button>
                    </>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
}

function FactsPage() {
  const [facts, setFacts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetch(`${API}/admin/facts?limit=100`)
      .then(r => r.json())
      .then(data => { setFacts(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const filtered = facts.filter(f =>
    f.claim?.toLowerCase().includes(search.toLowerCase()) ||
    f.verdict?.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <>
      <div className="page-header">
        <div className="page-title">Fact Database</div>
        <div className="page-subtitle">Your knowledge base powering semantic fact-checking</div>
      </div>
      <input
        className="facts-search"
        placeholder="Search facts..."
        value={search}
        onChange={e => setSearch(e.target.value)}
      />
      <div className="section">
        <div className="section-header">
          <span className="section-title">All Facts</span>
          <span className="section-count">{filtered.length} facts</span>
        </div>
        <div className="table-wrap">
          {loading ? (
            <div className="loading">LOADING FACTS...</div>
          ) : filtered.length === 0 ? (
            <div className="empty">No facts found.</div>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Claim</th>
                  <th>Verdict</th>
                  <th>Category</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((fact, i) => (
                  <tr key={fact.id}>
                    <td style={{ fontFamily: "Space Mono", fontSize: 11, color: "var(--muted)", width: 40 }}>
                      {i + 1}
                    </td>
                    <td style={{ maxWidth: 320 }} title={fact.claim}>{fact.claim}</td>
                    <td>{getLabelBadge(fact.verdict)}</td>
                    <td style={{ fontSize: 11, color: "var(--muted)" }}>{fact.category || "general"}</td>
                    <td style={{ fontSize: 11, color: "var(--muted)", fontFamily: "Space Mono" }}>
                      {fact.source || "manual"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </>
  );
}

// ===== MAIN APP =====

export default function AdminDashboard() {
  const [page, setPage] = useState("stats");
  const [stats, setStats] = useState(null);
  const [statsLoading, setStatsLoading] = useState(true);

  const loadStats = async () => {
    setStatsLoading(true);
    try {
      const res = await fetch(`${API}/admin/stats`);
      const data = await res.json();
      setStats(data);
    } catch (e) { console.error(e); }
    setStatsLoading(false);
  };

  useEffect(() => { loadStats(); }, []);

  const nav = [
    { id: "stats", icon: "◈", label: "Overview" },
    { id: "logs", icon: "▤", label: "Logs" },
    { id: "pending", icon: "◉", label: "Pending Review" },
    { id: "facts", icon: "◆", label: "Fact Database" },
  ];

  return (
    <>
      <style>{styles}</style>
      <div className="dashboard">
        <aside className="sidebar">
          <div className="logo">
            <div className="logo-icon">🛡️</div>
            <div className="logo-text">Misinfo Shield</div>
            <div className="logo-sub">Admin Dashboard</div>
          </div>
          <nav className="nav">
            {nav.map(n => (
              <button
                key={n.id}
                className={`nav-item ${page === n.id ? "active" : ""}`}
                onClick={() => setPage(n.id)}
              >
                <span className="nav-icon">{n.icon}</span>
                {n.label}
                {n.id === "stats" && <span className="status-dot" />}
              </button>
            ))}
          </nav>
        </aside>
        <main className="main">
          {page === "stats" && <StatsPage stats={stats} loading={statsLoading} />}
          {page === "logs" && <LogsPage />}
          {page === "pending" && <PendingPage onApprove={loadStats} />}
          {page === "facts" && <FactsPage />}
        </main>
      </div>
    </>
  );
}
