#!/usr/bin/env python3
"""
Fix delete_idea Schema Validation
Le schéma doit être compatible avec LangChain
"""

import json
from pathlib import Path

def fix_schema_validation():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    for node in workflow['nodes']:
        if node['name'] == 'delete_idea':
            params = node['parameters']

            # Schéma simple et compatible LangChain
            params['workflowInputs'] = {
                "mappingMode": "defineBelow",
                "value": {
                    "idea_id": "={{ $fromAI('idea_id', '', 'string') }}"
                },
                "matchingColumns": [],
                "schema": [
                    {
                        "id": "idea_id",
                        "displayName": "idea_id",
                        "required": True,  # Python boolean → JSON true
                        "defaultMatch": False,
                        "display": True,
                        "canBeUsedToMatch": True,
                        "type": "string"
                    }
                ],
                "attemptToConvertTypes": False,
                "convertFieldsToString": False
            }

            changes_made.append("✓ Schéma simplifié: idea_id uniquement")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA SCHEMA VALIDATION")
    print("=" * 80)
    print()
    print("Correction du schéma pour LangChain compatibility")
    print()

    changes = fix_schema_validation()

    for change in changes:
        print(f"  {change}")
    print()

if __name__ == "__main__":
    main()
