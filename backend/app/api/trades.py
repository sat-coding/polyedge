from fastapi import APIRouter
from pydantic import BaseModel
from app.database import get_conn
router = APIRouter(prefix="/trades", tags=["trades"])

class TradeIn(BaseModel):
    market_id: str
    direction: str
    price: float
    size: float

@router.get("")
def list_trades():
    conn = get_conn(); rows = [dict(r) for r in conn.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 100").fetchall()]; conn.close(); return {"items": rows}

@router.post("/execute")
def execute_trade(payload: TradeIn):
    conn = get_conn(); conn.execute("INSERT INTO trades (market_id, mode, direction, price, size, status, executed_at) VALUES (?, ?, ?, ?, ?, ?, datetime(now))",(payload.market_id, "paper", payload.direction, payload.price, payload.size, "filled")); conn.commit(); conn.close(); return {"ok": True}
