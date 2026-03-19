from fastapi import APIRouter
from app.core.scanner import MarketScanner
router = APIRouter(prefix="/signals", tags=["signals"])

@router.get("")
async def list_signals(): return {"items": await MarketScanner().full_scan()}

@router.post("/scan")
async def scan_now(): return await list_signals()
