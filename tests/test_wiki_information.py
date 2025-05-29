import sys
import os
import unittest
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wiki_integration.wiki_information import get_wiki_page, format_html_pages


class TestMatchKeyWords(unittest.TestCase):
    """
    Klasse zum Testen des Abrufs der Minecraft Wiki Seiten als Html und Formatieren
    dieser zu normalem Text als Wiki Kontext
    """

    def test_get_wiki_page(self):
        """
        Testet den Abruf der Rückgabe des Volltext von Minecraft Wiki Seiten von der
        Minecraft Wiki API
        """

        page_title = ["spitzhacke"]
        result = get_wiki_page("https://de.minecraftwiki.net/api.php", page_title)

        print(f"\nSeitentitel: {page_title[0]}")
        print(f"Erwartete Seite: Spitzhacke | Gefundene Seite: {result[0].get_text().strip().split()[0]}")

        self.assertEqual(len(result), 1)
        self.assertTrue(result[0].get_text().startswith("\nSpitzhacke"))


    def test_format_html_pages(self):
        """
        Testet die Formatierung des HTML-Codes, der von der Minecraft Wiki API
        zurückgegeben wird
        """

        test_html = BeautifulSoup("<div><p>Das ist ein Test</p></div>", "html.parser")
        formatted_page = "Das ist ein Test"
        result = format_html_pages([test_html])

        print(f"\Test-HTML: {test_html}")
        print(f"Erwarteter Text: Das ist ein Test | Formatierte HTML: {result}")

        self.assertEqual(len(result), 1)
        self.assertIn(formatted_page, result[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)