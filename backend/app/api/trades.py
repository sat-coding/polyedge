from fastapi import APIRouter
from pydantic import BaseModel
from app.database import get_conn
from app.core.formulas import log_return

router = APIRouter(prefix="/trades", tags=["trades"])


class TradeIn(BaseModel):
    signal_id: int | None = None
    market_id: str
    question: str | None = None
    direction: str
    price: float
    size: float


@router.get("")
def list_trades():
    conn = get_conn()
    rows = [dict(r) for r in conn.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 150").fetchall()]
    conn.close()
    return {"items": rows}


@router.post("/execute")
def execute_trade(payload: TradeIn):
    conn = get_conn()
    shares = payload.size / max(payload.price, 0.01)
    fee = payload.size * 0.01
    conn.execute(
        "INSERT INTO trades (signal_id, market_id, mode, direction, price, size, shares, fee, status, executed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime(now))",
        (payload.signal_id, payload.market_id, "paper", payload.direction, payload.price, payload.size, shares, fee, "filled"),
    )

    conn.execute(
        "INSERT INTO positions (market_id, question, direction, entry_price, current_price, shares, cost_basis, unrealized_pnl, log_return, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            payload.market_id,
            payload.question or payload.market_id,
            payload.direction,
            payload.price,
            payload.price,
            shares,
            payload.size,
            0.0,
            0.0,
            "open",
        ),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@router.post("/mark")
def mark_positions():
    conn = get_conn()
    rows = [dict(r) for r in conn.execute("SELECT * FROM positions WHERE status = open").fetchall()]
    for p in rows:
        # simple mark simulation
        current = max(0.02, min(0.98, float(p["current_price"] or p["entry_price"]) * 1.002))
        pnl = (current - p["entry_price"]) * p["shares"]
        lr = log_return(max(0.01, p["entry_price"]), max(0.01, current))
        conn.execute("UPDATE positions SET current_price=?, unrealized_pnl=?, log_return=? WHERE id=?", (current, pnl, lr, p["id"]))
    conn.commit()
    conn.close()
    return {"ok": True, "marked": len(rows)}
