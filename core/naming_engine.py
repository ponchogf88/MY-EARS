"""
Naming Engine for MY EARS.
Genera títulos y descripciones repetitivas bajo las fórmulas de identidad de la marca.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class NamingEngine:
    def __init__(self, config_path: str = "config/soul_keywords.json"):
        self.config_path = Path(config_path)
        self.soul_config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def generate_titles(self, mood_data: Dict[str, Any], volume: int = 1) -> List[str]:
        """
        Genera múltiples variantes de títulos usando las fórmulas maestras.
        """
        patterns = self.soul_config.get("soul_patterns", [
            "MY EARS // {keyword_upper} — {concept}",
            "{keyword_title} & {essence_title} // Vol. {volume}",
            "FRECUENCIA {keyword_upper} :: {mood}"
        ])

        keyword = mood_data.get("primary_keyword", "esencia")
        concept = mood_data.get("concept", "Vibración")
        category_name = mood_data.get("category_key", "").replace("_", " ").title()
        tags = mood_data.get("default_tags", ["Esencia"])
        essence_tag = tags[0].title() if tags else "Esencia"

        date_str = datetime.now().strftime("%d.%m")

        results = []
        for pat in patterns:
            title = pat.format(
                keyword_upper=keyword.upper(),
                keyword_title=keyword.title(),
                essence_title=essence_tag,
                concept=concept,
                volume=f"{volume:02d}",
                mood=category_name,
                context=concept,
                date=date_str
            )
            results.append(title)

        return results

    def generate_description(self, mood_data: Dict[str, Any], title: str) -> str:
        """
        Genera la descripción para la playlist en Spotify con enfoque de conexión sensorial.
        """
        keyword = mood_data.get("primary_keyword", "esencia")
        category = mood_data.get("category_key", "").replace("_", " ")
        experience = mood_data.get("raw_experience", "")

        desc = (
            f"Curaduría oficial MY EARS. Capturando momentos de {category} y la vibración de '{keyword}'. "
            f"Banda sonora diseñada para transformar el estado mental y acompañar tus pasos. "
            f"Sincroniza tus oídos."
        )
        return desc
