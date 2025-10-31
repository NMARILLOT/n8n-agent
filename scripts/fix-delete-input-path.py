#!/usr/bin/env python3
"""
Fix delete_idea Input Path
Les données arrivent dans $input.json.query au lieu de $input.json directement
"""

import json
from pathlib import Path

def fix_input_path():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # Modifier "Prepare Delete Idea" pour lire dans query
    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            new_code = """// Les données arrivent dans query object
const input = $input.first().json;
const requestedId = (input.query?.idea_id || input.idea_id || '').trim();

console.log('[DELETE DEBUG] Full input:', JSON.stringify(input));
console.log('[DELETE DEBUG] Requested ID:', requestedId);

const allIdeas = $('Notion - Get Ideas For Delete').all();
console.log('[DELETE DEBUG] Total ideas found:', allIdeas.length);

const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  const errorResponse = `❌ Idée "${requestedId}" non trouvée.`;
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
            changes_made.append("✓ Corrigé path d'input: query?.idea_id || idea_id")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA INPUT PATH")
    print("=" * 80)
    print()
    print("Problème:")
    print("  Les données arrivent dans: $input.json.query.idea_id")
    print("  Au lieu de: $input.json.idea_id")
    print()
    print("Solution:")
    print("  Lire input.query?.idea_id || input.idea_id (fallback)")
    print()

    changes = fix_input_path()

    print("Changements:")
    for change in changes:
        print(f"  {change}")
    print()

if __name__ == "__main__":
    main()
