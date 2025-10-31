#!/usr/bin/env python3
"""
Script pour corriger l'outil delete_idea dans le workflow MCP
Le node Notion fait actuellement un getAll au lieu d'un delete
"""

import json
from pathlib import Path

# Charger le workflow
script_dir = Path(__file__).parent
project_root = script_dir.parent
workflow_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"

with open(workflow_path, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

print("🔧 Correction du node Notion - Delete Idea...")

# Trouver les nodes concernés
notion_delete_node = next((n for n in workflow['nodes'] if n['name'] == 'Notion - Delete Idea'), None)
format_delete_node = next((n for n in workflow['nodes'] if n['name'] == 'Prepare Delete Idea'), None)

if not notion_delete_node:
    print("❌ Node 'Notion - Delete Idea' non trouvé")
    exit(1)

if not format_delete_node:
    print("❌ Node 'Prepare Delete Idea' non trouvé")
    exit(1)

print(f"  📍 Notion Delete Node ID: {notion_delete_node['id']}")
print(f"  📍 Format Delete Node ID: {format_delete_node['id']}")

# Corriger le node Notion Delete pour faire une vraie suppression
notion_delete_node['parameters'] = {
    "resource": "page",
    "operation": "archive",
    "pageId": {
        "__rl": True,
        "mode": "id",
        "value": "={{ $json.notion_page_id }}"
    }
}

print("  ✅ Node Notion corrigé: page.archive avec notion_page_id")

# Créer un nouveau node Code pour formater la réponse finale
format_response_id = "format_delete_response_" + notion_delete_node['id'][:12]
format_response_node = {
    "parameters": {
        "jsCode": """const ideaId = $input.first().json.id || 'N/A';
const title = $input.first().json.title || 'N/A';

const response = `✅ Idée supprimée

⚠️ [${ideaId}] "${title}" a été supprimée définitivement de Notion.`;

return [{ json: { response } }];"""
    },
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [496, 1280],
    "id": format_response_id,
    "name": "Format Delete Response",
    "notes": "✅ Formate la confirmation de suppression"
}

# Vérifier si le node existe déjà
existing_format_response = next((n for n in workflow['nodes'] if n['name'] == 'Format Delete Response'), None)
if not existing_format_response:
    workflow['nodes'].append(format_response_node)
    print("  ✅ Node 'Format Delete Response' créé")
else:
    # Mettre à jour l'existant
    existing_format_response['parameters'] = format_response_node['parameters']
    format_response_id = existing_format_response['id']
    print("  ✅ Node 'Format Delete Response' mis à jour")

# Vérifier les connexions
if 'connections' not in workflow:
    workflow['connections'] = {}

# Connexion: Prepare Delete Idea → Notion - Delete Idea
format_delete_name = format_delete_node['name']
if format_delete_name not in workflow['connections']:
    workflow['connections'][format_delete_name] = {"main": [[]]}

workflow['connections'][format_delete_name]['main'][0] = [
    {
        "node": notion_delete_node['name'],
        "type": "main",
        "index": 0
    }
]
print(f"  ✅ Connexion: {format_delete_name} → Notion - Delete Idea")

# Connexion: Notion - Delete Idea → Format Delete Response
notion_delete_name = notion_delete_node['name']
if notion_delete_name not in workflow['connections']:
    workflow['connections'][notion_delete_name] = {"main": [[]]}

workflow['connections'][notion_delete_name]['main'][0] = [
    {
        "node": "Format Delete Response",
        "type": "main",
        "index": 0
    }
]
print(f"  ✅ Connexion: Notion - Delete Idea → Format Delete Response")

# Sauvegarder
with open(workflow_path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"\n✨ Workflow corrigé et sauvegardé!")
print(f"📁 Fichier: {workflow_path}")
