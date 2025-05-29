import spacy


def extract_keywords_pos_lemma_ner(user_question):
    """
    Extrahiert Schlüsselwörter aus der Nutzereingabe mittels POS-Tagging und Named Entity Recognition (NER).
    
    Args:
     user_question (str): Die vom Nutzer eingegebene Frage auf Deutsch.
    
    Returns:
     keywords (list):   Eine Liste eindeutiger Schlüsselwörter, bestehend aus wichtigen Lemmata
                        (Nomen, Verben) und benannten Entitäten.
    """

    # Lade das deutsche Sprachmodell für die Verarbeitung natürlicher Sprache
    nlp = spacy.load("de_core_news_sm")

    doc = nlp(user_question)
    important_pos = {"NOUN", "VERB"}

    keywords = []

    # Extrahiere relevante Lemmata basierend auf den POS-Tags
    for token in doc:
        lemma = token.lemma_
        if token.pos_ in important_pos and lemma not in keywords:
            keywords.append(lemma)

    # Falls noch nicht enthalten, füge zusätzlich erkannte Named Entities hinzu
    for ent in doc.ents:
        if ent.text not in keywords:
            keywords.append(ent.text)

    return keywords


def holmes_style_compound_split(word, wordlist):
    """
    Zerlegt zusammengesetzte deutsche Wörter rekursiv nach dem Holmes-Ansatz.

    Args:
     word (str): Das zusammengesetzte Wort, das zerlegt werden soll.
     wordlist (set): Eine Menge gültiger deutscher Wörter, gegen die geprüft wird.
    
    Returns:
     results (list):    Eine Liste möglicher Wortzerlegungen. 
                        Das ursprüngliche Wort wird immer als erste Variante zurückgegeben.
    """
    
    # Normalisiere auf Kleinschreibung für den Vergleich mit Wortliste
    word = word.lower()
    results = []

    def helper(subword, path):
        # Wenn das Wort vollständig zerlegt wurde, speichere die Pfadkombination
        if not subword:
            results.append(path)
            return

        # Versuche ab Position 3 alle möglichen Prefixe, die in der Wortliste enthalten sind
        for i in range(3, len(subword)+1):
            prefix = subword[:i]
            if prefix in wordlist:
                helper(subword[i:], path + [prefix])

    helper(word, [])

    # Falls keine Wortzerlegung gefunden wurde, gib das Originalwort zurück
    return [[word]] + results if results else [[word]]

'''
Hinweis zur Wortliste:
Die Datei "de_50k.txt" enthält die 50.000 häufigsten deutschen Wörter (basierend auf OpenSubtitles 2018),
und dient der Zerlegung zusammengesetzter Wörter (Compound-Splitting).
Quelle: https://github.com/hermitdave/FrequencyWords/blob/master/content/2018/de/de_50k.txt
'''