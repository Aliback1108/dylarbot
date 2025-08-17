from __future__ import annotations
from typing import Dict, List, Tuple


def extract_team_stats(matches: List[dict], team_id: int) -> Dict[str, float]:
    if not matches:
        return {
            "gs_avg": 0.0, "gc_avg": 0.0,
            "ht_win_rate": 0.0, "st_win_rate": 0.0,
            "btts_rate": 0.0, "n": 0
        }

    gs = gc = ht_w = st_w = btts = 0
    n = len(matches)

    for m in matches:
        home_id = m["homeTeam"]["id"]
        away_id = m["awayTeam"]["id"]
        ft_home = (m["score"]["fullTime"]["home"] or 0)
        ft_away = (m["score"]["fullTime"]["away"] or 0)
        ht_home = (m["score"]["halfTime"]["home"] or 0)
        ht_away = (m["score"]["halfTime"]["away"] or 0)

        sc_home2 = ft_home - ht_home
        sc_away2 = ft_away - ht_away

        if team_id == home_id:
            gs += ft_home; gc += ft_away
            ht_w += 1 if ht_home > ht_away else 0
            st_w += 1 if sc_home2 > sc_away2 else 0
        elif team_id == away_id:
            gs += ft_away; gc += ft_home
            ht_w += 1 if ht_away > ht_home else 0
            st_w += 1 if sc_away2 > sc_home2 else 0
        btts += 1 if (ft_home > 0 and ft_away > 0) else 0

    return {
        "gs_avg": round(gs / max(1, n), 3),
        "gc_avg": round(gc / max(1, n), 3),
        "ht_win_rate": round(ht_w / max(1, n), 3),
        "st_win_rate": round(st_w / max(1, n), 3),
        "btts_rate": round(btts / max(1, n), 3),
        "n": n
    }


def relevant_matches(home_matches: List[dict], away_matches: List[dict], home_id: int, away_id: int) -> List[dict]:
    # H2H récents + derniers matchs des deux équipes (sans doublons)
    h2h = [m for m in home_matches if m["awayTeam"]["id"] == away_id]
    pool = {m["id"]: m for m in (h2h + home_matches[:10] + away_matches[:10])}
    # tri chronologique (plus récent en dernier)
    return sorted(pool.values(), key=lambda x: x.get("utcDate", ""))