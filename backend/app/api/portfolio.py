from fastapi import APIRouter
from app.database import get_conn
router = APIRouter(prefix="/portfolio", tags=["portfolio"])

@router.get("")
def get_portfolio():
    conn = get_conn(); rows = [dict(r) for r in conn.execute("SELECT * FROM trades ORDER BY id DESC").fetchall()]; conn.close()
    exposure = round(sum(float(r.get("size") or 0) for r in rows), 2)
    return {"cash": round(1000 - exposure * 0.1, 2), "exposure": exposure, "positions": len(rows)}
