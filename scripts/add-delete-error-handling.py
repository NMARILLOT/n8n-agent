#!/usr/bin/env python3
"""
Ajouter des error handlers et debug au workflow delete_idea
"""

import json
from pathlib import Path

def add_error_handling():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # Modifier "Prepare Delete Idea" pour ajouter plus de debug
    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            new_code = """const requestedId = ($input.first().json.idea_id || '').trim();

console.log('[DELETE DEBUG] Requested ID:', requestedId);
console.log('[DELETE DEBUG] Input:', JSON.stringify($input.first().json));

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
            changes_made.append("✓ Ajouté logs de debug à 'Prepare Delete Idea'")

        # Modifier "Format Delete Response" pour gérer les erreurs
        elif node['name'] == 'Format Delete Response':
            new_code = """const input = $input.first().json;

console.log('[DELETE DEBUG] Format Response input:', JSON.stringify(input));

// Si erreur dans Prepare Delete Idea
if (input.error) {
  return [{ json: { response: input.response } }];
}

const ideaId = input.id || 'N/A';
const title = input.title || 'N/A';

const response = `✅ Idée archivée

⚠️ [${ideaId}] "${title}" a été archivée dans Notion.
(Note: L'API Notion ne permet pas la suppression définitive)`;

console.log('[DELETE DEBUG] Final response:', response);

return [{ json: { response } }];"""

            node['parameters']['jsCode'] = new_code
            changes_made.append("✓ Ajouté gestion d'erreur à 'Format Delete Response'")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 AJOUT D'ERROR HANDLING AU WORKFLOW delete_idea")
    print("=" * 80)
    print()

    changes = add_error_handling()

    print("Changements appliqués:")
    for change in changes:
        print(f"  {change}")

    print()
    print("Les logs apparaîtront dans la console n8n lors de l'exécution.")
    print()

if __name__ == "__main__":
    main()
