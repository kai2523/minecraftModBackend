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
    Creates a dictionary which contains the page titles and redirect titles
    for each Minecraft Wiki page as the basis for matching the key words from
    the user question with the Minecraft Wiki pages

    Args:
     wiki_api_url (str): URL of the Minecraft Wiki used in the API call
    Return:
     matching_dict (dicitonary): All Minecraft Wiki page titles and redirect titles
    """

    # Get all page titles
    page_titles = get_wiki_page_titles(wiki_api_url)
    print(f"{len(page_titles)} Titel gefunden.")

    # Create matching dictionary
    matching_dict = {}
    for page_title in page_titles:
        # Get all redirect titles
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
    Makes an API call to the Minecraft Wiki which gets the title of each
    Minecraft Wiki page

    Args:
     wiki_api_url (str): URL of the Minecraft Wiki used in the API call
    Return:
     page_titles (list): List of all Minecraft Wiki page titles
    """

    page_titles = []
    letters = list(string.ascii_uppercase) + ["Ä", "Ö", "Ü"]
    apcontinue = None

    # Get all page titles from Media Wiki API
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

            # Collect page titles
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

            # Check if there are more pages
            if "continue" in data:
                apcontinue = data["continue"]["apcontinue"]
            else:
                break

    # page_titles = ["handwerk", "spitzhacke"]

    return page_titles


def get_wiki_page_redirect_titles(wiki_api_url, page_title):
    """
    Makes an API call to the Minecraft Wiki which gets the titles of all redirects
    to the given Minecraft Wiki page

    Args:
     wiki_api_url (str): URL of the Minecraft Wiki used in the API call
     page_title (str): Title of the given Minecraft Wiki page
    Return:
     redirect_titles (list): List of all redirect titles to the Minecraft Wiki page
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

    # Collect redirect title
    data = response.json()
    backlinks = data.get("query", {}).get("backlinks", [])
    redirect_titles = []
    for backlink in backlinks:
        redirect_title = backlink["title"].lower()
        redirect_titles.append(redirect_title)

    return redirect_titles


def get_wiki_page_section_infos(wiki_api_url, page_title):
    """
    Makes an API call to the Minecraft Wiki which gets the titles of all sections
    and their indexes of the given Minecraft Wiki page

    Args:
     wiki_api_url (str): URL of the Minecraft Wiki used in the API call
     page_title (str): Title of the given Minecraft Wiki page
    Return:
     section_infos (list): List of all sections and section indexes of the
                             Minecraft Wiki page
    """


    """
    es kann sein, dass wg der Wikistruktur kein Index für eine Section vorhanden ist,
    s. Seite "Handwerk"
    """


    # Get all section infos from Media Wiki API
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

    # Collect section titles and indexes
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
    Compares the key words from the user question to all Minecraft Wiki page titles
    and returns the matched titles

    Args:
     matching_dict (dictionary): All Minecraft Wiki page titles and redirect titles
     key_words (list): Extracted key words from the user question
     max_distance (int): Maximum distance for calculating the Levenshtein distance
    Return:
     matched_pages (list): All matched page titles
    """

    matched_pages = []
    for page_title, info in matching_dict.items():
        # Use page title and redirect titles for matching
        redirects = info.get("redirects", [])
        all_titles = [page_title] + redirects
        
        # Check if key words match with titles or redirects
        for key_word in key_words:
            for title in all_titles:
                # Consider typos in user questions
                distance = Levenshtein.distance(key_word, title)
                if distance <= max_distance:
                    matched_pages.append(page_title)
                    break

    return matched_pages


def get_wiki_page(wiki_api_url, matched_pages):
    """
    Makes API calls to the Minecraft Wiki which get the full Minecraft Wiki pages
    by the page titles

    Args:
     wiki_api_url (str): URL of the Minecraft Wiki used in the API call
     matched_pages (list): Titles of the matched Minecraft Wiki pages
    Return:
     html_pages (list): HTML codes of the matched Minecraft Wiki pages
    """

    """
    noch Error-Handling einbauen falls page_title wg Technik Wiki etc. nicht funktioniert
    """

    # Get wiki page from Media Wiki API
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

        # Parse response
        json = response.json()
        html = json["parse"]["text"]["*"]
        html = BeautifulSoup(html, "html.parser")

        html_pages.append(html)

    return html_pages


def format_html(html_pages):
    """
    Formats the HTML codes of the matched Minecraft Wiki pages into normal text

    Args:
     html_pages (list): HTML codes of the matched Minecraft Wiki pages
    Return:
     formatted_pages (list): Formatted text of the matched Minecraft Wiki pages
    """

    formatted_pages = []
    for html_page in html_pages:
        # Remove mobile only sections
        for section in html_page.find_all(class_="nomobile mobileonly"):
            section.decompose()

        for section in html_page.find_all("span", class_="dateiUrl nomobile mobileonly"):
            section.decompose()

        # Format tables
        tables = html_page.find_all("table")

        for table in tables:
            rows = table.find_all("tr")
            formatted_rows = []

            # Include table header
            if table.caption:
                caption = table.caption.get_text(separator=" ", strip=True)
                formatted_rows.append(f"\n{caption}")

            # Format each table row
            rowspans = {}
            for row in rows:
                cols = row.find_all(["th", "td"])
                col_text = []
                col_idx = 0

                for col in cols:
                    # Consider rowspan and colspan argument
                    while col_idx in rowspans:
                        remaining, value = rowspans[col_idx]
                        col_text.append(value)

                        if remaining > 1:
                            rowspans[col_idx][0] -= 1
                        else:
                            del rowspans[col_idx]

                        col_idx += 1

                    # Get text from each column
                    text = col.get_text(separator=" ", strip=True)
                    if not text:
                        text = "Bild"

                    # Get rowspan and colspan argument
                    rowspan = int(col.get("rowspan", 1))
                    colspan = int(col.get("colspan", 1))

                    if rowspan > 1:
                        for offset in range(colspan):
                            rowspans[col_idx + offset] = [rowspan - 1, text]

                    # Add colspan values
                    col_text.extend([text] * colspan)
                    col_idx += colspan

                # Add rowspan values
                while col_idx in rowspans:
                    remaining, value = rowspans[col_idx]
                    col_text.append(value)
                    if remaining > 1:
                        rowspans[col_idx][0] -= 1
                    else:
                        del rowspans[col_idx]
                    col_idx += 1

                formatted_rows.append(" | ".join(col_text))

            # Replace table html with text
            table_text = "\n".join(formatted_rows)
            table.string = table_text

        # Replace remaining html with text
        page_text = html_page.get_text()

        formatted_pages.append(page_text)

    return formatted_pages


if __name__ == "__main__":
    # API URLs for the Minecraft Fandom Wiki and the official Minecraft Wiki
    url_fandom_wiki = "https://minecraft.fandom.com/de/api.php"
    url_official_wiki = "https://de.minecraftwiki.net/api.php"

    # matching_dict = create_matching_dict(url_fandom_wiki)
    """with open("matching_dict.pkl", "wb") as f:
        pickle.dump(matching_dict, f)"""

    with open("matching_dict.pkl", "rb") as f:
        matching_dict = pickle.load(f)

    key_words = ["craften", "diamantspitzhacke", "diamant"]
    matched_pages = match_key_words(matching_dict, key_words)
    print(matched_pages)

    response = get_wiki_page(url_fandom_wiki, matched_pages)
    wiki_pages = format_html(response)

    for i, page in enumerate(wiki_pages, 1):
        print(f"\n--- Seite {i} ---\n")
        print(page)