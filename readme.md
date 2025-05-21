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
