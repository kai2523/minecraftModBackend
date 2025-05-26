"""
Copyright Felix Weller, 2025
"""

import requests
import string
import Levenshtein
from bs4 import BeautifulSoup

import pickle


def create_matching_dict(wiki_api_url):
    """
    Erstellt ein Dictionary, das die Seitentitel und Redirect-Titel für jede
    Minecraft Wiki Seite als Basis für das Matching der Schlüsselwörter
    aus den Nutzerfragen mit den Minecraft Wiki Seiten enthält

    Args:
     wiki_api_url (str): URL des Minecraft Wiki für den API call
    Returns:
     matching_dict (dicitonary): Alle Minecraft Wiki Seitetitel und Redirect-Titel
    """

    # Alle Seitentitel holen
    page_titles = get_wiki_page_titles(wiki_api_url)
    print(f"{len(page_titles)} Titel gefunden.")

    # Matching Dictionary erstellen
    matching_dict = {}
    for page_title in page_titles:
        # Alle Redirect-Titel holen
        redirect_titles = get_wiki_page_redirect_titles(wiki_api_url, page_title)
        section_infos = get_wiki_page_section_infos(wiki_api_url, page_title)

        sections = []
        for title, index in section_infos:
            sections.append({
                "title": title,
                "index": index
            })

        matching_dict[page_title] = {
            "redirects": redirect_titles,
            "sections": section_infos
        }

    return matching_dict


def get_wiki_page_titles(wiki_api_url):
    """
    Führt API Calls an das Minecraft Wiki aus, die den Titel jeder
    Minecraft Wiki Seite zurückgeben

    Args:
     wiki_api_url (str): URL des Minecraft Wiki für den API call
    Returns:
     page_titles (list): Liste aller Minecraft Wiki Seitentitel
    """

    page_titles = []
    letters = list(string.ascii_uppercase) + ["Ä", "Ö", "Ü"]
    apcontinue = None

    # Alle Seitentitel von der Minecraft Wiki API holen
    for letter in letters:
        while True:
            headers = {
                "User-Agent": "MinecraftVillagerBot"
            }
            params = {
                "action": "query",
                "format": "json",
                "list": "allpages",
                "apprefix": letter,
                "apfilterredir": "nonredirects",
                "aplimit": "max"
            }

            if apcontinue:
                params["apcontinue"] = apcontinue

            response = requests.get(wiki_api_url, headers=headers, params=params)

            # Seitentitel sammeln
            data = response.json()
            pages = data.get("query", {}).get("allpages", [])
            for page in pages:
                page_title = page["title"].lower()


                """
                # Seiten, die mit "Version", "Vollversion" (etc.) beginnen, herausfiltern
                if not page_title.startswith("Version"):
                    page_titles.append(page_title)
                """


                page_titles.append(page_title)

            # Prüfen, ob weitere Seitentitel in der Antwort vorhanden sind
            if "continue" in data:
                apcontinue = data["continue"]["apcontinue"]
            else:
                break

    return page_titles


def get_wiki_page_redirect_titles(wiki_api_url, page_title):
    """
    Führt einen API Call an das Minecraft Wiki aus, der alle Redirect-Titel für die
    gegebene Minecraft Wiki Seite zurückgibt

    Args:
     wiki_api_url (str): URL des Minecraft Wiki für den API call
     page_title (str): Title der gegebenen Minecraft Wiki Seite
    Returns:
     redirect_titles (list): Liste aller Redirect-Titel, die auf die gegebene
                             Minecraft Wiki Seite führen
    """

    headers = {
        "User-Agent": "MinecraftVillagerBot"
    }
    params = {
        "action": "query",
        "format": "json",
        "list": "backlinks",
        "bltitle": page_title,
        "blfilterredir": "redirects",
        "bllimit": "max"
    }

    response = requests.get(wiki_api_url, headers=headers, params=params)

    # Redirect-Titel sammeln
    data = response.json()
    backlinks = data.get("query", {}).get("backlinks", [])
    redirect_titles = []
    for backlink in backlinks:
        redirect_title = backlink["title"].lower()
        redirect_titles.append(redirect_title)

    return redirect_titles


def get_wiki_page_section_infos(wiki_api_url, page_title):
    """
    Führt einen API Call an das Minecraft Wiki aus, der den Titel und alle Unterkapitel
    und deren Indizes von der gegebenen Minecraft Wiki Seite zurückgibt

    Args:
     wiki_api_url (str): URL des Minecraft Wiki für den API call
     page_title (str): Title der gegebenen Minecraft Wiki Seite
    Returns:
     section_infos (list): Liste aller Unterkapitel und deren Indizes der gegebenen
                           Minecraft Wiki Seite
    """


    """
    es kann sein, dass wg der Wikistruktur kein Index für eine Section vorhanden ist,
    s. Seite "Handwerk"
    """


    # Alle Informationen zu den Unterkapiteln von der Minecraft Wiki API holen
    headers = {
        "User-Agent": "MinecraftVillagerBot"
    }
    params = {
        "action": "parse",
        "format": "json",
        "prop": "sections",
        "page": page_title,
        "redirects": 1
    }

    response = requests.get(wiki_api_url, headers=headers, params=params)

    # Titel und Indizes der Unterkapitel holen
    data = response.json()
    sections = data.get("parse", {}).get("sections", [])
    section_infos = []
    for section in sections:
        title = section["line"]
        index = section["index"]
        section_infos.append((title, index))

    return section_infos


