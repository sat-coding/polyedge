from fastapi import APIRouter
from app.integrations.gamma_client import GammaClient
router = APIRouter(prefix="/markets", tags=["markets"])

@router.get("")
async def list_markets():
    return {"items": await GammaClient().get_active_markets(limit=50)}
