from fastapi import APIRouter
from app.database import get_conn

router = APIRouter(prefix="/news", tags=["news"])


@router.get("")
def list_news():
    conn = get_conn()
    rows = [dict(r) for r in conn.execute("SELECT * FROM news_items ORDER BY id DESC LIMIT 30").fetchall()]
    conn.close()
    return {"items": rows}
