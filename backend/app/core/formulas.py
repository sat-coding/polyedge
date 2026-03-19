import math

def expected_value(market_price: float, true_prob: float) -> float:
    return true_prob * (1 - market_price) - (1 - true_prob) * market_price

def kelly_fraction(true_prob: float, market_price: float, kelly_multiplier: float = 0.25) -> float:
    if market_price <= 0 or market_price >= 1: return 0.0
    b = (1 - market_price) / market_price
    p = true_prob; q = 1 - p
    f = (p * b - q) / b
    return max(f, 0.0) * kelly_multiplier

def bayesian_update(prior: float, likelihood: float, evidence: float) -> float:
    if evidence <= 0: return prior
    posterior = (likelihood * prior) / evidence
    return min(max(posterior, 0.01), 0.99)

def log_return(price_start: float, price_end: float) -> float:
    if price_start <= 0 or price_end <= 0: return 0.0
    return math.log(price_end / price_start)
