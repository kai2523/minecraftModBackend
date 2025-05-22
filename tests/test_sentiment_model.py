"""
test_sentiment_analysis.py

Funktion zum Testen der Sentiment-Analyse anhand vordefinierter Beispielsätze.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sentiment_analysis import init_sentiment_pipeline, analyze_sentiment

# Beispielsätze für Test
test_data = [
    # freundlich
    {"sentence": "Du bist so toll und hilfst mir immer!", "label": "freundlich"},
    {"sentence": "Hallo lieber Dorfbewohner, könnte man preislich bei dir noch was machen? Ich kann dir 2 Rohes Kaninchen für einen Smaragd geben. Das wäre wirklich freundlich und ich würde mich echt freuen", "label": "freundlich"},
    {"sentence": "Ich freue mich auf unsere Zusammenarbeit.", "label": "freundlich"},
    {"sentence": "Dein Engagement wird sehr geschätzt.", "label": "freundlich"},
    {"sentence": "Herzlichen Glückwunsch zu deinem großartigen Erfolg!", "label": "freundlich"},

    # neutral
    {"sentence": "Kann man preislich bei dir noch was machen? Ich kann dir 2 Rohes Kaninchen für einen Smaragd geben.", "label": "neutral"},
    {"sentence": "Wie crafte ich eine Diamantspitzhacke?", "label": "neutral"},
    {"sentence": "Das Wald-Biom hat viele Eichenbäume.", "label": "neutral"},
    {"sentence": "Unsere nächste Station ist die Mine zum Erze farmen.", "label": "neutral"},
    {"sentence": "Das Wetter soll morgen bewölkt sein.", "label": "neutral"},

    # unfreundlich
    {"sentence": "Was für ein Idiot bist du bitte?", "label": "unfreundlich"},
    {"sentence": "Willst du stress du Arschloch?", "label": "unfreundlich"},
    {"sentence": "Hey du Arschloch, was kostet eine dämliche Karte bei dir?", "label": "unfreundlich"},
    {"sentence": "Halte endlich dein Maul.", "label": "unfreundlich"},
    {"sentence": "Komm raus ich hau dich!", "label": "unfreundlich"},
    {"sentence": "Du Spast, wie ist das Wetter?", "label": "unfreundlich"},
]

def test_sentiment_analysis(model_dir = "tinybert-german-finetuned"):
    """
    Testet die Sentiment-Analyse-Pipeline anhand vordefinierter Beispielsätze.

    Args: model_dir (str): Pfad zum Model-Ordner.

    Returns: None (Ausgabe im Terminal der erwarteten vs. vorhergesagten Labels aus.
    """
    # Pipeline initialisieren
    pipeline = init_sentiment_pipeline(model_dir)

    # Ergebnisse sammeln
    success = 0
    total = len(test_data)
    print("Starte Sentiment-Analyse Tests...\n")

    for entry in test_data:
        sentence = entry["sentence"]
        expected = entry["label"]
        label, score, prompt = analyze_sentiment(pipeline, sentence)
        # Nur Label vergleichen
        correct = (label.lower() == expected.lower())
        result = "Richig" if correct else "Falsch"
        print(f"{result} Satz: '{sentence}'")
        print(f"    Erwartet: {expected}, Vorhergesagt: {label} ({score*100:.1f}%)")

        if correct:
            success += 1
    
    print(f"\nTestergebnis: {success}/{total} korrekt ({(success/total*100):.1f}%).")


if __name__ == "__main__":
    # Der Pfad 'tinybert-german-finetuned' muss zum Model-Verzeichnis passen
    test_sentiment_analysis()
