import os
# 0) Fehlermeldung zur Parallelität unterdrücken
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from dotenv import load_dotenv
from functools import wraps
from flask import Flask, request
from flask.json import jsonify as flask_jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
import openai
import logging
import json

# Wiki-Integration
from wiki_integration.get_wiki_information import (
    match_key_words,
    get_wiki_page,
    format_html
)
# POS-Tagging und Lemmatisierung
from wiki_integration.question_key_words import (
    extract_keywords_pos_lemma,
    holmes_style_compound_split
)
import pickle

# 1) Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

# 2) Env-Variablen laden
load_dotenv()
PORT = int(os.getenv("PORT", 3000))
VALID_API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WIKI_API_URL = os.getenv("WIKI_API_URL", "https://minecraft.fandom.com/de/api.php")
WORDLIST_PATH = "wiki_integration/de_50k.txt"

# OpenAI API-Key konfigurieren
openai.api_key = OPENAI_API_KEY

# 3) Flask-App initialisieren
app = Flask(__name__)

app.config["DEBUG"] = False
app.config["TESTING"] = False
# JSON-Unicode-Ausgabe
app.config["JSON_AS_ASCII"] = False
app.logger.setLevel(logging.INFO)

# 4) Load matching_dict einmalig
data_dir = os.path.dirname(__file__)
matching_dict_path = os.path.join(data_dir, 'wiki_integration', 'matching_dict.pkl')
with open(matching_dict_path, 'rb') as f:
    matching_dict = pickle.load(f)
app.logger.info(f"Wiki-Matching-Dictionary geladen ({len(matching_dict)} Einträge)")

# 5) Wortliste laden für Compound-Splitter
wordlist = set()
with open(WORDLIST_PATH, encoding='utf-8') as f:
    for line in f:
        word = line.strip().split()[0]
        if word:
            wordlist.add(word.lower())
app.logger.info(f"Wortliste geladen ({len(wordlist)} Wörter)")

# 6) API-Key Authentication Decorator
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get("api-key")
        if api_key != VALID_API_KEY:
            app.logger.warning(f"Ungültiger API-Schlüssel: {api_key}")
            return app.response_class(
                response=json.dumps({"error": "Ungültiger API-Schlüssel"}, ensure_ascii=False),
                status=403,
                mimetype="application/json; charset=utf-8"
            )
        return f(*args, **kwargs)
    return decorated

# 7) Sentiment-Pipeline initialisieren
model_dir = os.path.join(data_dir, 'tinybert-german-finetuned')
device = 0 if torch.cuda.is_available() else -1

tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSequenceClassification.from_pretrained(
    model_dir,
    use_safetensors=True,
    local_files_only=True,
    attn_implementation="eager"
)
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model=model,
    tokenizer=tokenizer,
    device=device
)
app.logger.info("Sentiment-Pipeline mit finetuned TinyBERT-German geladen.")

# 8) Label-Mapping
def map_label(label: str) -> str:
    l = label.lower()
    if l == "freundlich":
        return "Antworte im sehr freundlichen, enthusiastischen Ton."
    if l == "neutral":
        return "Antworte in neutralem Ton."
    if l == "unfreundlich":
        return "Antworte im sehr unfreundlichen, schroffen Ton mit beleidigenden Ausdrücken."
    return "Antworte in neutralem Ton."

# 9) Health-Check Endpoint
@app.route("/", methods=["GET"])
def health_check():
    return "Minecraft Chat Backend ist aktiv!", 200

# 10) Chat Endpoint
@app.route("/chat", methods=["POST"])
@require_api_key
def chat():
    data = request.get_json() or {}
    message = data.get("message")
    context = data.get("context", [])

    if not message:
        return app.response_class(
            response=json.dumps({"error": "Keine Nachricht übergeben."}, ensure_ascii=False),
            status=400,
            mimetype="application/json; charset=utf-8"
        )

    # 10.1) Keyword-Extraktion mit POS & Lemma
    lemmas = extract_keywords_pos_lemma(message)
    app.logger.info(f"Lemmata extrahiert: {lemmas}")
    # Compound-Splitter anwenden
    key_words = []
    for lemma in lemmas:
        splits = holmes_style_compound_split(lemma, wordlist)
        # Splits ist Liste von Listen, wir nehmen alle Komponenten
        for path in splits:
            key_words.extend(path)
    # Duplikate entfernen
    key_words = list(dict.fromkeys(key_words))
    app.logger.info(f"Endgültige Keywords: {key_words}")

    # 10.2) Wiki-Abfrage
    matched = match_key_words(matching_dict, key_words)
    app.logger.info(f"Gefundene Wiki-Seiten: {matched}")
    raw_pages = get_wiki_page(WIKI_API_URL, matched)
    wiki_texts = format_html(raw_pages)
    wiki_context = "\n---\n".join(wiki_texts)[:20000]
    app.logger.info(f"Wiki Kontext Länge: {len(wiki_context)}")

    # 10.3) Sentiment-Analyse
    result = sentiment_pipeline(message)[0]
    label, score = result["label"], result["score"]
    app.logger.info(f"Prompt: {message}")
    app.logger.info(f"Sentiment-Rating: {label} ({score*100:.1f}%)")
    sentiment_prompt = map_label(label)

    # 10.4) System-Prompt mit Wiki-Content
    system_message = (
        "Nutze ausschließlich die folgenden Minecraft-Wiki-Inhalte und den gegebenen Kontext, um die Frage zu beantworten.\n"
        f"{wiki_context}\n"
        "Du bist ein Villager in Minecraft. Dein Wissen beschränkt sich auf Minecraft.\n"
        "Beantworte nur basierend auf den Wiki-Informationen und dem Kontext.\n"
        f"{sentiment_prompt}\n"
        "Gib mir bitte eine kurze Antwort."
    )
    messages = [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": "\n".join(context)},
        {"role": "user", "content": message},
    ]

    # 10.5) Anfrage an OpenAI
    try:
        resp = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )
        reply = resp.choices[0].message.content
        app.logger.info(f"Antwort an Client: {reply}")
        response_body = json.dumps({"reply": reply}, ensure_ascii=False)
        return app.response_class(
            response=response_body,
            status=200,
            mimetype="application/json; charset=utf-8"
        )
    except Exception as e:
        app.logger.error(f"Fehler im /chat Handler: {e}")
        return app.response_class(
            response=json.dumps({"error": "Fehler bei der Verarbeitung der Anfrage."}, ensure_ascii=False),
            status=500,
            mimetype="application/json; charset=utf-8"
        )

# 11) Server starten
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
