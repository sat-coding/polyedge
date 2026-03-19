"use client"
import { useEffect, useState } from "react"

export default function SignalsPage() {
  const [items, setItems] = useState<any[]>([])
  useEffect(() => { fetch("http://127.0.0.1:8000/api/signals").then(r=>r.json()).then(d=>setItems(d.items||[])) }, [])

  async function run(s:any){
    await fetch("http://127.0.0.1:8000/api/trades/execute",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({signal_id:s.id,market_id:s.market_id,question:s.question,direction:s.direction,price:0.5,size:Math.max(25,s.suggested_position||25)})})
    alert("Paper trade executed")
  }

  return <main style={{padding:24,maxWidth:1200,margin:"0 auto"}}><h1>Signals</h1><table style={{width:"100%"}}><thead><tr><th>Question</th><th>Dir</th><th>EV</th><th>Kelly</th><th>Reason</th><th></th></tr></thead><tbody>{items.map(s=><tr key={s.id}><td>{s.question}</td><td>{s.direction}</td><td>{s.ev_per_dollar}</td><td>{((s.kelly_fraction||0)*100).toFixed(2)}%</td><td>{s.reasoning}</td><td><button onClick={()=>run(s)}>Execute</button></td></tr>)}</tbody></table></main>
}
