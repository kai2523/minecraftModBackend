#!/usr/bin/env bash
#
# Einfache REPL, um Nachrichten an http://localhost:3000/chat zu schicken
if ! nc -z localhost 3000 2>/dev/null; then
  echo "ERROR: Backend auf localhost:3000 scheint nicht erreichbar zu sein."
  echo "Bitte stelle sicher, dass der Docker-Container läuft und auf Port 3000 lauscht."
  exit 1
fi

echo "CLI für Minecraft-Backend"
echo "Tippe eine Nachricht und drücke ENTER. Mit Strg+C beenden."
echo ""

while true; do
  # 1) Eingabe auslesen
  read -p "Nachricht: " MESSAGE

  # Wenn die Eingabe leer ist, überspringen
  if [ -z "$MESSAGE" ]; then
    continue
  fi

  # 2) Beispiel-Context (hier leer) – du kannst das anpassen oder festlegen
  #    Falls du einen Standard-Context definieren willst, baue ihn hier ein.
  CONTEXT_JSON='[
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
  ]'

  # 3) Die POST-Anfrage mit curl absenden
  RESPONSE=$(curl -s -X POST http://localhost:3000/chat \
    -H "Content-Type: application/json" \
    -H "api-key: 4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7" \
    -d "{
          \"message\": \"$MESSAGE\",
          \"context\": $CONTEXT_JSON
        }")

  # 4) Nur das Feld "reply" extrahieren und anzeigen (mit jq)
  echo ""
  echo "Antwort:"
  echo "$RESPONSE" | jq -r '.reply'
  echo ""
done
