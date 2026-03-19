"use client"

import { useEffect, useState } from "react"
import LineChart from "../components/LineChart"

type Portfolio = any

export default function Home() {
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null)
  const [signals, setSignals] = useState<any[]>([])
  const [trades, setTrades] = useState<any[]>([])
  const [news, setNews] = useState<any[]>([])
  const [equityCurve, setEquityCurve] = useState<number[]>([])

  async function load() {
    const [p, s, t, n, b] = await Promise.all([
      fetch("/backend/api/portfolio").then(r => r.json()),
      fetch("/backend/api/signals").then(r => r.json()),
      fetch("/backend/api/trades").then(r => r.json()),
      fetch("/backend/api/news/refresh", { method: "POST" }).then(() => fetch("/backend/api/news")).then(r => r.json()),
      fetch("/backend/api/backtest/run", { method: "POST" }).then(r => r.json()),
    ])
    setPortfolio(p)
    setSignals(s.items || [])
    setTrades(t.items || [])
    setNews(n.items || [])
    setEquityCurve(b.equity_curve || [])
  }

  useEffect(() => {
    load()
    const id = setInterval(load, 15000)
    return () => clearInterval(id)
  }, [])

  async function executeFromSignal(s: any) {
    await fetch("/backend/api/trades/execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ signal_id: s.id, market_id: s.market_id, question: s.question, direction: s.direction, price: 0.5, size: Math.max(25, s.suggested_position || 25) })
    })
    await fetch("/backend/api/trades/mark", { method: "POST" })
    await load()
  }

  const riskPct = Math.min(100, ((portfolio?.drawdown || 0) * 100) + ((portfolio?.exposure || 0) / 20))

  return (
    <main style={{ maxWidth: 1280, margin: "0 auto", padding: 24 }}>
      <h1 style={{ marginBottom: 4 }}>PolyEdge — Trading Command Center</h1>
      <p style={{ color: "#888899", marginTop: 0 }}>Signals, risk, news impact, execution lifecycle</p>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(6,1fr)", gap: 10 }}>
        <K title="Equity" value={`$${portfolio?.equity ?? "-"}`} />
        <K title="Cash" value={`$${portfolio?.cash ?? "-"}`} />
        <K title="Exposure" value={`$${portfolio?.exposure ?? "-"}`} />
        <K title="Unrealized" value={`$${portfolio?.unrealized_pnl ?? "-"}`} />
        <K title="Realized" value={`$${portfolio?.realized_pnl ?? "-"}`} />
        <K title="Win Rate" value={`${((portfolio?.win_rate || 0) * 100).toFixed(1)}%`} />
      </section>

      <section style={{ display: "grid", gridTemplateColumns: "2fr 1fr", gap: 14, marginTop: 14 }}>
        <Panel title="Equity Curve (Backtest)">
          <LineChart values={equityCurve} />
        </Panel>
        <Panel title="Risk Gauge">
          <div style={{ height: 18, borderRadius: 999, border: "1px solid #1E1E2E", overflow: "hidden", background: "#12121A" }}>
            <div style={{ width: `${riskPct}%`, height: "100%", background: riskPct > 70 ? "#FF5252" : riskPct > 40 ? "#FFD740" : "#00E676" }} />
          </div>
          <p style={{ color: "#888899" }}>Drawdown {(portfolio?.drawdown * 100 || 0).toFixed(2)}% · Exposure ${portfolio?.exposure || 0}</p>
          <p style={{ color: "#888899" }}>Signals: ✅ {portfolio?.signals?.approved || 0} · ❌ {portfolio?.signals?.rejected || 0}</p>
        </Panel>
      </section>

      <section style={{ display: "grid", gridTemplateColumns: "1.6fr 1fr", gap: 14, marginTop: 14 }}>
        <Panel title="Signal Queue">
          <Table headers={["Market", "Dir", "EV", "Kelly", "Risk", "Action"]} rows={(signals || []).slice(0, 12).map((s) => [
            s.question?.slice(0, 52) || s.market_id,
            chip(s.direction),
            num(s.ev_per_dollar),
            `${((s.kelly_fraction || 0) * 100).toFixed(2)}%`,
            s.risk_check_result,
            <button key={s.id} onClick={() => executeFromSignal(s)} style={btnPrimary}>Execute</button>
          ])} />
        </Panel>

        <Panel title="News Impact">
          {(news || []).map((n: any) => (
            <div key={n.id} style={{ borderBottom: "1px solid #1E1E2E", padding: "10px 0" }}>
              <div style={{ fontWeight: 600 }}>{n.title}</div>
              <div style={{ color: "#888899", fontSize: 13 }}>{n.source} · impact {(n.impact_score * 100).toFixed(0)}% · sentiment {n.sentiment}</div>
              <div style={{ color: "#aaaab9", fontSize: 13 }}>{n.summary}</div>
            </div>
          ))}
        </Panel>
      </section>

      <section style={{ marginTop: 14 }}>
        <Panel title="Trade Journal">
          <Table headers={["ID", "Market", "Direction", "Size", "Price", "Status", "Time"]} rows={(trades || []).slice(0, 16).map((t) => [t.id, t.market_id, t.direction, `$${num(t.size)}`, num(t.price), t.status, t.executed_at || t.created_at])} />
        </Panel>
      </section>
    </main>
  )
}

function K({ title, value }: { title: string; value: string }) {
  return <div style={{ background: "#12121A", border: "1px solid #1E1E2E", borderRadius: 12, padding: 12 }}><div style={{ color: "#888899", fontSize: 12 }}>{title}</div><div style={{ fontSize: 24, fontWeight: 700 }}>{value}</div></div>
}
function Panel({ title, children }: { title: string; children: React.ReactNode }) {
  return <div style={{ background: "#12121A", border: "1px solid #1E1E2E", borderRadius: 12, padding: 14 }}><h3 style={{ marginTop: 0 }}>{title}</h3>{children}</div>
}
function Table({ headers, rows }: { headers: any[]; rows: any[][] }) {
  return <table style={{ width: "100%", borderCollapse: "collapse" }}><thead><tr>{headers.map((h, i) => <th key={i} style={{ textAlign: "left", color: "#888899", borderBottom: "1px solid #1E1E2E", padding: "8px 6px" }}>{h}</th>)}</tr></thead><tbody>{rows.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j} style={{ borderBottom: "1px solid #1E1E2E", padding: "8px 6px" }}>{c}</td>)}</tr>)}</tbody></table>
}
function num(v: any) { return Number(v || 0).toFixed(3) }
function chip(v: string) { return <span style={{ padding: "4px 8px", borderRadius: 999, background: v?.includes("BUY") ? "#0e2a1e" : "#2a1818", color: v?.includes("BUY") ? "#00E676" : "#FF5252", fontSize: 12 }}>{v}</span> }

const btnPrimary: React.CSSProperties = { background: "#6C63FF", color: "white", border: "none", borderRadius: 8, padding: "6px 10px", cursor: "pointer" }
