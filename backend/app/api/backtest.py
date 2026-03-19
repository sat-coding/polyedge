from fastapi import APIRouter
import random
router = APIRouter(prefix="/backtest", tags=["backtest"])

@router.post("/run")
def run_backtest():
    equity=[1000.0]
    for _ in range(60): equity.append(round(equity[-1]*(1+random.uniform(-0.015,0.02)),2))
    return {"equity_curve":equity,"final":equity[-1],"return_pct":round((equity[-1]/equity[0]-1)*100,2)}
