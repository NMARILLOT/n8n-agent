#!/usr/bin/env python3
"""
Fix delete_idea - Problème complet identifié
1. Input arrive dans query: {query: {operation, idea_id}}
2. operation est "delete" au lieu de "delete_idea"
"""

import json
from pathlib import Path

def fix_delete_complete():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # 1. Modifier le Switch pour lire dans query.operation
    for node in workflow['nodes']:
        if node['name'] == 'Switch Operation':
            rules = node['parameters']['rules']['values']

            # Trouver la règle delete_idea
            for i, rule in enumerate(rules):
                if rule.get('outputKey') == 'delete_idea':
                    # Modifier pour lire query.operation
                    old_value = rule['conditions']['conditions'][0]['leftValue']
                    rule['conditions']['conditions'][0]['leftValue'] = "={{ $json.query.operation }}"
                    # ET accepter "delete" comme valeur
                    rule['conditions']['conditions'][0]['rightValue'] = "delete"

                    changes_made.append(f"✓ Switch: {old_value} → $json.query.operation == 'delete'")

    # 2. Modifier Prepare Delete Idea pour lire query.idea_id
    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            new_code = """// Les données arrivent dans query object
const query = $input.first().json.query || $input.first().json;
const requestedId = (query.idea_id || '').trim();

console.log('[DELETE DEBUG] Full input:', JSON.stringify($input.first().json));
console.log('[DELETE DEBUG] Query object:', JSON.stringify(query));
console.log('[DELETE DEBUG] Requested ID:', requestedId);

if (!requestedId) {
  return [{ json: { response: '❌ ID manquant. Utilise: delete_idea(idea_id="IDEA-XXX")', error: true } }];
}

const allIdeas = $('Notion - Get Ideas For Delete').all();
console.log('[DELETE DEBUG] Total ideas found:', allIdeas.length);

const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  const errorResponse = `❌ Idée "${requestedId}" non trouvée dans la database.`;
  console.log('[DELETE DEBUG]', errorResponse);
  return [{ json: { response: errorResponse, error: true } }];
}

const notionPageId = idea.json.id;
const title = idea.json.property_titre_de_l_id_e || '';

console.log('[DELETE DEBUG] Found idea:', {
  id: requestedId,
  notion_page_id: notionPageId,
  title: title
});

return [{
  json: {
    id: requestedId,
    notion_page_id: notionPageId,
    title: title
  }
}];"""

            node['parameters']['jsCode'] = new_code
            changes_made.append("✓ Prepare Delete Idea: lit query.idea_id avec fallback")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA - CORRECTION COMPLÈTE")
    print("=" * 80)
    print()
    print("Problèmes identifiés:")
    print("  1. Input arrive dans: {query: {operation, idea_id}}")
    print("  2. Switch lit: $json.operation (devrait être $json.query.operation)")
    print("  3. operation est 'delete' (Switch attend 'delete_idea')")
    print()
    print("Corrections:")
    print("  ✅ Switch lit maintenant $json.query.operation")
    print("  ✅ Switch accepte 'delete' comme valeur")
    print("  ✅ Prepare Delete Idea lit query.idea_id")
    print()

    changes = fix_delete_complete()

    print("Changements appliqués:")
    for change in changes:
        print(f"  {change}")
    print()

if __name__ == "__main__":
    main()
