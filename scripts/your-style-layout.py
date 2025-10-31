#!/usr/bin/env python3
"""
TON STYLE - Basé sur tes derniers changements
Compact horizontal, bien espacé vertical, sans sticky notes
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT MCP - TON STYLE RÉCUPÉRÉ
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [],  # Tu n'aimes pas les sticky notes
    "nodes": {
        # Basé sur tes positions actuelles que j'ai récupérées
        "MCP Server Trigger": [-1008, 256],

        # Les 9 tools - tu les as mis en colonne verticale
        "search_projects": [-1264, -368],
        "get_project_by_id": [-1264, -208],
        "list_categories": [-1264, -48],
        "create_project": [-1264, 112],
        "create_idea": [-1264, 272],
        "search_ideas": [-1264, 432],
        "get_idea_by_id": [-1264, 592],
        "update_idea": [-1264, 752],
        "delete_idea": [-1264, 912],

        # Backend processing - tu as organisé en branches horizontales
        "Execute Workflow Trigger": [-864, 256],
        "Switch Operation": [-672, 256],

        # Branches parallèles - ton organisation actuelle
        "Notion - Search Projects": [-416, -368],
        "Format Search Projects": [-176, -368],

        "Notion - Get Project By ID": [-416, -208],
        "Format Get Project By ID": [-176, -208],

        "List Categories": [-416, -48],

        "Notion - Search Ideas": [-416, 112],
        "Format Search Ideas": [-176, 112],

        "Notion - Get Idea By ID": [-416, 272],
        "Format Get Idea": [-176, 272],

        "Generate Project ID": [-416, 432],
        "Notion - Create Project": [-176, 432],
        "Format Create Project Response": [64, 432],

        "Generate Idea ID": [-416, 592],
        "Notion - Get Project For Idea": [-176, 592],
        "Find Project Page ID": [64, 592],
        "Notion - Create Idea1": [368, 592],
        "Format Create Idea Response": [624, 592],

        "Notion - Update Idea": [-416, 752],
        "Prepare Update Idea": [-176, 752],
        "Notion - Update Idea Page": [64, 752],
        "Format Update Response": [304, 752],

        "Notion - Delete Idea": [-416, 912],
        "Prepare Delete Idea": [-176, 912],
        "Format Delete Response": [64, 912],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [],  # Pas de sticky notes non plus
    "nodes": {
        # Tes positions actuelles pour Telegram
        "Telegram Trigger": [-600, 100],
        "Switch: Type d'entrée": [-400, 100],

        # Branche vocale
        "Get Audio File": [-200, -500],
        "Download Audio": [0, -500],
        "Transcribe Audio": [200, -500],
        "Format Audio Input": [400, -500],

        # Branche texte
        "Format Text Input": [-200, 500],

        # Merge
        "Merge Inputs": [600, 100],

        # Agent IA
        "Agent Dev Ideas": [1000, 100],
        "Claude Sonnet 4.5": [800, 400],
        "MCP Client - Projects": [1000, 400],
        "Simple Memory": [1200, 400],

        # Sortie
        "Format Markdown for Telegram": [1400, 100],
        "Send Telegram Response": [1600, 100],
    }
}

# ============================================================================
# APPLY - Exactement comme tu aimes
# ============================================================================

def apply_layout(workflow_path, layout_config, name):
    print(f"🎨 Application de ton style à: {name}")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Supprimer TOUTES les sticky notes (tu n'en veux pas)
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']

    # Repositionner les nodes selon ton style
    repositioned = 0
    not_found = []
    for node in workflow['nodes']:
        if node['name'] in layout_config["nodes"]:
            node['position'] = layout_config["nodes"][node['name']]
            repositioned += 1
        else:
            not_found.append(node['name'])

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"  ✅ {repositioned} nodes repositionnés selon ton style")
    if not_found:
        print(f"  ℹ️ Nodes non trouvés: {', '.join(not_found)}")

def main():
    print("=" * 80)
    print("🎯 TON STYLE - Intégration de tes préférences")
    print("=" * 80)
    print("\n✨ Caractéristiques de ton style:")
    print("  • Pas de sticky notes")
    print("  • Espacement horizontal compact (~150-240px)")
    print("  • Espacement vertical généreux (~160px)")
    print("  • Outils MCP en colonne verticale à gauche")
    print("  • Branches backend horizontales alignées")
    print("  • Flux gauche → droite très net")

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # MCP workflow
    mcp_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"
    if mcp_path.exists():
        apply_layout(mcp_path, MCP_LAYOUT, "MCP - Idée Dev Nico (Perso)")

    # Telegram workflow
    telegram_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    if telegram_path.exists():
        apply_layout(telegram_path, TELEGRAM_LAYOUT, "Agent Telegram - Dev Ideas")

    print("\n" + "=" * 80)
    print("✅ TON STYLE APPLIQUÉ - Exactement comme tu aimes!")
    print("=" * 80)

if __name__ == "__main__":
    main()