def match_key_words(matching_dict, key_words, max_distance = 0):
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


def get_wiki_page(wiki_api_url, matched_pages):
    """
    Führt API Calls an das Minecraft Wiki aus, die die vollständigen Seiteninhalte
    der gegebenen Seitentitel zurückgeben

    Args:
     wiki_api_url (str): URL des Minecraft Wiki für den API call
     matched_pages (list): Alle gematchten Seitentitel
    Returns:
     html_pages (list): HTML der gematchten Minecraft Wiki Seiten
    """

    """
    noch Error-Handling einbauen falls page_title wg Technik Wiki etc. nicht funktioniert
    """

    # Seiten von der Minecraft Wiki API holen
    html_pages = []
    for page_title in matched_pages:
        headers = {
            "User-Agent": "MinecraftVillagerBot"
        }
        params = {
            "action": "parse",
            "format": "json",
            "prop": "text",
            "page": page_title,
            # "section": 6,
            "redirects": 1
        }

        response = requests.get(wiki_api_url, headers=headers, params=params)

        # Antwort parsen
        json = response.json()
        html = json["parse"]["text"]["*"]
        html = BeautifulSoup(html, "html.parser")

        html_pages.append(html)

    return html_pages


def format_html(html_pages):
    """
    Formatiert den HTML-Code der gematchten Minecraft Wiki Seiten als normalen Text

    Args:
     html_pages (list): HTML der gematchten Minecraft Wiki Seiten
    Returns:
     formatted_pages (list): Formattierter Text der gematchten Minecraft Wiki Seiten
    """

    formatted_pages = []
    for html_page in html_pages:
        # Mobile only Abschnitte entfernen
        for section in html_page.find_all(class_="nomobile mobileonly"):
            section.decompose()

        for section in html_page.find_all("span", class_="dateiUrl nomobile mobileonly"):
            section.decompose()

        # Tabellen formatieren
        tables = html_page.find_all("table")

        for table in tables:
            rows = table.find_all("tr")
            formatted_rows = []

            # Tabellenüberschrift miteinbeziehen
            if table.caption:
                caption = table.caption.get_text(separator=" ", strip=True)
                formatted_rows.append(f"\n{caption}")

            # Jede Tabellenzeile formatieren
            rowspans = {}
            for row in rows:
                cols = row.find_all(["th", "td"])
                col_text = []
                col_idx = 0

                # Jede Tabellenspalte der Zeile formatieren
                for col in cols:
                    # Rowspan- und Colpan-Argument berücksichtigen
                    while col_idx in rowspans:
                        remaining, value = rowspans[col_idx]
                        col_text.append(value)

                        if remaining > 1:
                            rowspans[col_idx][0] -= 1
                        else:
                            del rowspans[col_idx]

                        col_idx += 1

                    # Text der Spalte holen
                    text = col.get_text(separator=" ", strip=True)
                    if not text:
                        text = "Bild"

                    # Rowspan- und Colspan-Werte holen
                    rowspan = int(col.get("rowspan", 1))
                    colspan = int(col.get("colspan", 1))

                    if rowspan > 1:
                        for offset in range(colspan):
                            rowspans[col_idx + offset] = [rowspan - 1, text]

                    # Colspan-Werte hinzufügen
                    col_text.extend([text] * colspan)
                    col_idx += colspan

                # Rowpsan-Werte hinzufügen
                while col_idx in rowspans:
                    remaining, value = rowspans[col_idx]
                    col_text.append(value)
                    if remaining > 1:
                        rowspans[col_idx][0] -= 1
                    else:
                        del rowspans[col_idx]
                    col_idx += 1

                formatted_rows.append(" | ".join(col_text))

            # Html-Code der Tabelle mit Text ersetzen
            table_text = "\n".join(formatted_rows)
            table.string = table_text

        # Verbleibenden HTML-Code mit Text ersetzen
        page_text = html_page.get_text()

        formatted_pages.append(page_text)

    return formatted_pages


if __name__ == "__main__":
    # API URL des offiziellen Minecraft Wiki
    wiki_api_url = "https://de.minecraftwiki.net/api.php"

    # matching_dict = create_matching_dict(url_fandom_wiki)
    """with open("matching_dict.pkl", "wb") as f:
        pickle.dump(matching_dict, f)"""

    with open("matching_dict.pkl", "rb") as f:
        matching_dict = pickle.load(f)

    key_words = ["craften", "diamantspitzhacke", "diamant"]
    matched_pages = match_key_words(matching_dict, key_words)
    print(matched_pages)

    response = get_wiki_page(wiki_api_url, matched_pages)
    wiki_pages = format_html(response)

    for i, page in enumerate(wiki_pages, 1):
        print(f"\n--- Seite {i} ---\n")
        print(page)