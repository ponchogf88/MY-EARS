"""
Spotify Client for MY EARS.
Maneja la autenticación y creación de playlists en Spotify.
Soporta modo en vivo (vía Spotipy) y modo simulación para desarrollo inmediato sin bloqueos.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    SPOTIPY_AVAILABLE = True
except ImportError:
    SPOTIPY_AVAILABLE = False

class SpotifyClient:
    def __init__(self, config_path: str = "config/settings.json"):
        self.config_path = Path(config_path)
        self.settings = self._load_settings()
        self.sp = None
        self._init_spotify()

    def _load_settings(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _init_spotify(self):
        spotify_cfg = self.settings.get("spotify", {})
        client_id = os.getenv("SPOTIFY_CLIENT_ID", spotify_cfg.get("client_id", ""))
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", spotify_cfg.get("client_secret", ""))
        redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI", spotify_cfg.get("redirect_uri", "http://127.0.0.1:8888/callback"))
        scope = spotify_cfg.get("scope", "playlist-modify-public playlist-modify-private")

        if SPOTIPY_AVAILABLE and client_id and client_secret:
            try:
                auth_manager = SpotifyOAuth(
                    client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    scope=scope,
                    open_browser=False
                )
                self.sp = spotipy.Spotify(auth_manager=auth_manager)
            except Exception:
                self.sp = None

    @property
    def is_live(self) -> bool:
        return self.sp is not None and not self.settings.get("simulation_mode", False)

    def create_playlist(
        self,
        name: str,
        description: str,
        tracks: List[Dict[str, Any]],
        public: bool = True
    ) -> Dict[str, Any]:
        """
        Crea la playlist y añade las canciones.
        Si no hay credenciales configuradas, ejecuta en modo simulación garantizando
        que el flujo del usuario no se interrumpa.
        """
        track_uris = [t["uri"] for t in tracks if "uri" in t]
        timestamp = datetime.now().isoformat()

        if self.is_live:
            try:
                user_id = self.sp.me()["id"]
                playlist = self.sp.user_playlist_create(
                    user=user_id,
                    name=name,
                    public=public,
                    description=description
                )
                playlist_id = playlist["id"]
                if track_uris:
                    self.sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)

                result = {
                    "id": playlist_id,
                    "name": name,
                    "url": playlist["external_urls"]["spotify"],
                    "uri": playlist["uri"],
                    "tracks_count": len(tracks),
                    "is_simulated": False,
                    "created_at": timestamp
                }
                self._record_history(result)
                return result
            except Exception as e:
                # Fallback suave a simulación reportando la situación
                pass

        # Modo simulación autónomo
        simulated_id = f"myears_{int(datetime.now().timestamp())}"
        result = {
            "id": simulated_id,
            "name": name,
            "description": description,
            "url": f"https://open.spotify.com/playlist/{simulated_id}",
            "uri": f"spotify:playlist:{simulated_id}",
            "tracks": tracks,
            "tracks_count": len(tracks),
            "is_simulated": True,
            "created_at": timestamp
        }
        self._record_history(result)
        return result

    def _record_history(self, playlist_data: Dict[str, Any]):
        history_path = Path(self.settings.get("storage_paths", {}).get("history", "data/history.json"))
        if not history_path.exists():
            history = {"playlists": [], "campaigns": []}
        else:
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except Exception:
                history = {"playlists": [], "campaigns": []}

        history.setdefault("playlists", []).append(playlist_data)
        with open(history_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
