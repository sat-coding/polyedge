from app.config import settings
from app.core.formulas import expected_value, kelly_fraction
from app.models.signal import TradeSignal
from app.integrations.openai_client import OpenAIClient

class MarketAnalyst:
    def __init__(self): self.client = OpenAIClient()

    async def analyze(self, market: dict) -> TradeSignal:
        data = await self.client.estimate(market["question"], market["yes_price"])
        ev = expected_value(market["yes_price"], data["probability"])
        kf = kelly_fraction(data["probability"], market["yes_price"], settings.kelly_multiplier)
        pos = round(settings.bankroll * min(kf, 0.05), 2)
        direction = "BUY_YES" if ev > settings.ev_threshold else "SKIP"
        factors = ", ".join(data.get("key_factors", [])[:3])
        risks = ", ".join(data.get("risks_to_estimate", [])[:2])
        reasoning = f"{data["reasoning"]} | factors: {factors or "n/a"} | risks: {risks or "n/a"}"
        return TradeSignal(market_id=market["id"],question=market["question"],market_price=market["yes_price"],ai_probability=data["probability"],confidence=data["confidence"],ev_per_dollar=round(ev,6),kelly_fraction=round(kf,6),position_size=pos,direction=direction,reasoning=reasoning)
