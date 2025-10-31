#!/usr/bin/env python3
"""
Fix delete_idea Tool Parameters
Simplifier : seulement idea_id est requis, supprimer les autres paramètres
"""

import json
from pathlib import Path

def fix_delete_tool_params():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    for node in workflow['nodes']:
        if node['name'] == 'delete_idea':
            params = node['parameters']

            # Nouvelle description plus claire
            params['description'] = (
                "Archive une idée dans Notion par son ID. "
                "Format de l'ID: IDEA-XXXXXXXX. "
                "Note: L'API Notion archive les pages, elle ne les supprime pas définitivement."
            )

            # Simplifier workflowInputs : seulement idea_id
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
                        "required": True,  # SEUL paramètre requis
                        "defaultMatch": False,
                        "display": True,
                        "canBeUsedToMatch": True,
                        "type": "string",
                        "description": "ID de l'idée à archiver (format: IDEA-XXXXXXXX)"
                    }
                ],
                "attemptToConvertTypes": False,
                "convertFieldsToString": False
            }

            changes_made.append("✓ Simplifié delete_idea: seulement idea_id requis")
            changes_made.append("✓ Supprimé: operation, query, title, content, category")

    # Maintenant il faut aussi adapter le Switch pour lire correctement
    for node in workflow['nodes']:
        if node['name'] == 'Switch Operation':
            # Le Switch doit maintenant détecter que c'est delete_idea
            # basé sur le fait qu'il n'y a QUE idea_id (pas d'autres params)

            # OU on peut ajouter un paramètre __operation__ automatique
            # Laissons le Switch tel quel pour l'instant
            pass

    # Modifier Prepare Delete Idea pour lire directement idea_id
    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            new_code = """// Input simplifié: seulement idea_id
const input = $input.first().json;
const requestedId = (input.idea_id || '').trim();

console.log('[DELETE DEBUG] Input:', JSON.stringify(input));
console.log('[DELETE DEBUG] Requested ID:', requestedId);

if (!requestedId) {
  return [{ json: {
    response: '❌ Paramètre manquant.\\n\\nUtilisation: delete_idea(idea_id="IDEA-XXXXXXXX")',
    error: true
  } }];
}

const allIdeas = $('Notion - Get Ideas For Delete').all();
console.log('[DELETE DEBUG] Total ideas in DB:', allIdeas.length);

const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  const errorResponse = `❌ Idée "${requestedId}" non trouvée.\\n\\nVérifie l'ID avec search_ideas().`;
  console.log('[DELETE DEBUG]', errorResponse);
  return [{ json: { response: errorResponse, error: true } }];
}

const notionPageId = idea.json.id;
const title = idea.json.property_titre_de_l_id_e || 'Sans titre';

console.log('[DELETE DEBUG] Found:', { id: requestedId, page_id: notionPageId, title });

return [{
  json: {
    id: requestedId,
    notion_page_id: notionPageId,
    title: title
  }
}];"""

            node['parameters']['jsCode'] = new_code
            changes_made.append("✓ Prepare Delete Idea: lit directement idea_id")

    # Le Switch doit maintenant router différemment
    # Problème: comment savoir que c'est delete_idea si on n'a plus operation?
    # Solution: Le tool delete_idea appelle directement le workflow
    # Le workflow n'a PAS besoin du Switch pour delete_idea!

    # On va router DIRECTEMENT depuis le trigger MCP vers le workflow
    # Mais pour ça il faut que le tool delete_idea pointe vers le bon workflow

    # EN FAIT: le problème est que delete_idea utilise Execute Workflow Trigger
    # qui nécessite le Switch

    # Meilleure solution: garder un paramètre __operation__ caché
    for node in workflow['nodes']:
        if node['name'] == 'delete_idea':
            params = node['parameters']

            # Ajouter operation comme paramètre caché (non affiché à l'utilisateur)
            params['workflowInputs']['value']['__operation__'] = "delete_idea"
            params['workflowInputs']['schema'].append({
                "id": "__operation__",
                "displayName": "__operation__",
                "required": False,
                "defaultMatch": False,
                "display": False,  # Caché
                "canBeUsedToMatch": False,
                "type": "string"
            })

            changes_made.append("✓ Ajouté paramètre caché __operation__")

    # Modifier le Switch pour utiliser __operation__
    for node in workflow['nodes']:
        if node['name'] == 'Switch Operation':
            rules = node['parameters']['rules']['values']

            for rule in rules:
                if rule.get('outputKey') == 'delete_idea':
                    rule['conditions']['conditions'][0]['leftValue'] = "={{ $json.__operation__ }}"
                    rule['conditions']['conditions'][0]['rightValue'] = "delete_idea"
                    changes_made.append("✓ Switch: lit $json.__operation__")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA TOOL PARAMETERS")
    print("=" * 80)
    print()
    print("Problème:")
    print("  Trop de paramètres requis (operation, query, title, content, category)")
    print("  L'utilisateur doit juste donner l'ID!")
    print()
    print("Solution:")
    print("  ✅ Paramètre visible: idea_id (requis)")
    print("  ✅ Paramètre caché: __operation__ (pour le Switch)")
    print("  ✅ Suppression de tous les autres paramètres")
    print()

    changes = fix_delete_tool_params()

    print("Changements:")
    for change in changes:
        print(f"  {change}")
    print()
    print("=" * 80)
    print("Utilisation:")
    print("  delete_idea(idea_id=\"IDEA-XXXXXXXX\")")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
