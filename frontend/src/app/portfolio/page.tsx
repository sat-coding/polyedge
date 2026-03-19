"use client"
import { useEffect, useState } from "react"

export default function PortfolioPage(){
  const [p,setP]=useState<any>(null)
  useEffect(()=>{fetch("http://127.0.0.1:8000/api/portfolio").then(r=>r.json()).then(setP)},[])
  return <main style={{padding:24,maxWidth:1100,margin:"0 auto"}}><h1>Portfolio</h1>
    <pre style={{background:"#12121A",padding:12,border:"1px solid #1E1E2E",borderRadius:8}}>{JSON.stringify(p,null,2)}</pre>
  </main>
}
