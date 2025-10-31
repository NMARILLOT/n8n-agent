#!/usr/bin/env python3
"""
FINAL CLEAN LAYOUT - Sans sticky notes, flux compact horizontal, outils MCP en bas
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT MCP - SANS STICKY NOTES, OUTILS EN BAS DU TRIGGER
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [],  # PAS DE STICKY NOTES
    "nodes": {
        # COLONNE 1: Trigger en haut (X = -600)
        "MCP Server Trigger": [-600, -800],

        # COLONNE 2: Tools EN BAS du trigger (X = -600, Y positifs, espacement de 200px)
        "search_projects": [-600, -400],
        "get_project_by_id": [-600, -200],
        "list_categories": [-600, 0],
        "create_project": [-600, 200],
        "create_idea": [-600, 400],
        "search_ideas": [-600, 600],
        "get_idea_by_id": [-600, 800],
        "update_idea": [-600, 1000],
        "delete_idea": [-600, 1200],

        # COLONNE 3: Backend trigger et switch (X = -200 et 0)
        "Execute Workflow Trigger": [-200, 300],
        "Switch Operation": [0, 300],

        # BRANCHES PARALLÈLES (espacement horizontal réduit à 200px)

        # Branche 1: Search Projects (Y = -1000)
        "Notion - Search Projects": [200, -1000],
        "Format Search Projects": [400, -1000],

        # Branche 2: Get Project By ID (Y = -800)
        "Notion - Get Project By ID": [200, -800],
        "Format Get Project By ID": [400, -800],

        # Branche 3: List Categories (Y = -600)
        "List Categories": [200, -600],

        # Branche 4: Search Ideas (Y = -400)
        "Notion - Search Ideas": [200, -400],
        "Format Search Ideas": [400, -400],

        # Branche 5: Get Idea By ID (Y = -200)
        "Notion - Get Idea By ID": [200, -200],
        "Format Get Idea": [400, -200],

        # Branche 6: Create Project (Y = 0)
        "Generate Project ID": [200, 0],
        "Notion - Create Project": [400, 0],
        "Format Create Project Response": [600, 0],

        # Branche 7: Create Idea (Y = 200)
        "Generate Idea ID": [200, 200],
        "Notion - Get Project For Idea": [400, 200],
        "Find Project Page ID": [600, 200],
        "Notion - Create Idea1": [800, 200],
        "Format Create Idea Response": [1000, 200],

        # Branche 8: Update Idea (Y = 400)
        "Notion - Update Idea": [200, 400],
        "Prepare Update Idea": [400, 400],
        "Notion - Update Idea Page": [600, 400],
        "Format Update Response": [800, 400],

        # Branche 9: Delete Idea (Y = 600)
        "Notion - Delete Idea": [200, 600],
        "Prepare Delete Idea": [400, 600],
        "Format Delete Response": [600, 600],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [],  # PAS DE STICKY NOTES
    "nodes": {
        # COLONNE 1: Entrée (X = -600)
        "Telegram Trigger": [-600, 100],

        # COLONNE 2: Switch (X = -400)
        "Switch: Type d'entrée": [-400, 100],

        # BRANCHE HAUTE: Traitement vocal (Y = -500, espacement horizontal de 200px)
        "Get Audio File": [-200, -500],
        "Download Audio": [0, -500],
        "Transcribe Audio": [200, -500],
        "Format Audio Input": [400, -500],

        # BRANCHE BASSE: Traitement texte (Y = 500)
        "Format Text Input": [-200, 500],

        # COLONNE 3: Merge (X = 600)
        "Merge Inputs": [600, 100],

        # COLONNE 4: Agent IA (X = 800-1200, distribution verticale)
        "Agent Dev Ideas": [1000, 100],
        "Claude Sonnet 4.5": [800, 400],
        "MCP Client - Projects": [1000, 400],
        "Simple Memory": [1200, 400],

        # COLONNE 5: Sortie (X = 1400-1600)
        "Format Markdown for Telegram": [1400, 100],
        "Send Telegram Response": [1600, 100],
    }
}

# ============================================================================
# APPLY
# ============================================================================

def apply_layout(workflow_path, layout_config, name):
    print(f"🎨 Applying final clean layout to: {name}")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Clear ALL sticky notes (important!)
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']

    # Add sticky notes if any (but we have none now)
    for sticky in layout_config["sticky_notes"]:
        workflow['nodes'].append({
            "parameters": {
                "content": sticky["content"],
                "height": sticky["height"],
                "width": sticky["width"],
                "color": sticky["color"]
            },
            "type": "n8n-nodes-base.stickyNote",
            "typeVersion": 1,
            "position": sticky["position"],
            "id": f"sticky_{sticky['name'].replace(' ', '_')}",
            "name": sticky["name"]
        })

    # Reposition nodes
    repositioned = 0
    not_found = []
    for node in workflow['nodes']:
        if node['type'] != 'n8n-nodes-base.stickyNote':
            if node['name'] in layout_config["nodes"]:
                node['position'] = layout_config["nodes"][node['name']]
                repositioned += 1
            else:
                not_found.append(node['name'])

    # Save
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"  ✅ {len(layout_config['sticky_notes'])} sticky notes (AUCUNE)")
    print(f"  ✅ {repositioned} nodes repositionnés")
    if not_found:
        print(f"  ℹ️ Nodes non trouvés: {', '.join(not_found)}")

def main():
    print("=" * 80)
    print("🎯 FINAL CLEAN LAYOUT - SANS STICKY NOTES")
    print("=" * 80)
    print("\n✨ Configuration finale:")
    print("  • PAS de sticky notes (nodes visibles)")
    print("  • Espacement HORIZONTAL de 200px (très compact)")
    print("  • Espacement VERTICAL de 200px (bien espacé)")
    print("  • Outils MCP EN BAS du trigger")
    print("  • Flux gauche → droite ultra compact")

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
    print("✅ FINAL LAYOUT APPLIED - Clean, compact, sans sticky notes!")
    print("=" * 80)

if __name__ == "__main__":
    main()