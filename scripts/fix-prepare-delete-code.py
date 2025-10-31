#!/usr/bin/env python3
"""
Fix Prepare Delete Idea Code
Doit lire 'Notion - Get Ideas For Delete' au lieu de 'Notion - Delete Idea'
"""

import json
from pathlib import Path

def fix_prepare_delete_code():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            old_code = node['parameters']['jsCode']

            print("=" * 80)
            print("Ancien code:")
            print("=" * 80)
            print(old_code)
            print()

            # Le code lit encore "Notion - Delete Idea"
            # Il doit lire "Notion - Get Ideas For Delete" maintenant
            new_code = """const requestedId = ($input.first().json.idea_id || '').trim();
const allIdeas = $('Notion - Get Ideas For Delete').all();

const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  return [{ json: { response: `Idée "${requestedId}" non trouvée.` } }];
}

const notionPageId = idea.json.id;
const title = idea.json.property_titre_de_l_id_e || '';

return [{
  json: {
    id: requestedId,
    notion_page_id: notionPageId,
    title: title
  }
}];"""

            node['parameters']['jsCode'] = new_code
            changes_made.append("✓ Corrigé 'Prepare Delete Idea' pour lire 'Notion - Get Ideas For Delete'")

            print("=" * 80)
            print("Nouveau code:")
            print("=" * 80)
            print(new_code)
            print()

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX PREPARE DELETE IDEA CODE")
    print("=" * 80)
    print()

    changes = fix_prepare_delete_code()

    print("=" * 80)
    print("CHANGEMENTS")
    print("=" * 80)
    for change in changes:
        print(f"  {change}")
    print()

if __name__ == "__main__":
    main()
