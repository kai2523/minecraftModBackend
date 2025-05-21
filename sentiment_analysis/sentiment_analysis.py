"""
sentiment_analysis.py

Modul zur Kapselung aller Funktionen rund um die Sentiment-Analyse.
"""
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch


def init_sentiment_pipeline(model_dir: str, use_safetensors: bool = True):
    """
    Initialisiert und gibt eine Huggingface-Pipeline für Sentiment-Analyse zurück.

    Args:
        model_dir (str): Pfad zum lokalen Model-Ordner (z.B. tinybert-german-finetuned).
        use_safetensors (bool): Ob das Model im Safetensors-Format geladen wird.

    Returns:
        transformers.Pipeline: Eine einsatzbereite Sentiment-Analyse-Pipeline.
    """
    device = 0 if torch.cuda.is_available() else -1
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_dir,
        use_safetensors=use_safetensors,
        local_files_only=True,
        attn_implementation="eager"
    )
    return pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer,
        device=device
    )


def map_label_to_prompt(label: str) -> str:
    """
    Mappt das Ergebnis-Label der Sentiment-Analyse auf einen ChatGPT-Systemprompt.

    Args:
        label (str): Roh-Label der Sentiment-Analyse (z.B. "freundlich", "neutral", "unfreundlich").

    Returns:
        str: Ein Prompt, der den gewünschten Ton beschreibt.
    """
    l = label.lower()
    if l == "freundlich":
        return "Antworte im sehr freundlichen, enthusiastischen Ton."
    if l == "neutral":
        return "Antworte in neutralem Ton."
    if l == "unfreundlich":
        return "Antworte im sehr unfreundlichen, schroffen Ton mit beleidigenden Ausdrücken."
    return "Antworte in neutralem Ton."


def analyze_sentiment(sentiment_pipeline, text: str) -> tuple[str, float, str]:
    """
    Führt die Sentiment-Analyse auf dem gegebenen Text aus und gibt Label, Score und System-Prompt zurück.

    Args:
        sentiment_pipeline (transformers.Pipeline): Die initialisierte Sentiment-Pipeline.
        text (str): Der zu analysierende Text.

    Returns:
        tuple:
            - label (str): Das erkannte Sentiment-Label.
            - score (float): Die Konfidenz des Labels.
            - prompt (str): Der auf das Label gemappte System-Prompt für ChatGPT.
    """
    result = sentiment_pipeline(text)[0]
    label, score = result["label"], result["score"]
    prompt = map_label_to_prompt(label)
    return label, score, prompt
