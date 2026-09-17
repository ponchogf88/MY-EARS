"""
Mood Engine for MY EARS.
Analiza la narración del usuario, extrae la esencia emocional y la mapea
contra el banco de palabras clave y arquetipos de sonido.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List

class MoodEngine:
    def __init__(self, config_path: str = "config/soul_keywords.json"):
        self.config_path = Path(config_path)
        self.soul_config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def analyze_experience(self, text: str) -> Dict[str, Any]:
        """
        Analiza el texto de la experiencia diaria y determina la categoría
        de esencia más afín, palabras clave y parámetros de audio.
        """
        normalized_text = text.lower()
        words = set(re.findall(r'\b\w+\b', normalized_text))

        categories = self.soul_config.get("soul_categories", {})
        scores = {}

        for cat_key, cat_data in categories.items():
            score = 0
            keywords = cat_data.get("keywords", [])
            for kw in keywords:
                if kw in normalized_text:
                    score += 3
            # Bonus por sinónimos y temática
            for tag in cat_data.get("default_tags", []):
                tag_words = tag.lower().split()
                if any(tw in words for tw in tag_words):
                    score += 1
            scores[cat_key] = score

        # Si no hay match explícito, deducir según palabras de valencia y energía
        best_category = max(scores, key=scores.get) if any(scores.values()) else "introspeccion_profunda"
        cat_info = categories.get(best_category, {})

        matched_keywords = [
            kw for kw in cat_info.get("keywords", [])
            if kw in normalized_text
        ]
        if not matched_keywords:
            matched_keywords = [cat_info.get("keywords", ["esencia"])[0]]

        # Extraer concepto resumido
        summary_concept = self._extract_concept(text, matched_keywords[0])

        return {
            "category_key": best_category,
            "matched_keywords": matched_keywords,
            "primary_keyword": matched_keywords[0],
            "concept": summary_concept,
            "spotify_criteria": cat_info.get("spotify_criteria", {}),
            "default_tags": cat_info.get("default_tags", []),
            "raw_experience": text
        }

    def _extract_concept(self, text: str, fallback: str) -> str:
        sentences = [s.strip() for s in re.split(r'[.,;!\n]+', text) if s.strip()]
        if sentences:
            # Tomar las primeras 3 a 5 palabras de la primera oración relevante
            words = sentences[0].split()
            concept = " ".join(words[:5]).capitalize()
            return concept
        return fallback.capitalize()
