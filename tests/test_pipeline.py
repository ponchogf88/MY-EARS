"""
Unit Tests for MY EARS System.
"""

import unittest
from core.mood_engine import MoodEngine
from core.naming_engine import NamingEngine
from core.curator_engine import CuratorEngine
from core.spotify_client import SpotifyClient
from campaign.influencer_engine import InfluencerEngine
from core.pipeline import MyEarsPipeline

class TestMyEarsSuite(unittest.TestCase):
    def setUp(self):
        self.pipeline = MyEarsPipeline()

    def test_mood_engine(self):
        engine = MoodEngine()
        result = engine.analyze_experience("Hoy busqué calma y silencio en el bosque para encontrar claridad")
        self.assertEqual(result["category_key"], "introspeccion_profunda")
        self.assertIn("claridad", result["matched_keywords"])

    def test_naming_engine(self):
        engine = NamingEngine()
        mood_data = {
            "primary_keyword": "claridad",
            "concept": "Caminata matutina",
            "category_key": "introspeccion_profunda",
            "default_tags": ["calma reflexiva"]
        }
        titles = engine.generate_titles(mood_data, volume=1)
        self.assertTrue(len(titles) > 0)
        self.assertIn("CLARIDAD", titles[0])

    def test_curator_engine(self):
        curator = CuratorEngine()
        tracks = curator.curate_playlist({"category_key": "resiliencia_y_poder"}, count=5)
        self.assertEqual(len(tracks), 5)
        self.assertIn("title", tracks[0])

    def test_influencer_engine(self):
        inf_engine = InfluencerEngine()
        campaign = inf_engine.generate_campaign(
            playlist_name="MY EARS // CLARIDAD",
            playlist_url="https://open.spotify.com/playlist/test",
            mood_data={"primary_keyword": "claridad", "category_key": "introspeccion_profunda"},
            featured_track={"title": "Weightless", "artist": "Marconi Union"}
        )
        self.assertEqual(len(campaign["scripts"]), 2)
        self.assertTrue(len(campaign["scripts"][0]["hook_0_to_3s"]) > 0)

    def test_pipeline_end_to_end(self):
        res = self.pipeline.process_experience(
            "Día de máxima energía y fuego, rompiendo marcas en el entrenamiento.",
            volume=3
        )
        self.assertEqual(res["status"], "success")
        self.assertTrue(len(res["tracks"]) > 0)
        self.assertIn("url", res["playlist"])
        self.assertEqual(len(res["campaign"]["scripts"]), 2)

if __name__ == "__main__":
    unittest.main()
