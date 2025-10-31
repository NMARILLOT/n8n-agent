#!/usr/bin/env python3
"""
Fix delete_idea - Force New Node
Supprimer l'ancien node et en créer un vraiment nouveau avec un nouvel ID
"""

import json
import uuid
from pathlib import Path

def fix_delete_force_new():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # 1. Supprimer complètement le node "Notion - Get Ideas For Delete"
    nodes_to_keep = []
    old_node_id = None

    for node in workflow['nodes']:
        if node['name'] == 'Notion - Get Ideas For Delete':
            old_node_id = node['id']
            print(f"Suppression de l'ancien node ID: {old_node_id}")
            changes_made.append(f"✓ Supprimé ancien node 'Notion - Get Ideas For Delete' (ID: {old_node_id})")
        else:
            nodes_to_keep.append(node)

    workflow['nodes'] = nodes_to_keep

    # 2. Créer un NOUVEAU node avec un nouvel ID, basé sur "Notion - Search Ideas"
    search_ideas_node = next((n for n in workflow['nodes'] if n['name'] == 'Notion - Search Ideas'), None)

    if search_ideas_node:
        new_node_id = str(uuid.uuid4()).replace('-', '')[:24]  # ID aléatoire comme n8n

        new_node = {
            "parameters": search_ideas_node['parameters'].copy(),  # Copier la config de Search Ideas
            "type": "n8n-nodes-base.notion",
            "typeVersion": 2.2,
            "position": [
                336,
                1248
            ],
            "id": new_node_id,  # NOUVEL ID
            "name": "Notion - Get Ideas For Delete",
            "credentials": search_ideas_node['credentials'],
            "notes": "🔍 Récupère TOUTES les idées pour trouver celle à supprimer (database des IDÉES)"
        }

        workflow['nodes'].append(new_node)
        changes_made.append(f"✓ Créé NOUVEAU node 'Notion - Get Ideas For Delete' (ID: {new_node_id})")

        print()
        print("Nouveau node créé:")
        print(f"  ID: {new_node_id}")
        print(f"  Database ID: {new_node['parameters']['databaseId']['value']}")
        print()

    # 3. Vérifier que le Switch pointe vers le bon node
    connections = workflow['connections']
    switch_outputs = connections.get('Switch Operation', {}).get('main', [])

    if len(switch_outputs) > 8:
        print("Connexion Switch Operation → Notion - Get Ideas For Delete:")
        print(f"  {switch_outputs[8]}")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA - FORCE NEW NODE")
    print("=" * 80)
    print()
    print("Problème:")
    print("  Le node 'Notion - Get Ideas For Delete' garde l'ancienne config")
    print("  même après modification, car l'ID est le même.")
    print()
    print("Solution:")
    print("  Supprimer complètement l'ancien node")
    print("  Créer un NOUVEAU node avec un nouvel ID")
    print("  Copier la config de 'Notion - Search Ideas' (qui fonctionne)")
    print()

    changes = fix_delete_force_new()

    print()
    print("=" * 80)
    print("CHANGEMENTS")
    print("=" * 80)
    for change in changes:
        print(f"  {change}")
    print()

if __name__ == "__main__":
    main()
