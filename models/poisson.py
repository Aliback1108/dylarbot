from __future__ import annotations
from math import exp, factorial
from typing import Dict, Tuple


def _poisson(lmbda: float, k: int) -> float:
    if lmbda <= 0:
        lmbda = 1e-6
    return (lmbda ** k) * exp(-lmbda) / factorial(k)


def score_matrix(home_lambda: float, away_lambda: float, max_goals: int = 6) -> Dict[Tuple[int, int], float]:
    m: Dict[Tuple[int, int], float] = {}
    for h in range(max_goals + 1):
        for a in range(max_goals + 1):
            m[(h, a)] = _poisson(home_lambda, h) * _poisson(away_lambda, a)
    # normalisation sécurité
    s = sum(m.values())
    if s > 0:
        for k in list(m.keys()):
            m[k] /= s
    return m


def probs_from_matrix(M: Dict[Tuple[int, int], float]) -> Dict[str, float]:
    p1 = sum(p for (h, a), p in M.items() if h > a)
    px = sum(p for (h, a), p in M.items() if h == a)
    p2 = sum(p for (h, a), p in M.items() if h < a)
    over25 = sum(p for (h, a), p in M.items() if (h + a) > 2)
    btts = sum(p for (h, a), p in M.items() if (h > 0 and a > 0))
    return {
        "1": p1, "X": px, "2": p2,
        "Over2.5": over25, "BTTS": btts
    }


def most_likely_score(M: Dict[Tuple[int, int], float]) -> str:
    (h, a), _ = max(M.items(), key=lambda kv: kv[1])
    return f"{h}-{a}"