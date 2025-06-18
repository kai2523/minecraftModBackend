"""
chatgpt_request.py

Modul zum Erstellen und Abschicken von ChatGPT-Anfragen.
"""
import openai


def build_chat_payload(wiki_context, sentiment_prompt, context, user_message):
    """
    Baut den kompletten Nachrichten-Payload für die OpenAI-Chat-API basierend auf Wiki-Inhalten,
    Sentiment-Anweisung, vorherigem Kontext und der Nutzerfrage.

    Args:
        wiki_context (str): Die Minecraft-Wiki-URLs der entsprechenden Seiten
        sentiment_prompt (str): Der auf das Sentiment gemappte Ton-Prompt.
        context (list[str]): Kontext mit Infos über Minecraft und den Villager
        user_message (str): Die aktuelle Nutzerfrage.

    Returns:
        list[dict]: Nachrichtenliste für ChatGPT (system, assistant, user).
    """
    system_message = (
        "Nutze ausschließlich die Inhalte der folgenden Minecraft-Wiki-Seiten, die du bei Bedarf aufrufst und den gegebenen Kontext, um die Frage zu beantworten.\n"
        f"{wiki_context}\n"
        "Du bist ein Villager in Minecraft. Dein Wissen beschränkt sich auf Minecraft.\n"
        "Beantworte nur basierend auf den Wiki-Informationen und dem Kontext.\n"
        "Du darfst auf keinen Fall Emojis oder andere Sonderzeichen verwenden!\n"
        f"{sentiment_prompt}\n"
        "Gib mir bitte eine kurze Antwort."
    )
    return [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": "\n".join(context)},
        {"role": "user", "content": user_message},
    ]


def send_chat_request(messages, model = "gpt-4o", temperature = 0.7):
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
