#!/usr/bin/env python3
"""
Fix delete_idea Schema - Add __operation__ Parameter
Problème: GPT-4o envoie __operation__ mais il n'est pas dans le schema → validation error
Solution: Ajouter __operation__ au schema comme paramètre optionnel caché
"""

import json
from pathlib import Path

def fix_delete_schema():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    for node in workflow['nodes']:
        if node['name'] == 'delete_idea':
            params = node['parameters']
            schema = params['workflowInputs']['schema']

            # Vérifier si __operation__ existe déjà dans le schema
            has_operation = any(p['id'] == '__operation__' for p in schema)

            if not has_operation:
                # Ajouter __operation__ au schema
                schema.append({
                    "id": "__operation__",
                    "displayName": "__operation__",
                    "required": False,  # Pas requis car hardcodé
                    "defaultMatch": False,
                    "display": False,   # Caché à l'utilisateur
                    "canBeUsedToMatch": False,
                    "type": "string",
                    "description": "Internal routing parameter (auto-filled)"
                })
                changes_made.append("✓ Ajouté __operation__ au schema (optionnel, caché)")
            else:
                changes_made.append("⚠️  __operation__ déjà dans le schema")

            # Vérifier aussi qu'il est bien hardcodé dans value
            value = params['workflowInputs']['value']
            if '__operation__' not in value:
                value['__operation__'] = 'delete_idea'
                changes_made.append("✓ Ajouté __operation__ hardcodé dans value")

            break

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA SCHEMA - ADD __operation__ PARAMETER")
    print("=" * 80)
    print()
    print("Problème:")
    print("  'Received tool input did not match expected schema'")
    print("  → GPT-4o envoie __operation__ mais il n'est pas dans le schema")
    print("  → LangChain rejette les paramètres non déclarés")
    print()
    print("Solution:")
    print("  Ajouter __operation__ au schema comme paramètre optionnel caché")
    print("  Le garder hardcodé à 'delete_idea' dans value")
    print()

    changes = fix_delete_schema()

    print("Changements:")
    for change in changes:
        print(f"  {change}")
    print()
    print("=" * 80)
    print("Schema final:")
    print("  1. idea_id (required, visible)")
    print("  2. __operation__ (optional, hidden, hardcoded)")
    print()
    print("GPT-4o peut maintenant:")
    print("  - Envoyer seulement idea_id (requis)")
    print("  - Ou envoyer idea_id + __operation__ (tous deux acceptés)")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
