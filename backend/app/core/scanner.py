from app.config import settings
from app.core.analyst import MarketAnalyst
from app.core.risk_manager import RiskManager, RiskConfig
from app.integrations.gamma_client import GammaClient

class MarketScanner:
    def __init__(self):
        self.gamma = GammaClient(); self.analyst = MarketAnalyst(); self.risk = RiskManager(RiskConfig(paper_trading=settings.paper_trading))

    async def full_scan(self) -> list[dict]:
        markets = await self.gamma.get_active_markets(limit=80)
        filtered = [m for m in markets if m["volume_24h"] >= 5000 and 0.05 < m["yes_price"] < 0.95][:30]
        signals = []
        for m in filtered:
            sig = await self.analyst.analyze(m)
            ok, reason = self.risk.check_trade(sig, settings.bankroll)
            d = sig.model_dump(); d["risk_check_result"] = reason
            if ok and d["direction"] != "SKIP": signals.append(d)
        signals.sort(key=lambda x: x["ev_per_dollar"], reverse=True)
        return signals[:5]
