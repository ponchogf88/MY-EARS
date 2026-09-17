"""
Unit tests for Curator Bot, Review Assistant and Notion Sync.
"""

import unittest
from core.curator_bot import SpotifyCuratorBot
from monetization.review_assistant import CuratorReviewAssistant
from integrations.notion_sync import NotionHustleSync

class TestCuratorBotSuite(unittest.TestCase):
    def test_curator_bot_4_rules(self):
        bot = SpotifyCuratorBot()
        pkg = bot.generate_curator_package("indie_triste")

        # Regla 1: 5 títulos
        self.assertEqual(len(pkg["rule_1_titles"]), 5)
        self.assertIn("we never dated", pkg["selected_title"])

        # Regla 2: 50 tracks con 5 trailers
        self.assertEqual(len(pkg["rule_2_tracklist"]["full_tracks"]), 50)
        self.assertEqual(len(pkg["rule_2_tracklist"]["trailer_tracks"]), 5)

        # Regla 3: DALL-E prompt y 3 líneas de descripción
        self.assertIn("dalle_prompt", pkg["rule_3_packaging"])
        self.assertIn("spotify_description_3_lines", pkg["rule_3_packaging"])

        # Regla 4: 4 ganchos de TikTok de 7 segundos
        self.assertEqual(len(pkg["rule_4_tiktok_engine"]["hooks"]), 4)

    def test_review_assistant_compliance(self):
        assistant = CuratorReviewAssistant()
        rev = assistant.generate_review(
            artist="Luna",
            track_title="Nocturno",
            genre="Indie",
            playlist_name="MY EARS // INDIE",
            decision="accepted"
        )
        self.assertTrue(rev["submithub_compliant"])
        self.assertTrue(rev["word_count"] >= 15)

    def test_notion_sync_export(self):
        sync = NotionHustleSync()
        bot = SpotifyCuratorBot()
        pkg = bot.generate_curator_package("rap_gimnasio")
        entry = sync.prepare_notion_entry(pkg, followers=250, spotify_url="https://open.spotify.com/playlist/test")
        self.assertEqual(entry["Status"], "Activa")
        self.assertEqual(entry["Seguidores"], 250)

        csv_file = sync.export_to_notion_csv([entry], filename="test_export.csv")
        self.assertTrue(csv_file.endswith(".csv"))

if __name__ == "__main__":
    unittest.main()
