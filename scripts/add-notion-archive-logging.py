#!/usr/bin/env python3
"""
Add Logging to Notion Archive Process
Pour comprendre pourquoi Notion - Archive Idea ne fonctionne pas
"""

import json
from pathlib import Path

def add_archive_logging():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # Ajouter un node Code AVANT Notion - Archive Idea pour logger l'input
    log_before_id = "log_before_archive_debug"

    log_before_node = {
        "parameters": {
            "jsCode": """const input = $input.first().json;

console.log('==============================================');
console.log('[ARCHIVE DEBUG] Input to Notion - Archive Idea:');
console.log(JSON.stringify(input, null, 2));
console.log('notion_page_id:', input.notion_page_id);
console.log('Type:', typeof input.notion_page_id);
console.log('==============================================');

// Passer l'input tel quel
return [$input.first()];"""
        },
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [636, 1248],
        "id": log_before_id,
        "name": "Log Before Archive",
        "notes": "🔍 Debug logging avant archivage Notion"
    }

    # Vérifier si le node existe déjà
    log_before_exists = any(n['name'] == 'Log Before Archive' for n in workflow['nodes'])

    if not log_before_exists:
        workflow['nodes'].append(log_before_node)
        changes_made.append("✓ Ajouté node 'Log Before Archive'")

    # Ajouter un node Code APRÈS Notion - Archive Idea pour logger le résultat
    log_after_id = "log_after_archive_debug"

    log_after_node = {
        "parameters": {
            "jsCode": """const input = $input.first();

console.log('==============================================');
console.log('[ARCHIVE DEBUG] Output from Notion - Archive Idea:');
console.log(JSON.stringify(input, null, 2));

// Vérifier si l'archivage a réussi
if (input.json) {
  console.log('Archive SUCCESS - Notion returned data');
  console.log('Page archived:', input.json.archived || input.json.id);
} else {
  console.log('Archive FAILED - No json data returned');
}
console.log('==============================================');

// Récupérer les données de Prepare Delete Idea
const prepareData = $('Prepare Delete Idea').first().json;

// Passer les données originales pour Format Delete Response
return [{
  json: {
    id: prepareData.id,
    notion_page_id: prepareData.notion_page_id,
    title: prepareData.title,
    archive_success: !!input.json
  }
}];"""
        },
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [836, 1248],
        "id": log_after_id,
        "name": "Log After Archive",
        "notes": "🔍 Debug logging après archivage Notion"
    }

    # Vérifier si le node existe déjà
    log_after_exists = any(n['name'] == 'Log After Archive' for n in workflow['nodes'])

    if not log_after_exists:
        workflow['nodes'].append(log_after_node)
        changes_made.append("✓ Ajouté node 'Log After Archive'")

    # Modifier les connections pour insérer les nodes de logging
    connections = workflow['connections']

    # Prepare Delete Idea → Log Before Archive
    connections['Prepare Delete Idea'] = {
        "main": [[{
            "node": "Log Before Archive",
            "type": "main",
            "index": 0
        }]]
    }
    changes_made.append("✓ Prepare Delete Idea → Log Before Archive")

    # Log Before Archive → Notion - Archive Idea
    connections['Log Before Archive'] = {
        "main": [[{
            "node": "Notion - Archive Idea",
            "type": "main",
            "index": 0
        }]]
    }
    changes_made.append("✓ Log Before Archive → Notion - Archive Idea")

    # Notion - Archive Idea → Log After Archive
    connections['Notion - Archive Idea'] = {
        "main": [[{
            "node": "Log After Archive",
            "type": "main",
            "index": 0
        }]]
    }
    changes_made.append("✓ Notion - Archive Idea → Log After Archive")

    # Log After Archive → Format Delete Response
    connections['Log After Archive'] = {
        "main": [[{
            "node": "Format Delete Response",
            "type": "main",
            "index": 0
        }]]
    }
    changes_made.append("✓ Log After Archive → Format Delete Response")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔍 ADD NOTION ARCHIVE DEBUG LOGGING")
    print("=" * 80)
    print()
    print("Objectif:")
    print("  Ajouter des logs avant et après 'Notion - Archive Idea'")
    print("  pour voir exactement ce qui se passe")
    print()
    print("Logs ajoutés:")
    print("  1. AVANT archivage: notion_page_id reçu")
    print("  2. APRÈS archivage: résultat Notion API")
    print()

    changes = add_archive_logging()

    print("Changements:")
    for change in changes:
        print(f"  {change}")
    print()
    print("=" * 80)
    print("Nouveau flux:")
    print("  Prepare Delete Idea →")
    print("    → Log Before Archive (🔍 debug) →")
    print("      → Notion - Archive Idea →")
    print("        → Log After Archive (🔍 debug) →")
    print("          → Format Delete Response")
    print("=" * 80)
    print()
    print("Utilisation:")
    print("  1. Déployer: ./scripts/deploy.sh")
    print("  2. Appeler delete_idea(idea_id='IDEA-1FZFTW26')")
    print("  3. Consulter les logs n8n pour voir les [ARCHIVE DEBUG]")
    print()

if __name__ == "__main__":
    main()
