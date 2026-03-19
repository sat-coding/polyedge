from fastapi import APIRouter
from app.database import get_conn
from app.integrations.news_sources import fetch_news

router = APIRouter(prefix="/news", tags=["news"])


@router.get("")
def list_news():
    conn = get_conn()
    rows = [dict(r) for r in conn.execute("SELECT * FROM news_items ORDER BY id DESC LIMIT 40").fetchall()]
    conn.close()
    return {"items": rows}


@router.post("/refresh")
async def refresh_news():
    items = await fetch_news(limit_per_feed=8)
    conn = get_conn()
    conn.execute("DELETE FROM news_items")
    conn.executemany(
        "INSERT INTO news_items (title, source, published_at, sentiment, impact_score, related_market, summary) VALUES (?, ?, ?, ?, ?, ?, ?)",
        [(i["title"], i["source"], i["published_at"], i["sentiment"], i["impact_score"], i["related_market"], i["summary"]) for i in items],
    )
    conn.commit()
    conn.close()
    return {"ok": True, "count": len(items)}
