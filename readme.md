Änderungen pullen:
git pull https://github.com/kai2523/minecraftModBackend.git

Änderungen pushen:
git add . 
git commit -m "Kommentar zur Änderung"
git push

Dev-Server lokal starten:
npm run dev

Dev-Server stoppen:
Str + C

Test-Nachricht an lokalen Dev-Server:

curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -H "api-key: 4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7" \
  -d '{ 
        "message": "was hast du so im Angebot?", 
        "context": [
          "villager_level: Anfänger",
          "villager_profession: toolsmith",
          "villager_distance_to_player: 1.9 blocks",
          "trade: 1x Emerald → 1x Stone Shovel",
          "trade: 1x Emerald → 1x Stone Axe",
          "time_of_day: 11:15 (Mittag)",
          "day_count: Day 0",
          "is_daytime: true",
          "is_raining: false",
          "is_thundering: false",
          "dimension: minecraft:overworld",
          "biome: minecraft:plains"
        ]
     }'



Weitere Testnachricht an lokalen Dev-Server mit anderem Kontext:

curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -H "api-key: 4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7" \
  -d '{
    "message": "Wie crafte ich eine Diamantspitzhacke?",
    "context": [
      "villager_level: Anfänger",
      "villager_profession: shepherd",
      "villager_distance_to_player: 3.5 blocks",
      "trade: 2x Emerald → 1x Shears",
      "trade: 18x Gray Wool → 1x Emerald",
      "world_time: 1937",
      "time_of_day: 07:56 (Vormittag)",
      "day_count: Day 0",
      "is_daytime: true",
      "is_raining: false",
      "is_thundering: false",
      "dimension: minecraft:overworld",
      "biome: minecraft:plains"
    ]
  }'


Weitere Testnachricht an lokalen Dev-Server mit anderem Kontext:

curl -X POST http://localhost:3000/chat \
  -H "Content-Type: application/json" \
  -H "api-key: 4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7" \
  -d '{
    "message": "wie weit bin ich von dir weg?",
    "context": [
      "villager_level: Anfänger",
      "villager_profession: shepherd",
      "villager_distance_to_player: 3.5 blocks",
      "trade: 2x Emerald → 1x Shears",
      "trade: 18x Gray Wool → 1x Emerald",
      "world_time: 1665",
      "time_of_day: 07:39 (Vormittag)",
      "day_count: Day 0",
      "is_daytime: true",
      "is_raining: false",
      "is_thundering: false",
      "dimension: minecraft:overworld",
      "biome: minecraft:plains"
    ]
  }'


----------------------------------------------------------------

Nachricht an richtigen Backend-Server:

curl -X POST https://minecraftmodbackend-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -H "api-key: 4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7" \
  -d '{
    "message": "was hast du so im Angebot?",
    "context": [
      "villager_level: Anfänger",
      "villager_profession: toolsmith",
      "villager_distance_to_player: 1.9 blocks",
      "trade: 1x Emerald → 1x Stone Shovel",
      "trade: 1x Emerald → 1x Stone Axe",
      "time_of_day: 11:15 (Mittag)",
      "day_count: Day 0",
      "is_daytime: true",
      "is_raining: false",
      "is_thundering: false",
      "dimension: minecraft:overworld",
      "biome: minecraft:plains"
    ]
  }'


Weitere Nachricht an richtigen Backend-Server mit anderem Kontext:
curl -X POST https://minecraftmodbackend-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -H "api-key: 4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7" \
  -d '{
    "message": "welche Tageszeit ist es?",
    "context": [
      "villager_level: Anfänger",
      "villager_profession: shepherd",
      "villager_distance_to_player: 3.5 blocks",
      "trade: 2x Emerald → 1x Shears",
      "trade: 18x Gray Wool → 1x Emerald",
      "world_time: 1937",
      "time_of_day: 07:56 (Vormittag)",
      "day_count: Day 0",
      "is_daytime: true",
      "is_raining: false",
      "is_thundering: false",
      "dimension: minecraft:overworld",
      "biome: minecraft:plains"
    ]
  }'



Weitere Nachricht richtigen Backend-Server mit anderem Kontext:

curl -X POST https://minecraftmodbackend-production.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -H "api-key: 4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7" \
  -d '{
    "message": "wie weit bin ich von dir weg?",
    "context": [
      "villager_level: Anfänger",
      "villager_profession: shepherd",
      "villager_distance_to_player: 3.5 blocks",
      "trade: 2x Emerald → 1x Shears",
      "trade: 18x Gray Wool → 1x Emerald",
      "world_time: 1665",
      "time_of_day: 07:39 (Vormittag)",
      "day_count: Day 0",
      "is_daytime: true",
      "is_raining: false",
      "is_thundering: false",
      "dimension: minecraft:overworld",
      "biome: minecraft:plains"
    ]
  }'

Das MinecraftModBackend beinhaltet einen Chatbot, der es Minecraft Spielern ermöglicht mit
einem beliebigen Villager zu kommunizieren. Der Spieler kann über den Chat Informationen
zu einem Villager selbst oder zu verschiedensten Spielinhalten erfragen, die ihm der
Villager beantwortet.

Beschreibung Mod

Das Python Backend gibt die Frage des Spielers an question_key_words weiter.py, in der aus
der Frage relevante Schlüsselwörter extrahiert werden.

Beschreibung Key Words

Anhand der Schlüsselwörter aus der Frage werden in key_words_matching.py die zur Beantwortung
der Frage benötigten Minecraft Wiki Seiten bestimmt. Die Grundlage hierfür bildet das
matching_dict.json, das in matching_dict.py über API-Calls an die Minecraft Wiki API erstellt
wurde. Es enthält die Titel aller verfügbaren Minecraft Wiki Seiten sowie deren Redirects und
deren URL. matching_dict.py prüft für jedes Key Word, ob dieses mit einem Seitentitel oder einem
Redirect auf eine Seite übereinstimmt, wobei es Schreibfehler mit einer Levenshtein-Distanz von 1
berücksichtigt. Eine höhere Levenshtein-Distanz als 1 würde in vielen Fällen zu einem Matching
mit ungewollten Seiten führen.

Die gematchten Wiki Seiten können im weiteren Verlauf entweder in Form der URL oder als Volltext
in der ChatGPT-Request übergeben werden. Für den Volltext wird in wiki_information.py für jede
gematchte Wiki Seite ein API Call an das Minecraft Wiki ausgeführt, der den HTML-Code der jeweiligen
Seite zurückgibt und dieser anschließend als Text formatiert. Der Volltext beinhaltet jedoch
gegenüber der URL einen geringeren Informationsgehalt, da z.B. Bilder nicht dargestellt werden
können, was in bestimmten Fällen zu einer unvollständigen oder fehlerhaften Beantwortung der Frage
führen kann, und verhindert zudem bei einer zu hohen Token-Anzahl die ChatGPT-Request. Die
Verwendung der URL weist daher eine bessere Performance auf.

Beschreibung Sentiment Analyse

Beschreibung ChatGPT-Request