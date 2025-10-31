#!/usr/bin/env python3
"""
Fix delete_idea Missing Connection
Le node "Format Delete Response" ne retourne pas sa réponse → "workflow did not return a response"
"""

import json
from pathlib import Path

def analyze_and_fix():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print("=" * 80)
    print("🔍 ANALYSE DES CONNEXIONS")
    print("=" * 80)
    print()

    # Analyser les connexions actuelles
    connections = workflow.get('connections', {})

    # Branches qui fonctionnent
    print("✅ Branches qui fonctionnent:")
    working_branches = [
        'Format Search Projects',
        'Format Get Project By ID',
        'Format Search Ideas',
        'Format Get Idea',
        'Format Create Project Response',
        'Format Create Idea Response'
    ]

    for node_name in working_branches:
        if node_name in connections:
            print(f"  • {node_name} → {connections[node_name]}")
        else:
            print(f"  • {node_name} → PAS DE CONNEXION SORTANTE")

    print()
    print("❌ Branches cassées:")
    broken_branches = [
        'Format Delete Response',
        'Format Update Response'
    ]

    for node_name in broken_branches:
        if node_name in connections:
            print(f"  • {node_name} → {connections[node_name]}")
        else:
            print(f"  • {node_name} → ❌ PAS DE CONNEXION SORTANTE (BUG!)")

    print()
    print("=" * 80)
    print("🔧 CORRECTION")
    print("=" * 80)
    print()

    changes_made = []

    # En fait, dans n8n, les nodes "Format Response" ne retournent PAS directement au trigger
    # C'est le workflow qui retourne automatiquement la dernière sortie
    # Le problème est ailleurs...

    # Cherchons les IDs des nodes
    format_delete_id = None
    format_update_id = None
    prepare_delete_id = None

    for node in workflow['nodes']:
        if node['name'] == 'Format Delete Response':
            format_delete_id = node['id']
            print(f"Format Delete Response ID: {format_delete_id}")
        elif node['name'] == 'Format Update Response':
            format_update_id = node['id']
            print(f"Format Update Response ID: {format_update_id}")
        elif node['name'] == 'Prepare Delete Idea':
            prepare_delete_id = node['id']
            print(f"Prepare Delete Idea ID: {prepare_delete_id}")

    print()

    # Vérifier que "Prepare Delete Idea" récupère bien l'idée AVANT de la supprimer
    for node in workflow['nodes']:
        if node['name'] == 'Prepare Delete Idea':
            code = node['parameters'].get('jsCode', '')
            print("Code de 'Prepare Delete Idea':")
            print(code[:200] + "...")
            print()

            # Le problème : il cherche dans $('Notion - Delete Idea').all()
            # MAIS Notion - Delete Idea vient APRÈS, donc il n'y a pas encore de données!
            if "$('Notion - Delete Idea')" in code:
                print("❌ BUG TROUVÉ!")
                print("'Prepare Delete Idea' essaie de lire les données de 'Notion - Delete Idea'")
                print("MAIS 'Notion - Delete Idea' vient APRÈS dans le flux!")
                print()
                print("Solution: 'Prepare Delete Idea' doit d'abord CHERCHER l'idée,")
                print("PUIS 'Notion - Delete Idea' archive la page trouvée.")
                print()

                # Nouveau code qui cherche l'idée AVANT de la supprimer
                new_code = """const requestedId = $input.first().json.idea_id.trim();

// Chercher l'idée dans la database Notion
const searchNode = $('Notion - Search Ideas for Delete');
if (!searchNode || searchNode.all().length === 0) {
  return [{ json: {
    error: true,
    response: `Erreur: Impossible de trouver l'idée "${requestedId}"`
  } }];
}

const allIdeas = searchNode.all();
const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  return [{ json: {
    error: true,
    response: `Idée "${requestedId}" non trouvée.`
  } }];
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

                # Mais ATTENTION: il faut aussi ajouter un node "Notion - Search Ideas for Delete" AVANT
                # C'est trop complexe pour un simple fix automatique...

                print("⚠️  DIAGNOSTIC:")
                print("Le workflow a un problème d'ordre des opérations:")
                print()
                print("Flux actuel (CASSÉ):")
                print("  delete_idea tool")
                print("  → Switch Operation")
                print("  → Prepare Delete Idea (essaie de lire 'Notion - Delete Idea')")
                print("  → Notion - Delete Idea (archive)")
                print("  → Format Delete Response")
                print()
                print("Flux correct:")
                print("  delete_idea tool")
                print("  → Switch Operation")
                print("  → Notion - Search Ideas (cherche l'idée)")
                print("  → Prepare Delete Idea (prépare les données)")
                print("  → Notion - Delete Idea (archive)")
                print("  → Format Delete Response")
                print()

                changes_made.append("⚠️  Problème identifié: ordre des opérations incorrect")

    return changes_made

def main():
    print()
    changes = analyze_and_fix()
    print()
    print("=" * 80)
    print("📊 RÉSULTAT")
    print("=" * 80)
    for change in changes:
        print(f"  {change}")
    print()
    print("ℹ️  Ce bug nécessite une modification manuelle du workflow dans n8n")
    print("   Le script ne peut pas le corriger automatiquement.")
    print()

if __name__ == "__main__":
    main()
