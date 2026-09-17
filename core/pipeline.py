"""
Pipeline Orquestador de MY EARS.
Integra de extremo a extremo:
1. Captura de idea en el Banco de Ideas.
2. Análisis emocional y extracción de esencia.
3. Generación de títulos con patrones de identidad.
4. Curaduría de canciones.
5. Creación / Subida a Spotify.
6. Disparo de campaña con guiones para los 2 creadores.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

from core.mood_engine import MoodEngine
from core.naming_engine import NamingEngine
from core.curator_engine import CuratorEngine
from core.spotify_client import SpotifyClient
from campaign.influencer_engine import InfluencerEngine

class MyEarsPipeline:
    def __init__(self):
        self.mood_engine = MoodEngine()
        self.naming_engine = NamingEngine()
        self.curator_engine = CuratorEngine()
        self.spotify_client = SpotifyClient()
        self.campaign_engine = InfluencerEngine()

    def process_experience(self, experience_text: str, volume: int = 1, auto_publish: bool = True) -> Dict[str, Any]:
        """
        Ejecuta el ciclo autónomo completo a partir de una vivencia o pensamiento.
        """
        # 1. Registro automático en el Banco de Ideas (Descarga libre)
        self._record_idea(experience_text)

        # 2. Análisis del estado de ánimo
        mood_data = self.mood_engine.analyze_experience(experience_text)

        # 3. Generación de títulos y descripción
        titles = self.naming_engine.generate_titles(mood_data, volume=volume)
        selected_title = titles[0]
        description = self.naming_engine.generate_description(mood_data, selected_title)

        # 4. Curaduría musical
        curated_tracks = self.curator_engine.curate_playlist(mood_data, count=10)
        featured_track = curated_tracks[0] if curated_tracks else {"title": "Track", "artist": "Artista"}

        # 5. Creación y subida a Spotify
        playlist_result = {}
        if auto_publish:
            playlist_result = self.spotify_client.create_playlist(
                name=selected_title,
                description=description,
                tracks=curated_tracks,
                public=True
            )

        playlist_url = playlist_result.get("url", f"https://open.spotify.com/playlist/{selected_title.replace(' ', '_')}")

        # 6. Disparo de campaña para los 2 creadores
        campaign_result = self.campaign_engine.generate_campaign(
            playlist_name=selected_title,
            playlist_url=playlist_url,
            mood_data=mood_data,
            featured_track=featured_track
        )

        return {
            "status": "success",
            "experience": experience_text,
            "mood_analysis": mood_data,
            "titles_generated": titles,
            "selected_title": selected_title,
            "description": description,
            "tracks": curated_tracks,
            "playlist": playlist_result,
            "campaign": campaign_result
        }

    def _record_idea(self, text: str):
        ideas_path = Path("data/ideas_bank.json")
        try:
            if ideas_path.exists():
                with open(ideas_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                data = {"ideas": [], "last_updated": ""}
            
            data.setdefault("ideas", []).append({
                "text": text,
                "timestamp": datetime.now().isoformat()
            })
            data["last_updated"] = datetime.now().isoformat()

            with open(ideas_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
