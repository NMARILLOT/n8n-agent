#!/usr/bin/env python3
"""
Script pour obtenir votre Chat ID Telegram

Usage:
1. Envoyez /start à votre bot Telegram (@claude_code_nico_bot)
2. Exécutez ce script
3. Votre Chat ID s'affichera
"""

import requests
import json
import sys

# Token du bot
BOT_TOKEN = "8271481273:AAGbWO6JFwyQo7S10nyszmWt5R1fhaCWeG0"

def get_updates():
    """Récupère les dernières mises à jour du bot"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get('ok'):
            print(f"❌ Erreur API: {data.get('description')}")
            return None

        return data.get('result', [])

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def extract_chat_ids(updates):
    """Extrait tous les chat IDs uniques des mises à jour"""
    chat_ids = set()

    for update in updates:
        # Depuis un message
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            chat_type = update['message']['chat']['type']
            username = update['message']['from'].get('username', 'N/A')
            first_name = update['message']['from'].get('first_name', 'N/A')

            chat_ids.add((
                chat_id,
                chat_type,
                username,
                first_name
            ))

    return chat_ids

def main():
    print("🔍 Récupération de votre Chat ID Telegram...")
    print(f"📱 Bot: @claude_code_nico_bot")
    print()

    updates = get_updates()

    if updates is None:
        print("❌ Impossible de récupérer les mises à jour")
        sys.exit(1)

    if not updates:
        print("⚠️  Aucun message trouvé")
        print()
        print("💡 Instructions:")
        print("1. Ouvrez Telegram")
        print("2. Cherchez @claude_code_nico_bot")
        print("3. Envoyez /start")
        print("4. Relancez ce script")
        sys.exit(0)

    chat_ids = extract_chat_ids(updates)

    if not chat_ids:
        print("⚠️  Aucun Chat ID trouvé")
        sys.exit(0)

    print(f"✅ {len(chat_ids)} conversation(s) trouvée(s):\n")

    for chat_id, chat_type, username, first_name in sorted(chat_ids):
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"👤 Utilisateur: {first_name}")
        print(f"🔑 Username: @{username}")
        print(f"💬 Type: {chat_type}")
        print(f"🆔 Chat ID: {chat_id}")
        print()

        # Si c'est une conversation privée, c'est probablement Nicolas
        if chat_type == 'private':
            print(f"✅ Utilisez ce Chat ID dans le workflow:")
            print(f"   nicolasChatId = '{chat_id}';")
            print()

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

if __name__ == "__main__":
    main()
