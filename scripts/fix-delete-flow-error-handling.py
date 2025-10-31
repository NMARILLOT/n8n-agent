#!/usr/bin/env python3
"""
Fix delete_idea Error Flow
Problème: Le workflow continue vers Notion - Archive Idea même si Prepare Delete Idea retourne une erreur
Solution: Bypass Notion - Archive Idea en cas d'erreur et aller directement à Format Delete Response
"""

import json
from pathlib import Path

def fix_delete_error_flow():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # Solution: Ajouter un node IF après Prepare Delete Idea
    # pour router vers Format Delete Response si erreur

    # Trouver les IDs des nodes
    prepare_delete_id = None
    notion_archive_id = None
    format_response_id = None

    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            prepare_delete_id = node['id']
        elif node['name'] == 'Notion - Archive Idea':
            notion_archive_id = node['id']
        elif node['name'] == 'Format Delete Response':
            format_response_id = node['id']

    print(f"Prepare Delete ID: {prepare_delete_id}")
    print(f"Notion Archive ID: {notion_archive_id}")
    print(f"Format Response ID: {format_response_id}")

    # Créer un node IF pour gérer les erreurs
    if_node_id = "check_delete_error_node"

    if_node = {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict"
                },
                "conditions": [
                    {
                        "id": "error_check",
                        "leftValue": "={{ $json.error }}",
                        "rightValue": "true",
                        "operator": {
                            "type": "boolean",
                            "operation": "equals"
                        }
                    }
                ],
                "combinator": "and"
            },
            "options": {}
        },
        "type": "n8n-nodes-base.if",
        "typeVersion": 2,
        "position": [536, 1248],
        "id": if_node_id,
        "name": "Check Delete Error",
        "notes": "🔀 Route vers Format Response si erreur, sinon vers Notion Archive"
    }

    # Vérifier si le node IF existe déjà
    if_exists = any(n['name'] == 'Check Delete Error' for n in workflow['nodes'])

    if not if_exists:
        workflow['nodes'].append(if_node)
        changes_made.append("✓ Ajouté node IF 'Check Delete Error'")

    # Modifier les connections
    connections = workflow['connections']

    # Prepare Delete Idea → Check Delete Error
    connections['Prepare Delete Idea'] = {
        "main": [[{
            "node": "Check Delete Error",
            "type": "main",
            "index": 0
        }]]
    }
    changes_made.append("✓ Prepare Delete Idea → Check Delete Error")

    # Check Delete Error → deux sorties
    #   - Si erreur (true) → Format Delete Response
    #   - Si pas erreur (false) → Notion - Archive Idea
    connections['Check Delete Error'] = {
        "main": [
            [{
                "node": "Format Delete Response",
                "type": "main",
                "index": 0
            }],
            [{
                "node": "Notion - Archive Idea",
                "type": "main",
                "index": 0
            }]
        ]
    }
    changes_made.append("✓ Check Delete Error → Format (si erreur) | Archive (si OK)")

    # Notion - Archive Idea → Format Delete Response (inchangé)
    # Déjà connecté

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA ERROR FLOW")
    print("=" * 80)
    print()
    print("Problème:")
    print("  Le workflow continue vers 'Notion - Archive Idea' même si")
    print("  'Prepare Delete Idea' retourne {error: true}")
    print()
    print("Solution:")
    print("  Ajouter un node IF pour router:")
    print("  - Si error=true → Format Delete Response (skip archive)")
    print("  - Si error=false → Notion - Archive Idea → Format")
    print()

    changes = fix_delete_error_flow()

    print("Changements:")
    for change in changes:
        print(f"  {change}")
    print()
    print("=" * 80)
    print("Nouveau flux:")
    print("  Prepare Delete Idea →")
    print("    → Check Delete Error →")
    print("      ├─ [ERROR] → Format Delete Response")
    print("      └─ [OK] → Notion - Archive Idea → Format Delete Response")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
