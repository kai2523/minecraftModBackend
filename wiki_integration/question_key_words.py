"""
Copyright Felix Weller, 2025
"""

"""
github commands:
- Packages installieren: npm install

- git pull https://github.com/kai2523/minecraftModBackend.git -> aktuelle Dateien ziehen
- git add . -> alle Dateien auswählen
- git commit -m "Kommentar"
- git push

- Lokal testen: npm start
- curl -X POST https://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -H "api-key: 4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7" \
  -d "{"message": "Chat Nachricht", "context": []}"
"""

import spacy

# Lade das deutsche Sprachmodell
nlp = spacy.load("de_core_news_sm")

def extract_keywords_pos_lemma(user_question):
    # Verarbeite die Eingabe
    doc = nlp(user_question)

    # Definiere wichtige POS-Tags
    important_pos = {"NOUN", "VERB"}

    # Extrahiere Schlüsselwörter (lemma-basiert)
    keywords = []
    for token in doc:
        if token.pos_ in important_pos:
            keywords.append(token.lemma_)

    return keywords

# Holmes-Style rekursiver Compound-Splitter
def holmes_style_compound_split(word, wordlist):
    word = word.lower()
    results = []

    def helper(subword, path):
        if not subword:
            results.append(path)
            return
        for i in range(3, len(subword)+1):
            prefix = subword[:i]
            if prefix in wordlist:
                helper(subword[i:], path + [prefix])

    helper(word, [])

    # Falls keine sinnvolle Zerlegung gefunden wird, gib das Wort selbst zurück
    if not results:
        return [[word]]

    return results

if __name__ == "__main__":
    # Lade Wortliste
    with open("de_50k.txt", encoding="utf-8") as f:
        wordlist = set(line.strip().split()[0] for line in f)

    while True:
        user_question = input("Frage eingeben: ")
        
        # POS-Tagging und Lemmatisierung
        keywords = extract_keywords_pos_lemma(user_question)
        print("Lemma:", keywords)

        # Compound-Splitting für jedes Schlüsselwort
        for keyword in keywords:
            splits = holmes_style_compound_split(keyword, wordlist)
            print(f"Zerlegungen für '{keyword}': {splits}")