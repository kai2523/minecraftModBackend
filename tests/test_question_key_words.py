"""
test_question_key_words.py

Modul zum Testen von POS-Tagging, Lemmatisierung und Compound-Splitting.
"""

import unittest
import spacy
from wiki_integration.question_key_words import extract_keywords_pos_lemma_ner, holmes_style_compound_split

# Lade das deutsche Sprachmodell von spaCy
nlp = spacy.load("de_core_news_sm")

# Beispielhafte Wortliste für das Compound-Splitting
mock_wordlist = {
    "diamant", "schwert", "nether", "festung", "redstone", "maschine", "bauen", "finden", "minecraft"
}

#Testklasse mit einzelnen Testfällen 
class TestQuestionKeywords(unittest.TestCase):

    def test_pos_and_lemma(self):
        # Testet, ob relevante Wörter per POS-Tagging und Lemmatisierung korrekt erkannt werden
        text = "Wie kann ich ein Diamantschwert bauen?"
        expected = {"bauen", "Diamantschwert"}
        result = set(extract_keywords_pos_lemma_ner(text))
        print(f"\n[POS+Lemma] Text: {text}")
        print(f"Erwartet: {expected} | Gefunden: {result}")
        self.assertTrue(expected.issubset(result))

        def test_named_entity(self):
            # Testet, ob Named Entities korrekt extrahiert werden
            text = "Wo finde ich eine Netherfestung?"
            expected = {"finden", "Netherfestung"}
            result = set(extract_keywords_pos_lemma_ner(text))
            print(f"\n[NER] Text: {text}")
            print(f"Erwartet: {expected} | Gefunden: {result}")
            self.assertTrue(expected.issubset(result))

    def test_lemmatization(self):
        # Testet, ob Verbformen korrekt auf ihr Lemma reduziert werden
        text = "Wie finde ich Redstonemaschinen?"
        result = set(extract_keywords_pos_lemma_ner(text))
        print(f"\n[Lemma] Text: {text}")
        print(f"Gefunden: {result}")
        self.assertIn("finden", result)

    def test_compound_split_success(self):
        # Testet die erfolgreiche Zerlegung eines zusammengesetzten Wortes
        word = "Diamantschwert"
        expected_split = {"diamant", "schwert"}
        splits = holmes_style_compound_split(word, mock_wordlist)
        found = [set(s) for s in splits]
        print(f"\n[Compound Split Erfolg] Wort: {word}")
        print(f"Erwartet: {expected_split} | Gefunden: {splits}")
        self.assertIn(expected_split, found)

    def test_compound_split_failure(self):
        # Testet Verhalten bei nicht zerlegbarem Wort
        word = "Zombiediamantfestungsschwert"
        splits = holmes_style_compound_split(word, mock_wordlist)
        print(f"\n[Compound Split Fehlschlag] Wort: {word}")
        print(f"Gefunden: {splits}")
        self.assertEqual(splits[0][0], word.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
