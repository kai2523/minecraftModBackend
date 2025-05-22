"""
chatgpt_request.py

Modul zum Erstellen und Abschicken von ChatGPT-Anfragen.
"""
import openai


def build_chat_payload(
    wiki_context: str,
    sentiment_prompt: str,
    previous_context: list[str],
    user_message: str
) -> list[dict]:
    """
    Baut den kompletten Nachrichten-Payload für die OpenAI-Chat-API basierend auf Wiki-Inhalten,
    Sentiment-Anweisung, vorherigem Kontext und der Nutzerfrage.

    Args:
        wiki_context (str): Die formatierten Minecraft-Wiki-Inhalte.
        sentiment_prompt (str): Der auf das Sentiment gemappte Ton-Prompt.
        previous_context (list[str]): Bisheriger Chat-Verlauf als Liste von Antworten.
        user_message (str): Die aktuelle Nutzerfrage.

    Returns:
        list[dict]: Nachrichtenliste für ChatGPT (system, assistant, user).
    """
    system_message = (
        "Nutze ausschließlich die folgenden Minecraft-Wiki-Inhalte und den gegebenen Kontext, um die Frage zu beantworten.\n"
        f"{wiki_context}\n"
        "Du bist ein Villager in Minecraft. Dein Wissen beschränkt sich auf Minecraft.\n"
        "Beantworte nur basierend auf den Wiki-Informationen und dem Kontext.\n"
        f"{sentiment_prompt}\n"
        "Gib mir bitte eine kurze Antwort."
    )
    return [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": "\n".join(previous_context)},
        {"role": "user", "content": user_message},
    ]


def send_chat_request(messages: list[dict], model: str = "gpt-3.5-turbo", temperature: float = 0.7) -> str:
    """
    Sendet die Chat-Anfrage an die OpenAI-API und gibt die Antwort zurück.

    Args:
        messages (list[dict]): Die vorbereitete Nachrichtenliste.
        model (str): Gewünschtes Modell (Standard: gpt-3.5-turbo).
        temperature (float): Sampling-Temperatur.

    Returns:
        str: Der Text der ChatGPT-Antwort.
    """
    resp = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return resp.choices[0].message.content
