import requests
import string
import json


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

    # Matching Dictionary erstellen
    matching_dict = {}
    for page_title in page_titles:
        # Alle Redirect-Titel holen
        redirect_titles = get_wiki_page_redirect_titles(wiki_api_url, page_title)
        wiki_page_url = get_wiki_page_url(wiki_api_url, page_title)

        matching_dict[page_title] = {
            "redirects": redirect_titles,
            "url": wiki_page_url
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
     page_title (str): Titel der gegebenen Minecraft Wiki Seite
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
        "bltitle": page_title,
        "list": "backlinks",
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


def get_wiki_page_url(wiki_api_url, page_title):
    """
    Führt API Calls an das Minecraft Wiki aus, die die Url der gegebenen Minecraft
    Wiki Seite zurückgibt

    Args:
     wiki_api_url (str): URL des Minecraft Wiki für den API call
     page_title (str): Titel der gegebenen Minecraft Wiki Seite
    Returns:
     wiki_page_url (string): URL zur gegebenen Minecraft Wiki Seite
    """

    headers = {
        "User-Agent": "MinecraftVillagerBot"
    }
    params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "info",
        "inprop": "url",
        "redirects": 1
    }

    response = requests.get(wiki_api_url, headers=headers, params=params)

    # Url holen
    data = response.json()
    pages = data["query"]["pages"]
    for page in pages.values():
        wiki_page_url = page.get("fullurl")

    return wiki_page_url


if __name__ == "__main__":
    # API URL des offiziellen Minecraft Wiki
    wiki_api_url = "https://de.minecraftwiki.net/api.php"

    # Matching Dicitonary erstellen
    matching_dict = create_matching_dict(wiki_api_url)

    # Matching Dictionary als JSON speichern
    with open("matching_dict.json", "w", encoding="utf-8") as f:
        json.dump(matching_dict, f, ensure_ascii=False, indent=4)