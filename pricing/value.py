from __future__ import annotations

def implied_probability(odds: float) -> float:
    if odds <= 1.0:
        return 1.0
    return 1.0 / odds

def expected_value(prob: float, odds: float) -> float:
    # EV = prob*odds - 1 (en unités de mise)
    return prob * max(1.0, odds) - 1.0

def kelly_fraction(prob: float, odds: float, fraction: float = 0.3) -> float:
    # Kelly = ((p*o - 1)/(o-1)) ; fraction pour limiter la variance
    o = max(1.01, odds)
    num = prob * o - 1.0
    den = o - 1.0
    raw = num / den
    return max(0.0, raw * fraction)
