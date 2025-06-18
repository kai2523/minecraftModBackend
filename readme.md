# Minecraft Mod Backend

Dieses Projekt stellt ein Python-basiertes Backend für eine Minecraft-Mod bereit. Es ermöglicht, 
mit Dorfbewohnern (Villagern) über einen Chatbot zu interagieren. Der Bot nutzt Informationen aus 
der deutschen Minecraft-Wiki und generiert Antworten über die OpenAI API.

## Funktionen

* Extraktion von Schlüsselwörtern mittels **spaCy** (POS-Tagging und Named Entity Recognition)
* Matching dieser Schlüsselwörter mit dem Minecraft-Wiki (Levenshtein-Distanz)
* Abfrage von Inhalten der Mincraft Wiki Seite
* Sentiment-Analyse über ein fingetuntes, deutsches TinyBERT-Modell
* Generierung der finalen Chat-Antwort durch ChatGPT
* Unit-Tests für Kernkomponenten

## Komponenten im Detail

### Sentimentanalyse

Das Modul `sentiment_analysis.py` nutzt ein lokal gespeichertes BERT-Modell,
das aus dem öffentlichen **TinyBERT_General_4L_312D_de** von Hugging Face
gefintunt wurde. Das Finetuning erfolgte auf einem kleinen, von ChatGPT generierten
Datensatz mit den Klassen *freundlich*, *neutral* und *unfreundlich*. 
Die einzelnen Schritte zur Datenaufbereitung und zum Training
sind in den Jupyter-Notebooks unter `finetune_sentiment_model/` dokumentiert.
Zur Laufzeit wird das gefintunte Modell geladen und macht eine Sentimentanalyse für
den vom Spieler eingegebene Nachricht. Anschließend wird auf basis des zurückgegeben Sentiments
ein passenden Prompt erstellt, der den Ton bzw. Freundlichkeit der ChatGPT-Antwort steuert.

### Wortzerlegung und Lemmatisierung

In der Datei `question_key_words.py` wird die Nutzerfrage zunächst mithilfe von **spaCy** analysiert. Dabei werden die Lemmata aller erkannten Nomen und Verben extrahiert sowie zusätzliche Named Entities identifiziert. Zur Erkennung zusammengesetzter deutscher Wörter wird anschließend die Funktion `holmes_style_compound_split` aufgerufen. Diese nutzt die Wortliste aus `de_50k.txt`, um Wörter rekursiv in sinnvolle Einzelbestandteile zu zerlegen. Die Keywords werden anschließend für die Suche im Minecraft-Wiki verwendet.

### Lookup im Minecraft-Wiki

Anhand der Schlüsselwörter aus der Frage werden in `key_words_matching.py` die zur Beantwortung
der Frage benötigten Minecraft Wiki Seiten bestimmt. Die Grundlage hierfür bildet das
`matching_dict.json`, das in `matching_dict.py` über API-Calls an die Minecraft Wiki API erstellt
wurde. Es enthält die Titel aller verfügbaren Minecraft Wiki Seiten sowie deren Redirects und
deren URL. `matching_dict.py` prüft für jedes Key Word, ob dieses mit einem Seitentitel oder einem
Redirect auf eine Seite übereinstimmt, wobei es Schreibfehler mit einer Levenshtein-Distanz von 1
berücksichtigt. Eine höhere Levenshtein-Distanz als 1 würde in vielen Fällen zu einem Matching
mit ungewollten Seiten führen.

Die gematchten Wiki Seiten können im weiteren Verlauf entweder in Form der URL oder als Volltext
in der ChatGPT-Request übergeben werden. Für den Volltext wird in `wiki_information.py` für jede
gematchte Wiki Seite ein API Call an das Minecraft Wiki ausgeführt, der den HTML-Code der
jeweiligen Seite zurückgibt und dieser anschließend als Text formatiert. Der Volltext beinhaltet
jedoch gegenüber der URL einen geringeren Informationsgehalt, da z.B. Bilder nicht dargestellt
werden können, was in bestimmten Fällen zu einer unvollständigen oder fehlerhaften Beantwortung
der Frage führen kann, und verhindert zudem bei einer zu hohen Token-Anzahl die ChatGPT-Request.
Die Verwendung der URL weist daher eine bessere Performance auf.

