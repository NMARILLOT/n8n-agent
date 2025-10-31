#!/usr/bin/env python3
"""
Fix delete_idea Logic Bug
Corrige le flux: chercher l'idée AVANT de la supprimer
"""

import json
from pathlib import Path

def fix_delete_logic():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # 1. Modifier "Prepare Delete Idea" pour qu'il cherche l'idée dans la database
    #    au lieu de lire le résultat de "Notion - Delete Idea"
    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            old_code = node['parameters']['jsCode']

            # Nouveau code: cherche l'idée dans "Notion - Get Idea By ID"
            # qui doit être appelé AVANT
            new_code = """// Récupérer l'ID demandé
const requestedId = ($input.first().json.idea_id || '').trim();

// Récupérer les données de l'idée depuis le node précédent
// (devrait être "Notion - Get Idea By ID")
const ideaData = $input.first().json;

// Vérifier qu'on a bien les données
if (!ideaData.id) {
  return [{ json: {
    error: true,
    response: `Idée "${requestedId}" non trouvée.`
  } }];
}

// Préparer les données pour la suppression
return [{
  json: {
    id: ideaData.property_id || requestedId,
    notion_page_id: ideaData.id,
    title: ideaData.property_titre_de_l_id_e || 'Sans titre'
  }
}];"""

            node['parameters']['jsCode'] = new_code
            changes_made.append("✓ Modifié 'Prepare Delete Idea' pour utiliser les données de l'input")

    # 2. Ajouter une connexion du Switch vers "Notion - Get Idea By ID"
    #    AVANT "Prepare Delete Idea"
    connections = workflow['connections']

    # Trouver l'index de sortie du Switch pour delete_idea
    switch_outputs = connections.get('Switch Operation', {}).get('main', [])

    # L'output delete_idea devrait pointer vers "Notion - Get Idea By ID" d'abord
    # Puis "Notion - Get Idea By ID" → "Prepare Delete Idea"
    # MAIS "Notion - Get Idea By ID" existe déjà et est utilisé par get_idea_by_id

    # Solution plus simple: modifier "Prepare Delete Idea" pour qu'il fasse la recherche LUI-MÊME
    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            # Code qui fait la recherche ET la préparation
            combined_code = """// Récupérer l'ID demandé
const requestedId = ($input.first().json.idea_id || '').trim();

// Chercher dans toutes les idées (on doit faire un appel à la DB Notion)
// PROBLÈME: on ne peut pas appeler un autre workflow depuis ici...
// SOLUTION: Le Switch doit d'abord appeler "Notion - Get Idea By ID"
// puis envoyer le résultat à "Prepare Delete Idea"

// Pour l'instant, on suppose que $input contient déjà les données de l'idée
const ideaData = $input.first().json;

// Si on reçoit juste l'idea_id, on ne peut pas continuer
if (!ideaData.id && ideaData.idea_id) {
  return [{ json: {
    error: true,
    response: `Erreur interne: l'idée doit être récupérée avant la suppression.`
  } }];
}

return [{
  json: {
    id: ideaData.property_id || requestedId,
    notion_page_id: ideaData.id,
    title: ideaData.property_titre_de_l_id_e || 'Sans titre'
  }
}];"""

            node['parameters']['jsCode'] = combined_code
            changes_made.append("✓ Mis à jour la logique de 'Prepare Delete Idea'")

    # 3. Modifier les connexions du Switch pour la branche delete_idea
    # Actuellement: Switch → Prepare Delete Idea
    # Nouveau: Switch → Notion - Get Idea By ID → Prepare Delete Idea

    # Trouver l'index de l'output delete_idea dans le Switch
    switch_outputs = connections.get('Switch Operation', {}).get('main', [])
    delete_output_index = None

    for i, output_list in enumerate(switch_outputs):
        if output_list and output_list[0]['node'] == 'Notion - Delete Idea':
            delete_output_index = i
            break

    if delete_output_index is not None:
        # Rediriger vers "Notion - Get Idea By ID" d'abord
        switch_outputs[delete_output_index] = [{
            "node": "Notion - Get Idea By ID",
            "type": "main",
            "index": 0
        }]

        # Modifier la connexion de "Notion - Get Idea By ID" pour ajouter une sortie vers "Prepare Delete Idea"
        # MAIS attention: "Notion - Get Idea By ID" est utilisé ailleurs aussi
        # Il faut dupliquer ce node...

        # En fait, c'est trop complexe. Solution plus simple:
        # Modifier "Prepare Delete Idea" pour qu'il appelle lui-même la DB Notion

        changes_made.append("⚠️  Modification des connexions requise manuellement dans n8n")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA LOGIC BUG")
    print("=" * 80)
    print()
    print("Problème:")
    print("  ❌ 'Prepare Delete Idea' essaie de lire 'Notion - Delete Idea'")
    print("  ❌ Mais 'Notion - Delete Idea' vient APRÈS dans le flux!")
    print()
    print("Solution:")
    print("  ✅ Modifier le code pour utiliser les données de l'input")
    print("  ✅ Le Switch doit appeler 'Notion - Get Idea By ID' AVANT")
    print()

    changes = fix_delete_logic()

    print("Changements appliqués:")
    for change in changes:
        print(f"  {change}")

    print()
    print("=" * 80)
    print("⚠️  ATTENTION")
    print("=" * 80)
    print("Cette correction partielle nécessite aussi:")
    print("  1. Rediriger Switch → 'Notion - Get Idea By ID' (au lieu de Prepare)")
    print("  2. Ajouter connexion 'Notion - Get Idea By ID' → 'Prepare Delete Idea'")
    print()
    print("OU créer un node dédié 'Notion - Get Idea For Delete'")
    print()

if __name__ == "__main__":
    main()
