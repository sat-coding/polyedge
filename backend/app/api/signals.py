from fastapi import APIRouter
from app.core.scanner import MarketScanner
from app.database import get_conn

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
                "gpt-5.4-fallback", "medium", s.get("risk_check_result", "unknown"), "approved" if s["direction"] != "SKIP" else "rejected",
            ),
        )
    conn.commit()
    conn.close()


@router.get("")
async def list_signals():
    scanner = MarketScanner()
    fresh = await scanner.full_scan()
    if fresh:
        _persist_signals(fresh)

    conn = get_conn()
    rows = [dict(r) for r in conn.execute("SELECT * FROM signals ORDER BY id DESC LIMIT 50").fetchall()]
    conn.close()
    return {"items": rows}


@router.post("/scan")
async def scan_now():
    return await list_signals()
