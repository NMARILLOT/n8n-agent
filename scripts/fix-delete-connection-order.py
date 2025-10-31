#!/usr/bin/env python3
"""
Fix delete_idea Connection Order
Le Switch pointe vers "Notion - Delete Idea" au lieu de "Prepare Delete Idea"
"""

import json
from pathlib import Path

def fix_connection_order():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []
    connections = workflow['connections']

    # Trouver les outputs du Switch Operation
    switch_outputs = connections.get('Switch Operation', {}).get('main', [])

    print("=" * 80)
    print("🔍 ANALYSE DU FLUX delete_idea")
    print("=" * 80)
    print()

    # Afficher tous les outputs du Switch
    operations = [
        'search_projects',
        'get_project_by_id',
        'list_categories',
        'create_project',
        'create_idea',
        'search_ideas',
        'get_idea_by_id',
        'update_idea',
        'delete_idea'
    ]

    print("Flux actuel depuis Switch Operation:")
    for i, output in enumerate(switch_outputs):
        if output:
            node_name = output[0]['node']
            operation = operations[i] if i < len(operations) else f"Output {i}"
            print(f"  {i}. {operation:20} → {node_name}")

    print()

    # Le output index 8 devrait être delete_idea
    delete_output_index = 8

    if len(switch_outputs) > delete_output_index and switch_outputs[delete_output_index]:
        current_target = switch_outputs[delete_output_index][0]['node']
        print(f"❌ Problème: delete_idea pointe vers '{current_target}'")
        print(f"✅ Solution: delete_idea doit pointer vers 'Prepare Delete Idea'")
        print()

        if current_target == "Notion - Delete Idea":
            # Corriger: pointer vers "Prepare Delete Idea" d'abord
            switch_outputs[delete_output_index] = [{
                "node": "Notion - Get Idea By ID",  # D'abord récupérer l'idée
                "type": "main",
                "index": 0
            }]

            changes_made.append("✓ Redirigé Switch → 'Notion - Get Idea By ID' pour delete_idea")

            # Ajouter une connexion de "Notion - Get Idea By ID" vers "Prepare Delete Idea"
            # MAIS "Notion - Get Idea By ID" est déjà utilisé par get_idea_by_id...

            # EN FAIT: il faut créer un nouveau node "Notion - Get Idea For Delete"
            # OU utiliser "Prepare Delete Idea" directement

            # Solution simple: faire pointer vers "Prepare Delete Idea" qui va chercher l'idée
            switch_outputs[delete_output_index] = [{
                "node": "Notion - Search Ideas",  # Chercher d'abord
                "type": "main",
                "index": 0
            }]

            changes_made.append("✓ Redirigé Switch → 'Notion - Search Ideas' pour delete_idea")

            # Ajouter une connexion de "Notion - Search Ideas" vers "Prepare Delete Idea"
            # PROBLÈME: "Notion - Search Ideas" est déjà utilisé et pointe vers "Format Search Ideas"

            # Meilleure solution: créer un node dédié
            # MAIS on ne peut pas créer de nodes facilement en script...

            # SOLUTION FINALE SIMPLE:
            # Pointer vers "Prepare Delete Idea" qui fera lui-même la recherche
            switch_outputs[delete_output_index] = [{
                "node": "Prepare Delete Idea",
                "type": "main",
                "index": 0
            }]

            changes_made.append("✓ Redirigé Switch → 'Prepare Delete Idea' pour delete_idea")

            # Mettre à jour le code de "Prepare Delete Idea" pour qu'il récupère l'idée lui-même
            for node in workflow['nodes']:
                if node['name'] == 'Prepare Delete Idea':
                    # PROBLÈME: on ne peut pas appeler Notion depuis un Code node...

                    # SOLUTION: utiliser le node "Notion - Delete Idea" pour CHERCHER d'abord
                    # puis le renommer en "Notion - Get Idea For Delete"
                    # puis créer un nouveau "Notion - Delete Idea" pour archiver

                    # C'est trop complexe...

                    # VRAIE SOLUTION: modifier le node "Notion - Delete Idea"
                    # pour qu'il fasse getAll AVANT d'archiver

                    pass

    # En fait, regardons comment "update_idea" fait:
    # Switch → "Notion - Update Idea" (getAll)
    # → "Prepare Update Idea"
    # → "Notion - Update Idea Page" (update)

    # Pour delete_idea, on devrait avoir:
    # Switch → "Notion - Get All Ideas For Delete" (getAll)
    # → "Prepare Delete Idea"
    # → "Notion - Delete Idea" (archive)

    # Le node "Notion - Delete Idea" devrait être renommé en "Notion - Get Ideas For Delete"
    # et son opération changée en "getAll" au lieu de "archive"

    for node in workflow['nodes']:
        if node['name'] == 'Notion - Delete Idea':
            print("Node 'Notion - Delete Idea' actuel:")
            print(f"  Operation: {node['parameters'].get('operation', 'N/A')}")
            print(f"  Position: {node['position']}")
            print()

            # Trouver un node "Notion - Update Idea" pour copier sa config
            update_node = next((n for n in workflow['nodes'] if n['name'] == 'Notion - Update Idea'), None)
            if update_node:
                print("Comparaison avec 'Notion - Update Idea':")
                print(f"  Operation: {update_node['parameters'].get('operation', 'N/A')}")
                print(f"  Resource: {update_node['parameters'].get('resource', 'N/A')}")
                print()

                # "Notion - Update Idea" utilise getAll pour récupérer toutes les idées
                # Puis "Prepare Update Idea" filtre pour trouver la bonne

                # On va faire pareil pour delete:
                # 1. Renommer "Notion - Delete Idea" en "Notion - Get Ideas For Delete"
                # 2. Changer son opération en getAll (comme Update)
                # 3. Créer un nouveau node "Notion - Archive Idea" qui archive

                node['name'] = 'Notion - Get Ideas For Delete'
                node['parameters'] = update_node['parameters'].copy()
                node['notes'] = '🔍 Récupère toutes les idées pour trouver celle à supprimer'

                changes_made.append("✓ Converti 'Notion - Delete Idea' → 'Notion - Get Ideas For Delete' (getAll)")

                # Créer un nouveau node pour archiver
                archive_node = {
                    "parameters": {
                        "operation": "archive",
                        "pageId": {
                            "__rl": True,
                            "mode": "id",
                            "value": "={{ $json.notion_page_id }}"
                        }
                    },
                    "type": "n8n-nodes-base.notion",
                    "typeVersion": 2.2,
                    "position": [
                        528,  # Après Prepare Delete Idea
                        1248
                    ],
                    "id": "archive_idea_new_node_id",
                    "name": "Notion - Archive Idea",
                    "credentials": node['credentials'],
                    "notes": "🗑️ Archive l'idée dans Notion (limitation API: pas de suppression définitive)"
                }

                workflow['nodes'].append(archive_node)
                changes_made.append("✓ Créé nouveau node 'Notion - Archive Idea'")

                # Mettre à jour les connexions
                # "Notion - Get Ideas For Delete" → "Prepare Delete Idea"
                connections['Notion - Get Ideas For Delete'] = {
                    "main": [[{
                        "node": "Prepare Delete Idea",
                        "type": "main",
                        "index": 0
                    }]]
                }

                # "Prepare Delete Idea" → "Notion - Archive Idea"
                connections['Prepare Delete Idea'] = {
                    "main": [[{
                        "node": "Notion - Archive Idea",
                        "type": "main",
                        "index": 0
                    }]]
                }

                # "Notion - Archive Idea" → "Format Delete Response"
                connections['Notion - Archive Idea'] = {
                    "main": [[{
                        "node": "Format Delete Response",
                        "type": "main",
                        "index": 0
                    }]]
                }

                changes_made.append("✓ Mis à jour toutes les connexions de la branche delete")

                # Supprimer l'ancienne connexion "Notion - Delete Idea"
                if 'Notion - Delete Idea' in connections:
                    del connections['Notion - Delete Idea']

                # Rediriger Switch vers "Notion - Get Ideas For Delete"
                switch_outputs[delete_output_index] = [{
                    "node": "Notion - Get Ideas For Delete",
                    "type": "main",
                    "index": 0
                }]

                changes_made.append("✓ Switch pointe maintenant vers 'Notion - Get Ideas For Delete'")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA CONNECTION ORDER")
    print("=" * 80)
    print()

    changes = fix_connection_order()

    print()
    print("=" * 80)
    print("📊 CHANGEMENTS APPLIQUÉS")
    print("=" * 80)
    for change in changes:
        print(f"  {change}")
    print()

if __name__ == "__main__":
    main()
