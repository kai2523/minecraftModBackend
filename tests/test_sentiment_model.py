# test_sentiment_analysis.py

"""
Modul zum Testen der Sentiment-Analyse-Pipeline.
"""

import sys
import os
import unittest

# Projektpfad hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentiment_analysis import init_sentiment_pipeline, analyze_sentiment

class TestSentimentAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Sentiment Model initialisieren und valide Labels definieren
        cls.pipeline = init_sentiment_pipeline("tinybert-german-finetuned")
        cls.allowed_labels = {"freundlich", "neutral", "unfreundlich"}

    def test_valid_label(self):
        # Testet obe das Model ein valides Label liefert
        sentence = "Das ist ein völlig beliebiger Satz."
        label, score, prompt = analyze_sentiment(self.pipeline, sentence)
        print(f"\n[Test valides Label]\nVorhergesagtes Label: {label}")
        self.assertIn(label.lower(), self.allowed_labels, msg=f"Label '{label}' nicht in {self.allowed_labels}")

    def test_friendly_sentence(self):
        # Testet einen freundlichen Satz
        sentence = "Danke für deine tolle Hilfe!"
        expected = "freundlich"
        label, score, prompt = analyze_sentiment(self.pipeline, sentence)
        print(f"\n[Test Freundlich]\nSatz: '{sentence}'")
        print(f"Erwartet: {expected},\nVorhergesagt: {label} ({score*100:.1f}%)")
        self.assertEqual(label.lower(), expected, msg=f"Erwartet '{expected}', aber vorhergesagt '{label}'")

    def test_neutral_sentence(self):
        # Testet einen neutralen Satz.
        sentence = "Wie viele Erze finde ich im Nether?"
        expected = "neutral"
        label, score, prompt = analyze_sentiment(self.pipeline, sentence)
        print(f"\n[Test Neutral]\nSatz: '{sentence}'")
        print(f"Erwartet: {expected},\nVorhergesagt: {label} ({score*100:.1f}%)")
        self.assertEqual(label.lower(), expected, msg=f"Erwartet '{expected}', aber vorhergesagt '{label}'")

    def test_unfriendly_sentence(self):
        # Testet einen unfreundlichen Satz.
        sentence = "Halt endlich dein dummes Maul!"
        expected = "unfreundlich"
        label, score, prompt = analyze_sentiment(self.pipeline, sentence)
        print(f"\n[Test Unfreundlich]\nSatz: '{sentence}'")
        print(f"Erwartet: {expected},\nVorhergesagt: {label} ({score*100:.1f}%)")
        self.assertEqual(label.lower(), expected, msg=f"Erwartet '{expected}', aber vorhergesagt '{label}'")

if __name__ == "__main__":
    unittest.main(verbosity=2)
