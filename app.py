import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from dotenv import load_dotenv
from functools import wraps
from flask import Flask, request
import json
import logging
import pickle
import torch
import openai

# Wiki-Integration
from wiki_integration.get_wiki_information import match_key_words, get_wiki_page, format_html
from wiki_integration.question_key_words import extract_keywords_pos_lemma, holmes_style_compound_split

# Sentiment-Analyse
from sentiment_analysis import init_sentiment_pipeline, analyze_sentiment

# Chat-Request
from llm.chatgpt_request import build_chat_payload, send_chat_request

# Logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

# Env-Variablen
load_dotenv()
PORT = int(os.getenv("PORT", 3000))
VALID_API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WIKI_API_URL = "https://minecraft.fandom.com/de/api.php"
WORDLIST_PATH = "wiki_integration/de_50k.txt"

openai.api_key = OPENAI_API_KEY

# Flask
app = Flask(__name__)
app.config["DEBUG"] = False
app.config["TESTING"] = False
app.config["JSON_AS_ASCII"] = False
app.logger.setLevel(logging.INFO)

# Matching-Dictionary laden
data_dir = os.path.dirname(__file__)
with open(os.path.join(data_dir, 'wiki_integration', 'matching_dict.pkl'), 'rb') as f:
    matching_dict = pickle.load(f)
app.logger.info(f"Wiki-Matching-Dictionary geladen ({len(matching_dict)} Einträge)")

# Wortliste laden
wordlist = set()
with open(WORDLIST_PATH, encoding='utf-8') as f:
    for line in f:
        token = line.strip().split()[0]
        if token:
            wordlist.add(token.lower())
app.logger.info(f"Wortliste geladen ({len(wordlist)} Wörter)")

# Auth-Decorator
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.headers.get("api-key") != VALID_API_KEY:
            return app.response_class(
                response=json.dumps({"error": "Ungültiger API-Schlüssel"}, ensure_ascii=False),
                status=403,
                mimetype="application/json; charset=utf-8"
            )
        return f(*args, **kwargs)
    return decorated

# Sentiment-Pipeline initialisieren
model_dir = os.path.join(data_dir, 'tinybert-german-finetuned')
sentiment_pipeline = init_sentiment_pipeline(model_dir)

# Endpoints
@app.route("/", methods=["GET"])
def health_check():
    return "Minecraft Chat Backend ist aktiv!", 200

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

    # Keyword-Extraktion
    lemmas = extract_keywords_pos_lemma(message)
    app.logger.info(f"Lemmata extrahiert: {lemmas}")
    key_words = []
    for lemma in lemmas:
        for path in holmes_style_compound_split(lemma, wordlist):
            key_words.extend(path)
    key_words = list(dict.fromkeys(key_words))
    app.logger.info(f"Keywords: {key_words}")

    # Wiki-Kontext
    matched = match_key_words(matching_dict, key_words)
    raw_pages = get_wiki_page(WIKI_API_URL, matched)
    wiki_texts = format_html(raw_pages)
    wiki_context = "\n---\n".join(wiki_texts)[:20000]
    app.logger.info(f"Wiki-Kontext-Länge: {len(wiki_context)}")

    # Sentiment
    label, score, sentiment_prompt = analyze_sentiment(sentiment_pipeline, message)
    app.logger.info(f"Sentiment: {label} ({score*100:.1f}%)")

    # Chat-Payload & Anfrage
    messages = build_chat_payload(wiki_context, sentiment_prompt, context, message)
    reply = send_chat_request(messages)
    app.logger.info(f"Antwort an Client: {reply}")

    body = json.dumps({"reply": reply}, ensure_ascii=False)
    return app.response_class(
        response=body,
        status=200,
        mimetype="application/json; charset=utf-8"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
