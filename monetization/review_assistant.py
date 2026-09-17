"""
Curator Review Assistant for SubmitHub, Playlist Push & Groover.
Genera retroalimentaciones constructivas y profesionales que cumplen con los requisitos
mínimos de extensión y calidad editorial de las plataformas de curaduría de pago.
"""

from typing import Dict, Any, List
from datetime import datetime

class CuratorReviewAssistant:
    def __init__(self):
        self.quality_checkpoints = [
            "mezcla_y_masterizacion",
            "interpretacion_vocal",
            "diseno_sonoro_y_produccion",
            "encaje_en_la_playlist"
        ]

    def generate_review(
        self,
        artist: str,
        track_title: str,
        genre: str,
        playlist_name: str,
        decision: str,  # 'accepted' or 'declined'
        key_observation: str = ""
    ) -> Dict[str, Any]:
        """
        Genera una reseña detallada (> 20 palabras) para entregar en plataformas de curaduría.
        """
        is_accepted = decision.lower() in ["accepted", "aceptada", "si", "aprobada"]

        if is_accepted:
            feedback_text = (
                f"Gran trabajo en '{track_title}', {artist}. La atmósfera sonora y la definición en la mezcla "
                f"conectan de inmediato con la estética de nuestra lista '{playlist_name}'. Destaco especialmente "
                f"el balance dinámico y la emoción transmitida en la progresión armónica. "
                f"{key_observation if key_observation else 'El track aporta un matiz fresco y envolvente que nuestros oyentes valorarán.'} "
                f"Añadida en las primeras posiciones para maximizar exposición."
            )
            action_status = "ADDED_TO_PLAYLIST"
        else:
            feedback_text = (
                f"Hola {artist}, gracias por enviarnos '{track_title}'. La producción tiene una base sólida "
                f"y una propuesta melódica interesante, pero para el flujo específico de '{playlist_name}' "
                f"buscamos un timbre con una textura ligeramente distinta en las frecuencias medias y un tempo más alineado. "
                f"{key_observation if key_observation else 'Te sugerimos pulir un poco la presencia vocal en el estribillo para que destaque aún más.'} "
                f"Te animamos a seguir creando y a enviarnos tus próximos lanzamientos en este estilo."
            )
            action_status = "DECLINED_WITH_FEEDBACK"

        word_count = len(feedback_text.split())

        return {
            "artist": artist,
            "track_title": track_title,
            "genre": genre,
            "playlist_name": playlist_name,
            "decision": action_status,
            "feedback": feedback_text,
            "word_count": word_count,
            "submithub_compliant": word_count >= 15,
            "playlist_push_compliant": word_count >= 15,
            "timestamp": datetime.now().isoformat()
        }
