from dataclasses import dataclass
from app.models.signal import TradeSignal

@dataclass
class RiskConfig:
    max_bankroll_pct: float = 0.10
    max_total_exposure: float = 0.50
    max_drawdown_pct: float = 0.20
    min_ev_threshold: float = 0.05
    min_confidence: str = "medium"
    max_markets: int = 10
    paper_trading: bool = True

class RiskManager:
    def __init__(self, config: RiskConfig):
        self.config = config
        self.current_drawdown = 0.0
        self.open_positions: list[dict] = []

    def check_trade(self, signal: TradeSignal, bankroll: float) -> tuple[bool, str]:
        if self.config.paper_trading: return True, "PAPER_MODE"
        if self.current_drawdown >= self.config.max_drawdown_pct: return False, "DRAWDOWN_LIMIT"
        if signal.ev_per_dollar < self.config.min_ev_threshold: return False, "LOW_EV"
        rank = {"high": 3, "medium": 2, "low": 1}
        if rank.get(signal.confidence, 0) < rank[self.config.min_confidence]: return False, "LOW_CONFIDENCE"
        if signal.position_size > bankroll * self.config.max_bankroll_pct: return False, "POSITION_TOO_LARGE"
        exposure = sum(p.get("size", 0.0) for p in self.open_positions) + signal.position_size
        if exposure > bankroll * self.config.max_total_exposure: return False, "TOTAL_EXPOSURE_LIMIT"
        if len(self.open_positions) >= self.config.max_markets: return False, "MAX_MARKETS"
        return True, "APPROVED"
