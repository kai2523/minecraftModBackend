#!/usr/bin/env python3
import requests
import json
import sys
import socket

HOST = "localhost"
PORT = 3000
URL = f"http://{HOST}:{PORT}/chat"
API_KEY = "4luUOspevcoogFBMggw0aiCsVjeZWd1KS50e2C5upj5wSmrgeG0OY3sIlMZLfJHK79PNO5eXarQfvP5h9svp2nyJmo5Y175PzFayyOnZSUcgWYNHlpQlsPM5ljloQui7"

CONTEXT = [
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

def check_backend(host, port):
    try:
        with socket.create_connection((host, port), timeout=2):
            return True
    except OSError:
        return False

def main():
    if not check_backend(HOST, PORT):
        print(f"ERROR: Backend auf {HOST}:{PORT} scheint nicht erreichbar zu sein.")
        print("Bitte stelle sicher, dass der Docker-Container läuft und auf Port 3000 lauscht.")
        sys.exit(1)

    print("CLI für Minecraft-Backend")
    print("Tippe eine Nachricht und drücke ENTER. Mit Strg+C beenden.")
    print("")

    while True:
        try:
            message = input("Nachricht: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBeendet.")
            break

        if not message:
            continue

        payload = {
            "message": message,
            "context": CONTEXT
        }

        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY
        }

        try:
            response = requests.post(URL, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            reply = data.get("reply", "(keine Antwort)")
        except requests.RequestException as e:
            reply = f"Fehler bei der Anfrage: {e}"
        except json.JSONDecodeError:
            reply = "Ungültige Antwort vom Server."

        print("\nAntwort:")
        print(reply)
        print("")

if __name__ == "__main__":
    main()