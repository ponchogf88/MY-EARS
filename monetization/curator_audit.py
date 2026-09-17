"""
Curator Audit Tool for MY EARS.
Audita si una playlist cumple con los requisitos para monetizar en Playlist Push, SubmitHub y Groover.
"""

import json
from pathlib import Path
from typing import Dict, Any, List

class CuratorAuditor:
    def __init__(self, strategy_path: str = "config/monetization_strategy.json"):
        self.strategy_path = Path(strategy_path)
        self.strategy = self._load_strategy()

    def _load_strategy(self) -> Dict[str, Any]:
        if not self.strategy_path.exists():
            return {}
        with open(self.strategy_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def audit_playlist(self, current_followers: int, track_count: int, monthly_listeners: int = 0) -> Dict[str, Any]:
        """
        Evalúa el estado de elegibilidad de la playlist frente a las plataformas de monetización.
        """
        platforms = self.strategy.get("platforms", {})
        evaluation = {}

        for p_key, p_data in platforms.items():
            min_fol = p_data.get("min_followers", 0)
            min_tra = p_data.get("min_tracks", 20)
            max_tra = p_data.get("max_tracks", 150)

            followers_ok = current_followers >= min_fol
            tracks_ok = min_tra <= track_count <= max_tra

            remaining_followers = max(0, min_fol - current_followers)
            percentage_reached = min(100.0, round((current_followers / min_fol) * 100, 1)) if min_fol > 0 else 100.0

            evaluation[p_key] = {
                "name": p_data.get("name"),
                "eligible": followers_ok and tracks_ok,
                "followers_required": min_fol,
                "current_followers": current_followers,
                "remaining_followers": remaining_followers,
                "progress_percentage": percentage_reached,
                "track_count_valid": tracks_ok,
                "payout": p_data.get("estimated_payout_per_review"),
                "criteria": p_data.get("verification_criteria", [])
            }

        return {
            "summary": {
                "followers": current_followers,
                "tracks": track_count,
                "listeners": monthly_listeners
            },
            "platforms": evaluation
        }
