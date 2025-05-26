import json
import Levenshtein
import requests
from bs4 import BeautifulSoup


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

    # Matching Dictionary laden
    with open("matching_dict.json", "r", encoding="utf-8") as f:
        matching_dict = json.load(f)

    # Schlüsselwörter matchen
    key_words = ["craften", "diamantspitzhacke", "diamant"]
    matched_pages = match_key_words(matching_dict, key_words)

    # Gematchte Wiki Seiten holen
    response = get_wiki_page(wiki_api_url, matched_pages)

    # Wiki Seiten formattieren
    wiki_pages = format_html(response)

    for i, page in enumerate(wiki_pages, 1):
        print(f"\n--- Seite {i} ---\n")
        print(page)