"use client"
import { useState } from "react"
import LineChart from "../../components/LineChart"

export default function Backtest(){
  const [curve,setCurve]=useState<number[]>([])
  const [stats,setStats]=useState<any>(null)
  async function run(){
    const d=await fetch("http://127.0.0.1:8000/api/backtest/run",{method:"POST"}).then(r=>r.json())
    setCurve(d.equity_curve||[]); setStats(d)
  }
  return <main style={{padding:24,maxWidth:1100,margin:"0 auto"}}><h1>Backtest</h1><button onClick={run}>Run backtest</button>{stats&&<p>Final ${stats.final} · Return {stats.return_pct}%</p>}{curve.length>0&&<LineChart values={curve} />}</main>
}
