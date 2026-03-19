from fastapi import APIRouter
from app.database import get_conn

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


def _snapshot(conn, equity: float, exposure: float, drawdown: float):
    conn.execute(
        "CREATE TABLE IF NOT EXISTS equity_history (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT DEFAULT (datetime('now')), equity REAL, exposure REAL, drawdown REAL)"
    )
    conn.execute(
        "INSERT INTO equity_history (equity, exposure, drawdown) VALUES (?, ?, ?)",
        (equity, exposure, drawdown),
    )


@router.get("")
def get_portfolio():
    conn = get_conn()
    positions = [dict(r) for r in conn.execute("SELECT * FROM positions WHERE status = 'open' ORDER BY id DESC").fetchall()]
    trades = [dict(r) for r in conn.execute("SELECT * FROM trades ORDER BY id DESC LIMIT 200").fetchall()]
    signals = [dict(r) for r in conn.execute("SELECT * FROM signals ORDER BY id DESC LIMIT 200").fetchall()]

    exposure = round(sum(float(p.get("cost_basis") or 0) for p in positions), 2)
    unrealized = round(sum(float(p.get("unrealized_pnl") or 0) for p in positions), 2)
    realized = round(-sum(float(t.get("fee") or 0) for t in trades), 2)
    equity = round(1000 + realized + unrealized, 2)
    drawdown = round(max(0.0, (1000 - equity) / 1000), 4)
    win_rate = 0.0
    if positions:
        win_rate = round(sum(1 for p in positions if float(p.get("unrealized_pnl") or 0) > 0) / len(positions), 4)

    approved = sum(1 for s in signals if s.get("status") == "approved")
    rejected = sum(1 for s in signals if s.get("status") == "rejected")

    _snapshot(conn, equity, exposure, drawdown)
    conn.commit()
    conn.close()
    return {
        "cash": round(1000 - exposure * 0.1, 2),
        "equity": equity,
        "exposure": exposure,
        "positions": len(positions),
        "realized_pnl": realized,
        "unrealized_pnl": unrealized,
        "drawdown": drawdown,
        "win_rate": win_rate,
        "signals": {"approved": approved, "rejected": rejected},
        "open_positions": positions,
    }


@router.get('/equity-history')
def equity_history(limit: int = 200):
    conn = get_conn()
    conn.execute(
        "CREATE TABLE IF NOT EXISTS equity_history (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT DEFAULT (datetime('now')), equity REAL, exposure REAL, drawdown REAL)"
    )
    rows = [dict(r) for r in conn.execute("SELECT * FROM equity_history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]
    conn.close()
    rows.reverse()
    return {"items": rows}
