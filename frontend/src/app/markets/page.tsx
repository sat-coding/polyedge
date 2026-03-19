"use client"
import { useEffect, useState } from "react"

export default function Markets(){
  const [items,setItems]=useState<any[]>([])
  useEffect(()=>{fetch("/backend/api/markets").then(r=>r.json()).then(d=>setItems(d.items||[]))},[])
  return <main style={{padding:24,maxWidth:1200,margin:"0 auto"}}><h1>Markets</h1><table style={{width:"100%"}}><thead><tr><th>Question</th><th>YES</th><th>NO</th><th>Vol24h</th><th>Liquidity</th></tr></thead><tbody>{items.map(m=><tr key={m.id}><td>{m.question}</td><td>{m.yes_price}</td><td>{m.no_price}</td><td>{m.volume_24h}</td><td>{m.liquidity}</td></tr>)}</tbody></table></main>
}
