#!/usr/bin/env python3
"""
Script pour améliorer la présentation visuelle du workflow Agent Telegram
- Réorganise les positions sur une grille propre
- Ajoute des sticky notes explicatives
- Aligne les nodes correctement
"""

import json
from pathlib import Path

# Configuration de la grille
GRID = 200
START_X = -400
START_Y = 0

# Charger le workflow
script_dir = Path(__file__).parent
project_root = script_dir.parent
workflow_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"

with open(workflow_path, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

print("🎨 Amélioration de la présentation visuelle du workflow...")
print()

# === STICKY NOTES ===
sticky_notes = [
    {
        "id": "sticky_start",
        "type": "n8n-nodes-base.stickyNote",
        "position": [START_X - 200, START_Y - 400],
        "parameters": {
            "content": "## 🚀 DÉBUT DU WORKFLOW\n\n**Ce que fait ce workflow :**\n\nCapture les idées depuis Telegram.\nSupporte le texte ET la voix.\n\n✅ Message texte → Traité directement\n✅ Message vocal → Transcrit puis traité",
            "height": 280,
            "width": 400,
            "color": 4
        },
        "name": "Sticky Note - Début"
    },
    {
        "id": "sticky_switch",
        "type": "n8n-nodes-base.stickyNote",
        "position": [START_X + 400, START_Y - 500],
        "parameters": {
            "content": "## 🔀 CHOIX DU TYPE\n\n**Comment ça marche :**\n\nLe Switch regarde le message Telegram.\n\n✅ Si vocal → Va en haut\n✅ Si texte → Va en bas\n\n⚠️ Une seule branche s'exécute !",
            "height": 260,
            "width": 350,
            "color": 5
        },
        "name": "Sticky Note - Switch"
    },
    {
        "id": "sticky_agent",
        "type": "n8n-nodes-base.stickyNote",
        "position": [START_X + 1400, START_Y - 400],
        "parameters": {
            "content": "## 🤖 AGENT IA\n\n**Ce que fait Claude :**\n\nAnalyse ton idée.\nCherche des projets similaires.\nCrée ou ajoute à Notion.\n\n✅ Tout automatique !",
            "height": 240,
            "width": 350,
            "color": 6
        },
        "name": "Sticky Note - Agent"
    }
]

# Trouver et supprimer les anciennes sticky notes
workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']
print("  🗑️  Anciennes sticky notes supprimées")

# Ajouter les nouvelles sticky notes
for sticky in sticky_notes:
    workflow['nodes'].append(sticky)
    print(f"  ✅ Ajout: {sticky['name']}")

# === REPOSITIONNEMENT DES NODES ===
print("\n📐 Repositionnement des nodes sur la grille...")

# Définir les positions propres
positions = {
    "Telegram Trigger": [START_X, START_Y],
    "Switch: Type d'entrée": [START_X + 400, START_Y],

    # Branche vocale (en haut)
    "Get Audio File": [START_X + 600, START_Y - 300],
    "Download Audio": [START_X + 800, START_Y - 300],
    "Transcribe Audio": [START_X + 1000, START_Y - 300],
    "Format Audio Input": [START_X + 1200, START_Y - 300],

    # Branche texte (en bas)
    "Format Text Input": [START_X + 600, START_Y + 300],

    # Suite commune
    "Agent Dev Ideas": [START_X + 1400, START_Y],
    "Claude Sonnet 4.5": [START_X + 1400, START_Y + 240],
    "MCP Client - Projects": [START_X + 1600, START_Y + 240],
    "Simple Memory": [START_X + 1500, START_Y + 240],
    "Format Markdown for Telegram": [START_X + 1800, START_Y],
    "Send Telegram Response": [START_X + 2000, START_Y]
}

# Appliquer les positions
for node in workflow['nodes']:
    node_name = node['name']
    if node_name in positions:
        old_pos = node['position']
        new_pos = positions[node_name]
        node['position'] = new_pos
        print(f"  ✅ {node_name}: {old_pos} → {new_pos}")

# Sauvegarder
with open(workflow_path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"\n✨ Workflow réorganisé avec succès!")
print(f"📁 Fichier: {workflow_path}")
print()
print("📊 Résumé des améliorations:")
print(f"  - {len(sticky_notes)} sticky notes ajoutées")
print(f"  - {len(positions)} nodes repositionnés")
print()
print("🎯 Prochaines étapes:")
print("  1. Ouvre le workflow dans n8n pour vérifier visuellement")
print("  2. Ajuste manuellement si besoin (positions fines)")
print("  3. Déploie avec ./scripts/deploy.sh")
