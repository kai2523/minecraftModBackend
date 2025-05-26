import Levenshtein


def match_key_words(matching_dict, key_words, max_distance = 1):
    """
    Vergleicht die Schlüsselwörter der Nutzerfrage mit allen Minecraft Wiki Seitentiteln
    und gibt die gematched Titel zurück

    Args:
     matching_dict (dictionary): Alle Minecraft Wiki Seitetitel und Redirect-Titel
     key_words (list): Aus den Nutzerfragen extrahierte Schlüsselwörter
     max_distance (int): Maximale Levenshtein-Distanz
    Returns:
     matched_pages (list): Alle gematchten Seitentitel
    """

    matched_pages = []
    for page_title, info in matching_dict.items():
        # Seitentitel und Redirect-Titel für das Marching nutzen
        redirects = info.get("redirects", [])
        all_titles = [page_title] + redirects
        
        # Schlüsselwörter mit Seitentiteln und Redirect-Titeln matchen
        for key_word in key_words:
            for title in all_titles:
                # Schreibfehler in den Nutzerfragen berücksichtigen
                distance = Levenshtein.distance(key_word, title)
                if distance <= max_distance:
                    matched_pages.append(page_title)
                    break

    return matched_pages