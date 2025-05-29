import sys
import os
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wiki_integration.key_words_matching import match_key_words


class TestMatchKeyWords(unittest.TestCase):
    """
    Klasse zum Testen des Matching der Schlüsselwörter aus den Nutzerfragen mit
    den Seitentiteln aus dem Matching Dictionary
    """

    def setUp(self):
        """
        Erstellt ein Test-Dictionary mit einem Auszug des Matching Dictionary
        für die Minecraft Wiki Seiten Diamant und Handwerk
        """

        self.matching_dict = {
            "diamant": {
                "redirects": [
                    "diamant (edelstein)",
                    "diamond (gem)",
                    "diamond",
                    "dia"
                ],
                "url": "https://minecraft.fandom.com/de/wiki/Diamant"
            },
            "handwerk": {
                "redirects": [
                    "basteln",
                    "craften",
                    "craftingrezepte",
                    "rezeptebuch",
                    "herstellen",
                    "rezept-buch",
                    "herstellung",
                    "crafting",
                    "craft"
                ],
                "url": "https://minecraft.fandom.com/de/wiki/Handwerk"
            }
        }

    def test_exact_match(self):
        """
        Testet das exakte Matching von Schlüsselwörtern Diamant mit den
        Minecraft Wiki Seiten
        """

        key_words = ["diamant"]
        result = match_key_words(self.matching_dict, key_words)

        print(f"\nKey Words: {key_words}")
        print(f"Erwartet: diamant | Gefunden: {result}")

        self.assertIn("diamant", result)
        self.assertNotIn("handwerk", result)


    def test_redirect_match(self):
        """
        Testet das Matching eines Schlüsselworts mit den Redirects auf die
        Minecraft Wiki Seiten
        """

        key_words = ["craften"]
        result = match_key_words(self.matching_dict, key_words)

        print(f"\nKey Words: {key_words}")
        print(f"Erwartet: handwerk | Gefunden: {result}")

        self.assertIn("handwerk", result)
        self.assertNotIn("diamant", result)


    def test_levenshtein_match(self):
        """
        Testet das Matching von Schlüsselwörtern mit Rechtschreibfehlern und
        das Matching von ähnlichen Wörtern mit anderem Kontext, wobei die
        Levenshtein-Distanz von match_key_words 1 beträgt
        """
        
        key_words = ["diamnt", "draht"]  # "draht" soll nicht mit Redirect "craft" gematched werden
        result = match_key_words(self.matching_dict, key_words)

        print(f"\nKey Words: {key_words}")
        print(f"Erwartet: diamant | Gefunden: {result}")

        self.assertIn("diamant", result)
        self.assertNotIn("handwerk", result)


    def test_no_match(self):
        """
        Testet, dass bei nicht vorhandenen Wörtern bzw. zu vielen Schreibfehlern
        kein Match zustande kommt
        """

        key_words = ["dimnt", "kuchen"]
        result = match_key_words(self.matching_dict, key_words)

        print(f"\nKey Words: {key_words}")
        print(f"Erwartet: diamant | Gefunden: {result}")

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)