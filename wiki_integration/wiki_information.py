import requests
from bs4 import BeautifulSoup


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


def format_html_pages(html_pages):
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