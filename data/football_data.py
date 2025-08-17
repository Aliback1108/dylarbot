from __future__ import annotations
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import requests

from config import BASE_URL, API_TOKEN, REQUEST_TIMEOUT

HEADERS = {"X-Auth-Token": API_TOKEN}

class FootballDataClient:
    def __init__(self):
        if not API_TOKEN:
            raise RuntimeError("FOOTBALL_DATA_TOKEN manquant. Ajoute-le dans l'environnement.")

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{BASE_URL}{path}"
        for attempt in range(3):
            try:
                r = requests.get(url, headers=HEADERS, params=params, timeout=REQUEST_TIMEOUT)
                if r.status_code == 429:
                    # rate-limit → backoff simple
                    time.sleep(1.5 * (attempt + 1))
                    continue
                r.raise_for_status()
                return r.json()
            except requests.RequestException as e:
                if attempt == 2:
                    raise
                time.sleep(0.8 * (attempt + 1))
        return {}

    def team_logo(self, team_id: int) -> str:
        data = self._get(f"/teams/{team_id}")
        return data.get("crest", "")

    def team_matches(self, team_id: int, days: int = 120, limit: int = 20) -> List[Dict[str, Any]]:
        date_from = (datetime.utcnow() - timedelta(days=days)).strftime('%Y-%m-%d')
        date_to = datetime.utcnow().strftime('%Y-%m-%d')
        params = {
            "status": "FINISHED",
            "dateFrom": date_from,
            "dateTo": date_to,
            "limit": limit,
        }
        data = self._get(f"/teams/{team_id}/matches", params)
        return data.get("matches", [])