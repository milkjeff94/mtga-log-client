from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import requests


class RecommendClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def recommend(
        self,
        pack_ids: List[int],
        picked_ids: Optional[List[int]] = None,
        draft_mode: str = "Premier",
        set_code: Optional[str] = None,
        detect_set: bool = True,
        timeout: float = 2.0,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "pack_ids": [int(x) for x in pack_ids],
            "picked_ids": [int(x) for x in (picked_ids or [])],
            "draft_mode": draft_mode,
            "detect_set": detect_set,
        }
        if set_code:
            payload["set"] = set_code
        resp = requests.post(f"{self.base_url}/recommend", json=payload, timeout=timeout)
        resp.raise_for_status()
        return resp.json()


def format_recommendations(recs: List[Dict[str, Any]], top_k: int = 5) -> str:
    lines = []
    for r in recs[:top_k]:
        name = r.get("name")
        rating = r.get("rating")
        synergy = r.get("synergy")
        rank = r.get("rank")
        lines.append(f"{rank:>2}. {name}  — rating {rating:.1f} (synergy {synergy:+.1f})")
    return "\n".join(lines)