## Installation

Voraussetzungen:

* Docker (Docker Installation siehe <https://docs.docker.com/get-docker/>)
* Python 3.11 (Optional)

## Start des Backends als Docker-Container (empfohlen)

```bash
docker-compose up --build
```

Der Server lauscht standardmäßig auf Port **3000**.


## Lokaler Start ohne Docker 

```bash
# Auch benötigt zum Ausführen der Unittests
pip install -r requirements.txt
```

```bash
python app.py
```

## Test Nutzung

Für das Testen des Backens haben wir extra ein Python Skript `test_villager_response.py`angelegt. 
Nach dem Start des Backends über Docker, kann das Skript mit

```bash
./test_villager_response.py
```

ausgeführt werden. Es erscheint ein Eingabefeld, in welches Testnachrichten an den Dorfbewohner eingegeben werden können.
Im Terminal wird dann die jeweilige Antwort des Dorfbewohners ausgegeben.


## Tests

Es existieren Unit-Tests im Ordner tests für alle Bestandteile des Backends. Sie werden beim builden des Docker Images automatisch ausgeführt, können alternativ aber auch separat gestartet werden.

# Minecraft Mod Client (Forge-Mod)

Der Minecraft-Client-Mod befindet sich im Verzeichnis:

```
/client-dev-environment/

````

### Vorbereitung in IntelliJ IDEA

1. **Projekt öffnen**

   * Starten Sie IntelliJ IDEA.
   * Wählen Sie `File > Open` und öffnen Sie das Verzeichnis `client-dev-environment/`.

2. **Gradle-Projekt erkennen**

   * IntelliJ sollte die Datei `build.gradle` automatisch erkennen und das Projekt als Gradle-Projekt importieren.
   * Falls dies nicht automatisch geschieht, klicken Sie mit der rechten Maustaste auf `build.gradle` und wählen Sie `Import Gradle Project`.

3. **Run-Konfigurationen generieren**

   Öffnen Sie das Terminal innerhalb von IntelliJ und führen Sie im Projektverzeichnis folgenden Befehl aus:

   ```bash
   ./gradlew genIntellijRuns

> Dieser Befehl erzeugt die Run-Konfigurationen für Client und Server.

4. **Minecraft-Client starten**

   * Wählen Sie oben rechts im IntelliJ-Fenster im Dropdown-Menü die Run-Konfiguration `runClient` aus.
   * Klicken Sie anschließend auf den grünen Play-Button, um den Minecraft-Client im Entwicklungsmodus zu starten.

---

### OpenAI API-Key eintragen

Vor dem Start des Mods muss der Platzhalter `<OPEN_AI_API_KEY>` in der Datei
`src/main/java/com/nlp/villagerchat/VillagerChatMod.java` durch den tatsächlichen API-Schlüssel ersetzt werden.

```java
// Datei: VillagerChatMod.java (ca. Zeile 350)

private static final String OPENAI_API_KEY = "<OPEN_AI_API_KEY>";
```

Ersetzen Sie den Platzhalter durch Ihren gültigen OpenAI API-Key, beispielsweise:

```java
private static final String OPENAI_API_KEY = "sk-xxxxxx...";
```

Ohne diese Anpassung ist eine Kommunikation mit dem Backend nicht möglich.

---

### Erstellen des Mod-Builds

Zum Erzeugen des `.jar`-Artifacts führen Sie im Projektverzeichnis den folgenden Befehl aus:

```bash
./gradlew build
```

Das fertige `.jar`-File befindet sich anschließend im Verzeichnis:

```
client-dev-environment/build/libs/
```

Dieses `.jar` kann in den Minecraft-`mods/`-Ordner eingefügt werden.
