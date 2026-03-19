import httpx

class GammaClient:
    BASE_URL = "https://gamma-api.polymarket.com"

    async def get_active_markets(self, limit: int = 100) -> list[dict]:
        url = f"{self.BASE_URL}/markets?active=true&closed=false&limit={limit}"
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                res = await client.get(url); res.raise_for_status(); arr = res.json()
        except Exception:
            arr = []
        out = []
        for m in arr[:limit]:
            last = float(m.get("lastTradePrice") or 0.5)
            out.append({"id": m.get("id") or m.get("slug") or "unknown","question": m.get("question") or "unknown","category": m.get("category") or "other","yes_price": last,"no_price": round(1-last,4),"volume_24h": float(m.get("volume24hr") or 0),"liquidity": float(m.get("liquidity") or 0),"end_date": m.get("endDate")})
        return out
