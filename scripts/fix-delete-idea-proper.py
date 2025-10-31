#!/usr/bin/env python3
"""
Fix delete_idea tool - Notion API only supports archiving, not true deletion
"""

import json
from pathlib import Path

def fix_delete_idea():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    for node in workflow['nodes']:
        # Fix delete_idea tool description
        if node['name'] == 'delete_idea':
            old_desc = node['parameters'].get('description', '')
            node['parameters']['description'] = (
                "Archive une idée dans Notion (équivalent à suppression). "
                "L'idée sera archivée et n'apparaîtra plus dans les recherches. "
                "Note: L'API Notion ne permet pas la suppression définitive, seulement l'archivage."
            )
            changes_made.append(f"✓ Mis à jour description de delete_idea")

        # Fix Notion Delete node notes
        elif node['name'] == 'Notion - Delete Idea':
            node['notes'] = (
                "⚠️ Archive l'idée dans Notion\n\n"
                "IMPORTANT: L'API Notion ne permet pas la suppression définitive.\n"
                "La page est archivée et n'apparaît plus dans les vues, mais existe toujours.\n"
                "C'est une limitation de Notion, pas du workflow."
            )
            # Vérifier que l'opération est bien 'archive'
            if node['parameters'].get('operation') == 'archive':
                changes_made.append(f"✓ Mis à jour notes de Notion - Delete Idea")
            else:
                print(f"⚠️  ATTENTION: opération est '{node['parameters'].get('operation')}', devrait être 'archive'")

        # Fix Format Delete Response
        elif node['name'] == 'Format Delete Response':
            # Vérifier le code
            code = node['parameters'].get('jsCode', '')
            if 'supprimée avec succès' in code or 'deleted successfully' in code:
                # Corriger le message
                new_code = code.replace(
                    'supprimée avec succès',
                    'archivée avec succès'
                ).replace(
                    'deleted successfully',
                    'archived successfully'
                )
                node['parameters']['jsCode'] = new_code
                changes_made.append(f"✓ Corrigé message dans Format Delete Response")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print("=" * 80)
    print("🔧 FIX DELETE_IDEA - Correction de la description")
    print("=" * 80)
    print()
    print("Problème identifié:")
    print("  ❌ Le tool dit 'suppression définitive' mais Notion archive seulement")
    print("  ❌ L'API Notion ne permet PAS la suppression définitive")
    print()
    print("Solution:")
    print("  ✅ Corriger la description pour dire 'archive'")
    print("  ✅ Expliquer la limitation de Notion")
    print("  ✅ Mettre à jour les messages de succès")
    print()

    changes = fix_delete_idea()

    print("Changements appliqués:")
    for change in changes:
        print(f"  {change}")

    if not changes:
        print("  ⚠️  Aucun changement nécessaire")

    print()
    print("=" * 80)
    print("✅ FIX APPLIQUÉ - Prêt à déployer")
    print("=" * 80)

if __name__ == "__main__":
    main()