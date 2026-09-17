"""
Influencer & Campaign Engine for MY EARS.
Genera guiones de video y storyboards optimizados para alta retención (0-3s),
diseñados para los 2 creadores en situaciones de la vida diaria conectando con la playlist.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class InfluencerEngine:
    def __init__(self, config_path: str = "config/soul_keywords.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_campaign(
        self,
        playlist_name: str,
        playlist_url: str,
        mood_data: Dict[str, Any],
        featured_track: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Genera el paquete completo de distribución para los 2 influencers.
        """
        influencers = self.config.get("influencers", {})
        inf1_info = influencers.get("influencer_1", {})
        inf2_info = influencers.get("influencer_2", {})

        keyword = mood_data.get("primary_keyword", "esencia")
        category = mood_data.get("category_key", "introspeccion_profunda").replace("_", " ")
        song_name = featured_track.get("title", "Track")
        artist_name = featured_track.get("artist", "Artista")

        # Guión Influencer 1 (Alex - Cotidiano y Cercano)
        script_1 = {
            "creator": inf1_info.get("name", "Alex"),
            "format": "Instagram Story / Reel vertical (9:16, 15-20s)",
            "hook_0_to_3s": f"¿Alguna vez han sentido que el ruido del día simplemente satura todo?",
            "visual_direction": "Plano medio en primera persona (POV). Alex caminando con café en mano o en el auto durante una pausa, colocándose los audífonos con calma.",
            "audio_track": f"'{song_name}' de {artist_name} (iniciando al segundo 0:04)",
            "voiceover_body": (
                f"Llevaba un día pesado hasta que le di play a esta selección: '{playlist_name}'. "
                f"Te baja las revoluciones de golpe y te regresa a tu centro. Una joya para caminar o desconectar un rato."
            ),
            "call_to_action": f"Les dejo el sticker directo a Spotify para que la guarden. Háganse ese favor hoy.",
            "sticker_link": playlist_url,
            "on_screen_text": f"🎧 {playlist_name}\nTrack: {song_name} - {artist_name}"
        }

        # Guión Influencer 2 (Valeria - Energía y Cambio de Vibe)
        script_2 = {
            "creator": inf2_info.get("name", "Valeria"),
            "format": "TikTok / Reel vertical (9:16, 15-25s)",
            "hook_0_to_3s": f"Para un segundo... si tu energía hoy está en 20%, necesitas escuchar esto YA.",
            "visual_direction": "Corte dinámico rápido. Al inicio: expresión agotada frente a la laptop o en el gym. Beat drop: sonríe, sube el volumen, cambia su postura y arranca con determinación.",
            "audio_track": f"'{song_name}' de {artist_name} (iniciando en el punto más potente / beat drop)",
            "voiceover_body": (
                f"Literalmente esta playlist '{playlist_name}' me cambió el humor en tres minutos. "
                f"Es ese empujón que necesitas para terminar lo que empezaste con todo el poder."
            ),
            "call_to_action": f"Toquen el enlace aquí abajo y póngansela en bucle. Me lo agradecen después.",
            "sticker_link": playlist_url,
            "on_screen_text": f"⚡ Reset Mental Activado\nPlaylist: {playlist_name}"
        }

        campaign_payload = {
            "campaign_id": f"camp_{int(datetime.now().timestamp())}",
            "playlist_name": playlist_name,
            "playlist_url": playlist_url,
            "theme": category,
            "created_at": datetime.now().isoformat(),
            "scripts": [script_1, script_2]
        }

        self._record_campaign(campaign_payload)
        return campaign_payload

    def _record_campaign(self, campaign_data: Dict[str, Any]):
        history_path = Path("data/history.json")
        if not history_path.exists():
            history = {"playlists": [], "campaigns": []}
        else:
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = {"playlists": [], "campaigns": []}

        history.setdefault("campaigns", []).append(campaign_data)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
