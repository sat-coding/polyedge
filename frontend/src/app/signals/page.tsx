"use client"
import { useEffect, useState } from "react"

export default function SignalsPage() {
  const [items, setItems] = useState<any[]>([])
  useEffect(() => { fetch("/backend/api/signals").then(r=>r.json()).then(d=>setItems(d.items||[])) }, [])

  return <main style={{padding:24,maxWidth:1200,margin:"0 auto"}}><h1>Signals</h1><table style={{width:"100%"}}><thead><tr><th>Question</th><th>Dir</th><th>EV</th><th>Kelly</th><th>Reason</th></tr></thead><tbody>{items.map(s=><tr key={s.id}><td>{s.question}</td><td>{s.direction}</td><td>{s.ev_per_dollar}</td><td>{((s.kelly_fraction||0)*100).toFixed(2)}%</td><td>{s.reasoning}</td></tr>)}</tbody></table></main>
}
