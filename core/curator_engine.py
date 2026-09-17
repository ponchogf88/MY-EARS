"""
Curator Engine for MY EARS.
Genera la lista curada de canciones según los parámetros acústicos y emocionales del estado de ánimo.
"""

from typing import Dict, Any, List

# Banco curado de referencia por categoría sonora
CURATED_SEED_TRACKS = {
    "introspeccion_profunda": [
        {"title": "Weightless", "artist": "Marconi Union", "album": "Weightless", "uri": "spotify:track:6kkwzB6hXLsqZnrvUhPtGL"},
        {"title": "Day One", "artist": "Hans Zimmer", "album": "Interstellar OST", "uri": "spotify:track:45WgZ1UfV9YlFzXG3dJv1N"},
        {"title": "Holocene", "artist": "Bon Iver", "album": "Bon Iver", "uri": "spotify:track:4fbvXwMTXPWaFyaMWUm9CR"},
        {"title": "Near Light", "artist": "Ólafur Arnalds", "album": "Living Room Songs", "uri": "spotify:track:03s9hG5qQyFhJ5nZJqf7oY"},
        {"title": "Mystery of Love", "artist": "Sufjan Stevens", "album": "Call Me By Your Name", "uri": "spotify:track:5GbVzc6vSiiX19V0R7f6nk"},
        {"title": "Intro", "artist": "The xx", "album": "xx", "uri": "spotify:track:2usrT8QIbIk9y0NEtqwzHX"},
        {"title": "Experience", "artist": "Ludovico Einaudi", "album": "In a Time Lapse", "uri": "spotify:track:1BncfTToHYwxyOxCII7gvV"},
        {"title": "Gymnopédie No. 1", "artist": "Erik Satie", "album": "Essential Classics", "uri": "spotify:track:5NGtFXVpXSvwunEIGeviY3"},
        {"title": "Sparks", "artist": "Coldplay", "album": "Parachutes", "uri": "spotify:track:7D0RhFdoQVJRluNavbACJW"},
        {"title": "Dawn", "artist": "Dario Marianelli, Jean-Yves Thibaudet", "album": "Pride & Prejudice", "uri": "spotify:track:225xv97r095F29ufDqK9v7"}
    ],
    "resiliencia_y_poder": [
        {"title": "Time", "artist": "Hans Zimmer", "album": "Inception OST", "uri": "spotify:track:6ZFbIcPtQ91dnVoN8visQm"},
        {"title": "Midnight City", "artist": "M83", "album": "Hurry Up, We're Dreaming", "uri": "spotify:track:6GyFP1nfCDB87D2YRI0ilQ"},
        {"title": "Can't Stop", "artist": "Red Hot Chili Peppers", "album": "By The Way", "uri": "spotify:track:3ZOEytgrvLQIaoaqbgbbBt"},
        {"title": "Till I Collapse", "artist": "Eminem, Nate Dogg", "album": "The Eminem Show", "uri": "spotify:track:4xkOaSrkGQIO9ezTId0WJH"},
        {"title": "Run Boy Run", "artist": "Woodkid", "album": "The Golden Age", "uri": "spotify:track:0vdFrpUeR2mS4eZf6lX9Y7"},
        {"title": "Sail", "artist": "AWOLNATION", "album": "Megalithic Symphony", "uri": "spotify:track:7wGoVu4DEXVFDhu0BpBs2e"},
        {"title": "Radioactive", "artist": "Imagine Dragons", "album": "Night Visions", "uri": "spotify:track:62yJjFSm2qEGNTUKGrO7FF"},
        {"title": "Way Down We Go", "artist": "KALEO", "album": "A/B", "uri": "spotify:track:0y1QJc3BYVIxwTNnzZl42i"},
        {"title": "Stronger", "artist": "Kanye West", "album": "Graduation", "uri": "spotify:track:4fzsfWzRhPawzqhXZdoIyR"},
        {"title": "Strobe", "artist": "deadmau5", "album": "For Lack of a Better Name", "uri": "spotify:track:7H6on28d95Lz8D9h516Hn1"}
    ],
    "vibracion_alta_y_gozo": [
        {"title": "Electric Feel", "artist": "MGMT", "album": "Oracular Spectacular", "uri": "spotify:track:3FtYbEfBqAlGOJuUQlmVcR"},
        {"title": "September", "artist": "Earth, Wind & Fire", "album": "The Best of Earth, Wind & Fire", "uri": "spotify:track:2grjqo0Frpf25YIBToq3j9"},
        {"title": "Sunroof", "artist": "Nicky Youre, dazy", "album": "Sunroof", "uri": "spotify:track:27NovFLESLGrdBPqTHuXYC"},
        {"title": "Get Lucky", "artist": "Daft Punk, Pharrell Williams", "album": "Random Access Memories", "uri": "spotify:track:696DnlkuDOXcMBp6xm7bk3"},
        {"title": "Feel So Close", "artist": "Calvin Harris", "album": "18 Months", "uri": "spotify:track:1gihuJRmrnqKeTu34WzKiL"},
        {"title": "Safe and Sound", "artist": "Capital Cities", "album": "In A Tidal Wave Of Mystery", "uri": "spotify:track:6Z8R6UsFuE25jVqE3R8jWb"},
        {"title": "Tongue Tied", "artist": "GROUPLOVE", "album": "Never Trust a Happy Song", "uri": "spotify:track:0GO8y0TnC3uVqa9vU1tB0n"},
        {"title": "Levitating", "artist": "Dua Lipa", "album": "Future Nostalgia", "uri": "spotify:track:463CkQjx2Zk1yXoBuEVdQI"},
        {"title": "Watermelon Sugar", "artist": "Harry Styles", "album": "Fine Line", "uri": "spotify:track:6UelLqGlWMcVH1E5c4H7lY"},
        {"title": "Sunday Best", "artist": "Surfaces", "album": "Where the Light Is", "uri": "spotify:track:1q8RA5G6L4U07Wj3W2iQe9"}
    ],
    "nocturno_y_misterio": [
        {"title": "Nightcall", "artist": "Kavinsky", "album": "OutRun", "uri": "spotify:track:0U0ldCRmgCqhVv66ksj623"},
        {"title": "After Dark", "artist": "Mr.Kitty", "album": "Time", "uri": "spotify:track:2LKOHdO01qJ8rG2sE6oY4Q"},
        {"title": "Teardrop", "artist": "Massive Attack", "album": "Mezzanine", "uri": "spotify:track:67Hna13dND5ZvBpTXRIaOJ"},
        {"title": "Glory Box", "artist": "Portishead", "album": "Dummy", "uri": "spotify:track:353F57B96eP8k8XqL11hGq"},
        {"title": "Resonance", "artist": "HOME", "album": "Odyssey", "uri": "spotify:track:1TuopWDI4GQJ1v128k01pE"},
        {"title": "Starboy", "artist": "The Weeknd, Daft Punk", "album": "Starboy", "uri": "spotify:track:7MXVkk9YM5IZxh0WOSnek9"},
        {"title": "In the Air Tonight", "artist": "Phil Collins", "album": "Face Value", "uri": "spotify:track:18AXbzPzBS8Y3AkgSxzJPb"},
        {"title": "Subdivisions", "artist": "Rush", "album": "Signals", "uri": "spotify:track:12bEaRj51E5jRjY81kG9xY"},
        {"title": "Sunset Lover", "artist": "Petit Biscuit", "album": "Presence", "uri": "spotify:track:3WRQUvzRvBDr4AxMWhXc57"},
        {"title": "Drive", "artist": "The Cars", "album": "Heartbeat City", "uri": "spotify:track:2P9yvdqZl84rJp8i6m7e7Z"}
    ],
    "fluir_y_desconexion": [
        {"title": "Aguas de Março", "artist": "Stan Getz, João Gilberto", "album": "Getz/Gilberto", "uri": "spotify:track:13v0Xq27YJv6Jb2k9aP421"},
        {"title": "So What", "artist": "Miles Davis", "album": "Kind of Blue", "uri": "spotify:track:0qDs727Yj9VqJb6k6kP7yE"},
        {"title": "Space Song", "artist": "Beach House", "album": "Depression Cherry", "uri": "spotify:track:7Gd0vdqaYYnN969vN4kY3U"},
        {"title": "Breathe", "artist": "Telepopmusik", "album": "Genetic World", "uri": "spotify:track:0391XF07Z9v8h6L8k4J39x"},
        {"title": "Porcelain", "artist": "Moby", "album": "Play", "uri": "spotify:track:1hEh8Hc9kWG0q7VvQkL3bM"},
        {"title": "Sunset", "artist": "The xx", "album": "Coexist", "uri": "spotify:track:4jF91q8y9Jk0L10m8fJ8p0"},
        {"title": "Weightless Pt. 2", "artist": "Marconi Union", "album": "Weightless (Ambient)", "uri": "spotify:track:591Xk9b9vL02l87K7jVv8R"},
        {"title": "Clair de Lune", "artist": "Claude Debussy, Martin Jones", "album": "Debussy Piano Works", "uri": "spotify:track:6N7gPd9ISnBKLm0FmMRZeF"},
        {"title": "Slow Dancing in a Burning Room", "artist": "John Mayer", "album": "Continuum", "uri": "spotify:track:2jdAk8ATUrVUcuSvFRx0V4"},
        {"title": "Dreams", "artist": "Fleetwood Mac", "album": "Rumours", "uri": "spotify:track:0ofHAoxe9vBkTCp2UQIavz"}
    ]
}

class CuratorEngine:
    def __init__(self):
        self.seeds = CURATED_SEED_TRACKS

    def curate_playlist(self, mood_data: Dict[str, Any], count: int = 10) -> List[Dict[str, Any]]:
        """
        Selecciona las mejores canciones para el estado de ánimo específico.
        """
        cat_key = mood_data.get("category_key", "introspeccion_profunda")
        available_tracks = self.seeds.get(cat_key, self.seeds["introspeccion_profunda"])

        # Seleccionar hasta 'count' canciones
        selected = available_tracks[:count]
        return selected
