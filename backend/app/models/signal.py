from pydantic import BaseModel

class TradeSignal(BaseModel):
    market_id: str
    question: str
    market_price: float
    ai_probability: float
    confidence: str
    ev_per_dollar: float
    kelly_fraction: float
    position_size: float
    direction: str
    reasoning: str
