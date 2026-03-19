from __future__ import annotations
import datetime as dt
import xml.etree.ElementTree as ET
import httpx

RSS_FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("Cointelegraph", "https://cointelegraph.com/rss"),
    ("Reuters World", "https://feeds.reuters.com/Reuters/worldNews"),
]


def _score(title: str) -> tuple[float, float, str]:
    t = title.lower()
    positive = ["surge", "rise", "approve", "win", "growth", "inflow", "bull"]
    negative = ["drop", "fall", "ban", "hack", "lawsuit", "risk", "bear"]
    p = sum(1 for w in positive if w in t)
    n = sum(1 for w in negative if w in t)
    sentiment = max(-1.0, min(1.0, (p - n) / 3))
    impact = min(1.0, 0.3 + (p + n) * 0.12)
    related = "btc" if "bitcoin" in t or "btc" in t else "eth" if "ethereum" in t or "eth" in t else "macro"
    return sentiment, impact, related


async def fetch_news(limit_per_feed: int = 10) -> list[dict]:
    out: list[dict] = []
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        for source, url in RSS_FEEDS:
            try:
                r = await client.get(url)
                r.raise_for_status()
                root = ET.fromstring(r.text)
                items = root.findall(".//item")[:limit_per_feed]
                for it in items:
                    title = (it.findtext("title") or "").strip()
                    pub = (it.findtext("pubDate") or dt.datetime.utcnow().isoformat()).strip()
                    if not title:
                        continue
                    s, impact, related = _score(title)
                    out.append(
                        {
                            "title": title,
                            "source": source,
                            "published_at": pub,
                            "sentiment": round(s, 3),
                            "impact_score": round(impact, 3),
                            "related_market": related,
                            "summary": title,
                        }
                    )
            except Exception:
                continue
    return out[:30]
