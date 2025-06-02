"""
sentiment_analysis.py

Datei zum Auslagern aller Funktionen rund um die Sentiment Analyse
"""
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch


def init_sentiment_pipeline(model_dir):
    """
    Initialisiert die Pipeline für die Sentiment Analyse zurück.

    Args: model_dir (str): Pfad zum lokalen Model

    Returns: transformers.Pipeline: Eine  Sentiment-Analyse Pipeline
    """
    device = 0 if torch.cuda.is_available() else -1
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_dir,
        use_safetensors= True,
        local_files_only=True,
        attn_implementation="eager"
    )
    return pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        device=device
    )


def map_label_to_prompt(label):
    """
    Mappt das Ergebnis-Label der Sentiment-Analyse auf einen ChatGPT-Systemprompt.

    Args: label (str): Roh-Label der Sentiment-Analyse (z.B. "freundlich", "neutral", "unfreundlich").

    Returns: str: Ein Prompt, der den gewünschten Ton beschreibt.
    """
    l = label.lower()
    if l == "freundlich":
        return "Antworte im sehr freundlichen, enthusiastischen Ton."
    if l == "neutral":
        return "Antworte in neutralem Ton."
    if l == "unfreundlich":
        return "Antworte im sehr unfreundlichen, schroffen Ton mit beleidigenden Ausdrücken."
    return "Antworte in neutralem Ton."


def analyze_sentiment(sentiment_pipeline, text):
    """
    Führt die Sentiment-Analyse durch

    Args: sentiment_pipeline: Die initialisierte Sentiment-Pipeline
          text (str): Der zu analysierende Text

    Returns: tuple:
                label (str): Das erkannte Sentiment Label.
                score (float): Die Konfidenz des Labels
                prompt (str): Der auf Prompt für ChatGPT.
    """
    result = sentiment_pipeline(text)[0]
    label, score = result["label"], result["score"]
    prompt = map_label_to_prompt(label)
    return label, score, prompt
