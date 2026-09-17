"""
Notion & Make.com Integration Module for MY EARS.
Estructura datos para la base de datos 'Spotify Hustle' en Notion y genera payloads para Make.com.
"""

import csv
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

class NotionHustleSync:
    def __init__(self, export_dir: str = "data/notion_exports"):
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def prepare_notion_entry(self, package: Dict[str, Any], followers: int = 0, spotify_url: str = "") -> Dict[str, Any]:
        """
        Formatea el paquete del Curator Bot bajo el esquema exacto de Notion 'Spotify Hustle'.
        Campos: Nombre de Playlist, Status, Creada en Spotify, Seguidores, Ganchos de TikTok generados, Link SubmitHub.
        """
        title = package.get("selected_title", "Playlist Sin Título")
        hooks = package.get("rule_4_tiktok_engine", {}).get("hooks", [])
        hooks_text = " | ".join([f"H{h['hook_number']}: {h['overlay_text']}" for h in hooks])

        return {
            "Nombre de Playlist": title,
            "Status": "Activa" if spotify_url else "Borrador",
            "Creada en Spotify": bool(spotify_url),
            "Seguidores": followers,
            "Ganchos de TikTok generados": hooks_text,
            "Link SubmitHub": "https://www.submithub.com/curator/my-ears",
            "Link Playlist Spotify": spotify_url,
            "Fecha Creación": datetime.now().strftime("%Y-%m-%d")
        }

    def export_to_notion_csv(self, entries: List[Dict[str, Any]], filename: str = "notion_spotify_hustle.csv") -> str:
        """
        Genera un CSV listo para importar directamente con 1-click a Notion.
        """
        file_path = self.export_dir / filename
        headers = [
            "Nombre de Playlist",
            "Status",
            "Creada en Spotify",
            "Seguidores",
            "Ganchos de TikTok generados",
            "Link SubmitHub",
            "Link Playlist Spotify",
            "Fecha Creación"
        ]

        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for entry in entries:
                writer.writerow(entry)

        return str(file_path)

    def build_make_webhook_payload(self, package: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea el payload JSON listo para ser consumido por un webhook de Make.com o n8n.
        """
        return {
            "event": "playlist_created",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "playlist_title": package.get("selected_title"),
                "niche": package.get("niche"),
                "dalle_prompt": package.get("rule_3_packaging", {}).get("dalle_prompt"),
                "description": package.get("rule_3_packaging", {}).get("spotify_description_3_lines"),
                "tiktok_hooks": package.get("rule_4_tiktok_engine", {}).get("hooks", []),
                "trailers": package.get("rule_2_tracklist", {}).get("trailer_tracks", [])
            }
        }
