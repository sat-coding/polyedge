from fastapi import APIRouter
from app.core.scanner import MarketScanner
from app.database import get_conn
from app.config import settings

router = APIRouter(prefix="/signals", tags=["signals"])


def _persist_signals(items: list[dict]) -> None:
    conn = get_conn()
    for s in items:
        conn.execute(
            """
            INSERT INTO signals (market_id, question, ai_probability, confidence, ev_per_dollar, kelly_fraction,
                                 suggested_position, direction, reasoning, model_used, reasoning_effort, risk_check_result, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                s["market_id"], s["question"], s["ai_probability"], s["confidence"], s["ev_per_dollar"],
                s["kelly_fraction"], s["position_size"], s["direction"], s["reasoning"],
                "gpt-5.4", "medium", s.get("risk_check_result", "unknown"), "approved" if s["direction"] != "SKIP" else "rejected",
            ),
        )
    conn.commit()
    conn.close()


def _autonomous_execute(items: list[dict]) -> int:
    if not settings.autonomous_mode:
        return 0

    conn = get_conn()
    executed = 0
    for s in items:
        if s.get("direction") == "SKIP":
            continue
        exists = conn.execute(
            "SELECT 1 FROM trades WHERE market_id=? AND created_at >= datetime('now','-30 minutes') LIMIT 1",
            (s["market_id"],),
        ).fetchone()
        if exists:
            continue

        size = max(20.0, float(s.get("position_size") or 20.0))
        price = float(s.get("market_price") or 0.5)
        shares = size / max(price, 0.01)
        fee = size * 0.01

        conn.execute(
            "INSERT INTO trades (market_id, mode, direction, price, size, shares, fee, status, executed_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))",
            (s["market_id"], "paper-auto", s["direction"], price, size, shares, fee, "filled"),
        )
        conn.execute(
            "INSERT INTO positions (market_id, question, direction, entry_price, current_price, shares, cost_basis, unrealized_pnl, log_return, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (s["market_id"], s["question"], s["direction"], price, price, shares, size, 0.0, 0.0, "open"),
        )
        executed += 1

    conn.commit()
    conn.close()
    return executed


@router.get("")
async def list_signals():
    scanner = MarketScanner()
    fresh = await scanner.full_scan()
    if fresh:
        _persist_signals(fresh)
        _autonomous_execute(fresh)

    conn = get_conn()
    rows = [dict(r) for r in conn.execute("SELECT * FROM signals ORDER BY id DESC LIMIT 50").fetchall()]
    conn.close()
    return {"items": rows, "autonomous_mode": settings.autonomous_mode}


@router.post("/scan")
async def scan_now():
    return await list_signals()
