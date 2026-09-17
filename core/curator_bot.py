"""
Spotify Curator Bot Engine.
Implementa el protocolo maestro de 4 reglas para crear playlists virales
diseñadas para tracción en TikTok y monetización en Spotify.
"""

import json
from datetime import datetime
from typing import Dict, Any, List

class SpotifyCuratorBot:
    def __init__(self):
        # Base de datos curada de tracks de alta retención ("Tráilers" y canciones de nicho)
        self.niche_catalogs = {
            "indie_triste": {
                "trailers": [
                    {"title": "Glimpse of Us", "artist": "Joji", "album": "SMITHEREENS"},
                    {"title": "Space Song", "artist": "Beach House", "album": "Depression Cherry"},
                    {"title": "Mystery of Love", "artist": "Sufjan Stevens", "album": "Call Me By Your Name"},
                    {"title": "Apocalypse", "artist": "Cigarettes After Sex", "album": "Cigarettes After Sex"},
                    {"title": "Fourth of July", "artist": "Sufjan Stevens", "album": "Carrie & Lowell"}
                ],
                "deep_cuts_pool": [
                    ("Scott Street", "Phoebe Bridgers"), ("Romantic Homicide", "d4vd"),
                    ("Heather", "Conan Gray"), ("Slow Dancing in a Burning Room", "John Mayer"),
                    ("Roslyn", "Bon Iver, St. Vincent"), ("Holocene", "Bon Iver"),
                    ("Sparks", "Coldplay"), ("Skinny Love", "Bon Iver"),
                    ("I Love You So", "The Walters"), ("Chamber of Reflection", "Mac DeMarco"),
                    ("Freaks", "Surf Curse"), ("Are You Bored Yet?", "Wallows, Clairo"),
                    ("Sofia", "Clairo"), ("Sweater Weather", "The Neighbourhood"),
                    ("Daddy Issues", "The Neighbourhood"), ("Lovers Rock", "TV Girl"),
                    ("Not Allowed", "TV Girl"), ("Francis Forever", "Mitski"),
                    ("First Love / Late Spring", "Mitski"), ("Nobody", "Mitski"),
                    ("Wash.", "Bon Iver"), ("Exile", "Taylor Swift, Bon Iver"),
                    ("Cardigan", "Taylor Swift"), ("All I Want", "Kodaline"),
                    ("Somewhere Only We Know", "Keane"), ("The Night We Met", "Lord Huron"),
                    ("Anchor", "Novo Amor"), ("State Lines", "Novo Amor"),
                    ("Youth", "Daughter"), ("Medicine", "Daughter"),
                    ("Wait", "M83"), ("Transatlanticism", "Death Cab for Cutie"),
                    ("Re: Stacks", "Bon Iver"), ("Lua", "Bright Eyes"),
                    ("First Day of My Life", "Bright Eyes"), ("Cigarette Daydreams", "Cage The Elephant"),
                    ("Telescope", "Cage The Elephant"), ("Liability", "Lorde"),
                    ("Ribs", "Lorde"), ("Supercut", "Lorde"),
                    ("Motion Sickness", "Phoebe Bridgers"), ("Kyoto", "Phoebe Bridgers"),
                    ("Bags", "Clairo"), ("Bubble Gum", "Clairo"),
                    ("Flaming Hot Cheetos", "Clairo")
                ]
            },
            "rap_gimnasio": {
                "trailers": [
                    {"title": "Till I Collapse", "artist": "Eminem, Nate Dogg", "album": "The Eminem Show"},
                    {"title": "Can't C Me", "artist": "2Pac", "album": "All Eyez On Me"},
                    {"title": "Many Men (Wish Death)", "artist": "50 Cent", "album": "Get Rich or Die Tryin'"},
                    {"title": "Stronger", "artist": "Kanye West", "album": "Graduation"},
                    {"title": "HUMBLE.", "artist": "Kendrick Lamar", "album": "DAMN."}
                ],
                "deep_cuts_pool": [
                    ("X Gon' Give It To Ya", "DMX"), ("Ruff Ryders' Anthem", "DMX"),
                    ("Lose Yourself", "Eminem"), ("Venom", "Eminem"),
                    ("Godzilla", "Eminem, Juice WRLD"), ("Power", "Kanye West"),
                    ("Black Skinhead", "Kanye West"), ("DNA.", "Kendrick Lamar"),
                    ("King's Dead", "Jay Rock, Kendrick Lamar, Future"), ("Nonstop", "Drake"),
                    ("Mob Ties", "Drake"), ("SICKO MODE", "Travis Scott"),
                    ("GATTI", "JACKBOYS, Pop Smoke"), ("Dior", "Pop Smoke"),
                    ("Welcome to the Party", "Pop Smoke"), ("Invincible", "Pop Smoke"),
                    ("Praise The Lord (Da Shine)", "A$AP Rocky, Skepta"), ("Lord Pretty Flacko Jodye 2", "A$AP Rocky"),
                    ("Look At Me!", "XXXTENTACION"), ("SAD!", "XXXTENTACION"),
                    ("Moonlight", "XXXTENTACION"), ("Armed and Dangerous", "Juice WRLD"),
                    ("Lean Wit Me", "Juice WRLD"), ("Bank Account", "21 Savage"),
                    ("a lot", "21 Savage"), ("Redrum", "21 Savage"),
                    ("Ric Flair Drip", "Offset, Metro Boomin"), ("Father Stretch My Hands Pt. 1", "Kanye West"),
                    ("Off The Grid", "Kanye West"), ("Carnival", "Kanye West, Ty Dolla $ign"),
                    ("FE!N", "Travis Scott, Playboi Carti"), (" goosebumps", "Travis Scott"),
                    ("HIGHEST IN THE ROOM", "Travis Scott"), ("MAFIA", "Travis Scott"),
                    ("Superhero (Heroes & Villains)", "Metro Boomin, Future, Chris Brown"),
                    ("Creepin'", "Metro Boomin, The Weeknd, 21 Savage"), ("Too Many Nights", "Metro Boomin, Don Toliver"),
                    ("No Role Modelz", "J. Cole"), ("Middle Child", "J. Cole"),
                    ("m y . l i f e", "J. Cole, 21 Savage, Morray"), ("Suicidal Thoughts", "The Notorious B.I.G."),
                    ("Ambitionz Az A Ridah", "2Pac"), ("Hit 'Em Up", "2Pac, Outlawz"),
                    ("Survival of the Fittest", "Mobb Deep"), ("Shook Ones, Pt. II", "Mobb Deep")
                ]
            },
            "coding_nocturno": {
                "trailers": [
                    {"title": "Resonance", "artist": "HOME", "album": "Odyssey"},
                    {"title": "Nightcall", "artist": "Kavinsky", "album": "OutRun"},
                    {"title": "Time", "artist": "Hans Zimmer", "album": "Inception OST"},
                    {"title": "After Dark", "artist": "Mr.Kitty", "album": "Time"},
                    {"title": "Weightless", "artist": "Marconi Union", "album": "Weightless"}
                ],
                "deep_cuts_pool": [
                    ("Sunset Lover", "Petit Biscuit"), ("Intro", "The xx"),
                    ("Teardrop", "Massive Attack"), ("Glory Box", "Portishead"),
                    ("Day One", "Hans Zimmer"), ("Cornfield Chase", "Hans Zimmer"),
                    ("Subdivisions", "Rush"), ("Midnight City", "M83"),
                    ("Starboy", "The Weeknd, Daft Punk"), ("Veridis Quo", "Daft Punk"),
                    ("Giorgio by Moroder", "Daft Punk"), ("Harder, Better, Faster, Stronger", "Daft Punk"),
                    ("Around the World", "Daft Punk"), ("Contact", "Daft Punk"),
                    ("Genesis", "Justice"), ("D.A.N.C.E.", "Justice"),
                    ("Phantom Pt. II", "Justice"), ("Pacific Coast Highway", "Kavinsky"),
                    ("Odd Look", "Kavinsky, The Weeknd"), ("Tech Noir", "Gunship"),
                    ("Fly For Your Life", "Gunship"), ("Dark All Day", "Gunship"),
                    ("Turbo Killer", "Carpenter Brut"), ("Roller Mobster", "Carpenter Brut"),
                    ("Daylight", "Disasterpeace"), ("Compass", "Disasterpeace"),
                    ("Vignette: Panacea", "Disasterpeace"), ("Chamber", "Disasterpeace"),
                    ("Memory Reboot", "VOJ, Narvent"), ("Metamorphosis", "INTERWORLD"),
                    ("Rapture", "INTERWORLD"), ("Sahara", "Hensonn"),
                    ("KERAUNOS", "Playaphonk"), ("Phonky Town", "PlayaPhonk"),
                    ("Override", "KSLV Noh"), ("Disaster", "KSLV Noh"),
                    ("Experience", "Ludovico Einaudi"), ("Nuvole Bianche", "Ludovico Einaudi"),
                    ("Una Mattina", "Ludovico Einaudi"), ("Divenire", "Ludovico Einaudi"),
                    ("Elements", "Ludovico Einaudi"), ("Fly", "Ludovico Einaudi"),
                    ("Near Light", "Ólafur Arnalds"), ("3055", "Ólafur Arnalds"),
                    ("Only the Winds", "Ólafur Arnalds"), ("Brim", "Ólafur Arnalds"),
                    ("Particles", "Ólafur Arnalds, Nanna Bryndís Hilmarsdóttir")
                ]
            }
        }

    def generate_curator_package(self, niche: str, user_emotional_prompt: str = "") -> Dict[str, Any]:
        """
        Ejecuta las 4 reglas del Spotify Curator Bot en una sola operación.
        """
        clean_niche = self._normalize_niche(niche)

        # REGLA 1: Ideación Hiper-Específica (5 Títulos POV + Keywords SEO)
        titles = self._generate_hyper_specific_titles(clean_niche, user_emotional_prompt)
        selected_title = titles[0]

        # REGLA 2: Tracklist de exactamente 50 canciones (5 Tráilers + 45 Deep Cuts)
        tracklist = self._generate_50_tracklist(clean_niche)

        # REGLA 3: Empaque Visual y Metadatos (Prompt DALL-E + Descripción SEO 3 líneas)
        packaging = self._generate_packaging_and_seo(clean_niche, selected_title, tracklist[:5])

        # REGLA 4: Motor de Tráfico TikTok (4 Ganchos POV de 7 segundos)
        tiktok_hooks = self._generate_tiktok_hooks(clean_niche, selected_title)

        return {
            "niche": niche,
            "rule_1_titles": titles,
            "selected_title": selected_title,
            "rule_2_tracklist": {
                "total_count": len(tracklist),
                "trailer_tracks": tracklist[:5],
                "full_tracks": tracklist
            },
            "rule_3_packaging": packaging,
            "rule_4_tiktok_engine": {
                "format": "Grabación de pantalla (7s) de la playlist sonando en Spotify",
                "hooks": tiktok_hooks
            },
            "created_at": datetime.now().isoformat()
        }

    def _normalize_niche(self, niche: str) -> str:
        n = niche.lower()
        if any(w in n for w in ["indie", "triste", "sad", "desamor", "llorar", "nostalgia"]):
            return "indie_triste"
        elif any(w in n for w in ["gym", "gimnasio", "rap", "fuerza", "pesas", "modo guerra"]):
            return "rap_gimnasio"
        else:
            return "coding_nocturno"

    def _generate_hyper_specific_titles(self, niche_key: str, prompt: str) -> List[str]:
        if niche_key == "indie_triste":
            return [
                "we never dated but it still hurt | sad indie songs for situationship grief",
                "POV: you re-read old texts at 3:14 AM and regret existing | sad indie nostalgic",
                "staring at the ceiling feeling like a side character in your own life | melancholy indie folk",
                "screaming lyrics in the passenger seat so nobody hears you crying | crying in the car indie",
                "you were just a lesson and I failed the test | soft sad acoustic heartbreaks"
            ]
        elif niche_key == "rap_gimnasio":
            return [
                "POV: they doubted you and now you're about to lift the whole gym | aggressive gym rap",
                "training until the pain inside becomes pure fuel | dark phonk & hard gym hip hop",
                "POV: heavy PR attempt with zero margin for hesitation | demon workout trap",
                "the villain arc was necessary | rage workout rap motivation 2026",
                "nobody is coming to save you, get up | pure anger gym pump"
            ]
        else:
            return [
                "POV: fixing bugs at 2:47 AM under neon glow while the city sleeps | late night lofi dark synth",
                "entering 4-hour flow state with noise cancelling on 100% | deep work cyberpunk coding",
                "POV: your code compiles on the first try after 6 hours of torment | atmospheric ambient focus",
                "debugging the simulation in dark mode | minimal techno & synthwave for developers",
                "algorithmic hypnosis: high velocity focus beats | dark ambient deep focus"
            ]

    def _generate_50_tracklist(self, niche_key: str) -> List[Dict[str, Any]]:
        catalog = self.niche_catalogs.get(niche_key, self.niche_catalogs["coding_nocturno"])
        trailers = catalog["trailers"]
        deep_cuts = catalog["deep_cuts_pool"]

        tracklist = []

        # Primeras 5 canciones (El Tráiler)
        for i, t in enumerate(trailers, 1):
            tracklist.append({
                "position": i,
                "role": "TRÁILER (Retención Crítica)",
                "title": t["title"],
                "artist": t["artist"],
                "album": t.get("album", "Original Album"),
                "uri": f"spotify:track:{t['title'].lower().replace(' ', '_')}"
            })

        # Canciones 6 a 50 (Nicho Profundo)
        for j, (title, artist) in enumerate(deep_cuts[:45], 6):
            tracklist.append({
                "position": j,
                "role": "Nicho Profundo",
                "title": title,
                "artist": artist,
                "album": "Selected Collection",
                "uri": f"spotify:track:{title.lower().replace(' ', '_')}"
            })

        return tracklist

    def _generate_packaging_and_seo(self, niche_key: str, title: str, trailers: List[Dict[str, Any]]) -> Dict[str, Any]:
        artists = [t["artist"] for t in trailers[:3]]
        artists_str = ", ".join(artists)

        if niche_key == "indie_triste":
            dalle_prompt = (
                "A minimalist cinematic photograph, ultra-high contrast, grainy 35mm film texture. "
                "Close-up portrait of a melancholic face bathed in muted cool blue and amber streetlight. "
                "Intense emotional gaze looking out a rainy car window at night. Stop-the-scroll expression, "
                "vogue editorial style, zero text, no graphic elements, album cover 1:1 aspect ratio."
            )
            desc = (
                f"Para cuando el silencio de la noche pesa más de lo que admites.\n"
                f"Las mejores canciones de sad indie, situationship regrets y bedroom pop melancólico.\n"
                f"Incluye joyas esenciales de {artists_str}. Actualizada semanalmente."
            )
        elif niche_key == "rap_gimnasio":
            dalle_prompt = (
                "Dark brutalist photograph with dramatic chiaroscuro lighting. Extreme close-up of a determined "
                "sweating athlete staring straight into the lens in a dimly lit underground gym. Intense veins, "
                "heavy shadows, hyper-contrasted monochromatic with deep crimson rim light. Raw power and grit, "
                "album cover format 1:1, zero words."
            )
            desc = (
                f"Música para transformar la frustración en repeticiones.\n"
                f"Selección de aggressive gym rap, dark workout phonk y heavy trap para entrenar al fallo.\n"
                f"Con himnos imparables de {artists_str}. Dale guardar y sube el volumen."
            )
        else:
            dalle_prompt = (
                "A sleek dark-mode visual with vibrant neon cyan and deep violet accents. Overhead macro shot "
                "of hands over a backlit mechanical keyboard with a subtle CRT reflection. Cyberpunk minimalist aesthetic, "
                "hyper-clean high contrast, zero clutter, premium album cover aesthetic 1:1, no text."
            )
            desc = (
                f"Tu banda sonora para entrar en hiper-enfoque y programar hasta el amanecer.\n"
                f"Curaduría de late night coding, dark synthwave, atmospheric ambient y deep focus beats.\n"
                f"Con pistas maestras de {artists_str}. Ideal para programadores y diseñadores."
            )

        return {
            "dalle_prompt": dalle_prompt,
            "spotify_description_3_lines": desc,
            "featured_artists": artists
        }

    def _generate_tiktok_hooks(self, niche_key: str, title: str) -> List[Dict[str, str]]:
        if niche_key == "indie_triste":
            return [
                {
                    "hook_number": 1,
                    "overlay_text": "POV: estás romantizando al que dejaste ir... otra vez.",
                    "audio_suggestion": "Track #1 (Joji - Glimpse of Us) en el puente vocal",
                    "target_emotion": "Nostalgia universal e incomodidad emocional"
                },
                {
                    "hook_number": 2,
                    "overlay_text": "Si tu situationship no te escribe hoy, pon esta playlist en bucle.",
                    "audio_suggestion": "Track #2 (Beach House - Space Song) en el intro de sintetizador",
                    "target_emotion": "Validación de duelo no correspondido"
                },
                {
                    "hook_number": 3,
                    "overlay_text": "Canciones que duelen como si todavía hablaran todos los días.",
                    "audio_suggestion": "Track #4 (Cigarettes After Sex - Apocalypse)",
                    "target_emotion": "Melancolía íntima"
                },
                {
                    "hook_number": 4,
                    "overlay_text": "Guardé esta playlist porque nadie me dijo que el desapego se sentía así.",
                    "audio_suggestion": "Track #3 (Sufjan Stevens - Mystery of Love)",
                    "target_emotion": "Conexión empática instantánea"
                }
            ]
        elif niche_key == "rap_gimnasio":
            return [
                {
                    "hook_number": 1,
                    "overlay_text": "POV: te dijeron que no podías y hoy vas a romper tu récord personal.",
                    "audio_suggestion": "Track #1 (Eminem - Till I Collapse) segundo 0:05",
                    "target_emotion": "Rabia canalizada en disciplina"
                },
                {
                    "hook_number": 2,
                    "overlay_text": "La playlist que necesitas cuando entras al gym con el corazón roto.",
                    "audio_suggestion": "Track #3 (50 Cent - Many Men)",
                    "target_emotion": "Villain Arc activado"
                },
                {
                    "hook_number": 3,
                    "overlay_text": "3 canciones de esta lista y se te quita cualquier excusa.",
                    "audio_suggestion": "Track #4 (Kanye West - Stronger)",
                    "target_emotion": "Disparo de adrenalina"
                },
                {
                    "hook_number": 4,
                    "overlay_text": "Si tus audífonos no están a todo volumen con esto, no estás entrenando de verdad.",
                    "audio_suggestion": "Track #5 (Kendrick Lamar - HUMBLE.)",
                    "target_emotion": "Poder e intensidad"
                }
            ]
        else:
            return [
                {
                    "hook_number": 1,
                    "overlay_text": "POV: son las 2:30 AM, tus errores se solucionaron y el código corre limpio.",
                    "audio_suggestion": "Track #1 (HOME - Resonance)",
                    "target_emotion": "Alivio y dopamina técnica"
                },
                {
                    "hook_number": 2,
                    "overlay_text": "Ponle play a esto, apaga las luces y entra en deep work por 4 horas seguidas.",
                    "audio_suggestion": "Track #2 (Kavinsky - Nightcall)",
                    "target_emotion": "Inmersión y concentración absoluta"
                },
                {
                    "hook_number": 3,
                    "overlay_text": "La única razón por la que entrego mis proyectos a tiempo sin volverme loco.",
                    "audio_suggestion": "Track #3 (Hans Zimmer - Time)",
                    "target_emotion": "Épica de productividad"
                },
                {
                    "hook_number": 4,
                    "overlay_text": "Tu cerebro cuando finalmente encuentras el punto y coma que faltaba.",
                    "audio_suggestion": "Track #4 (Mr.Kitty - After Dark)",
                    "target_emotion": "Complicidad de comunidad dev"
                }
            ]
