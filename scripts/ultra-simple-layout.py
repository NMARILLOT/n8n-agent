#!/usr/bin/env python3
"""
ULTRA SIMPLE LAYOUT - Le plus basique possible
Juste des colonnes verticales, pas de fantaisie
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT MCP - EN COLONNES VERTICALES SIMPLES
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "MCP Server",
            "content": "## MCP SERVER\n\nDéclenche le serveur MCP",
            "position": [0, 0],
            "width": 300,
            "height": 200,
            "color": 6
        },
        {
            "name": "Tools",
            "content": "## TOOLS\n\nOutils exposés via MCP",
            "position": [400, -200],
            "width": 800,
            "height": 600,
            "color": 4
        },
        {
            "name": "Processing",
            "content": "## BACKEND",
            "position": [0, 500],
            "width": 1200,
            "height": 800,
            "color": 7
        }
    ],
    "nodes": {
        # Colonne 1: MCP Trigger
        "MCP Server Trigger": [100, 100],

        # Colonne 2-3: Tools (2 colonnes)
        "search_projects": [500, -100],
        "get_project_by_id": [500, 0],
        "list_categories": [500, 100],
        "create_project": [500, 200],
        "create_idea": [500, 300],

        "search_ideas": [800, -100],
        "get_idea_by_id": [800, 0],
        "update_idea": [800, 100],
        "delete_idea": [800, 200],

        # Backend - En grille régulière en bas
        "Execute Workflow Trigger": [100, 600],
        "Switch Operation": [300, 600],

        # Rangée des Notion nodes
        "Notion - Search Projects": [100, 800],
        "Notion - Get Project By ID": [300, 800],
        "Notion - Search Ideas": [500, 800],
        "Notion - Get Idea By ID": [700, 800],
        "Notion - Update Idea": [900, 800],
        "Notion - Delete Idea": [1100, 800],

        # Rangée des Format nodes
        "Format Search Projects": [100, 1000],
        "Format Get Project By ID": [300, 1000],
        "Format Search Ideas": [500, 1000],
        "Format Get Idea": [700, 1000],
        "Prepare Update Idea": [900, 1000],
        "Prepare Delete Idea": [1100, 1000],

        # Rangée du reste
        "List Categories": [100, 1200],
        "Generate Project ID": [300, 1200],
        "Notion - Create Project": [500, 1200],
        "Format Create Project Response": [700, 1200],
        "Generate Idea ID": [900, 1200],
        "Notion - Get Project For Idea": [1100, 1200],

        # Dernière rangée
        "Find Project Page ID": [300, 1400],
        "Notion - Create Idea1": [500, 1400],
        "Format Create Idea Response": [700, 1400],
        "Notion - Update Idea Page": [900, 1400],
        "Format Update Response": [1100, 1400],
        "Format Delete Response": [1300, 1400],
    }
}

# ============================================================================
# LAYOUT TELEGRAM - FLUX HORIZONTAL BASIQUE
# ============================================================================

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "Input",
            "content": "## INPUT",
            "position": [0, 0],
            "width": 400,
            "height": 300,
            "color": 6
        },
        {
            "name": "Processing",
            "content": "## PROCESSING",
            "position": [500, -200],
            "width": 800,
            "height": 600,
            "color": 4
        },
        {
            "name": "AI",
            "content": "## AI",
            "position": [1400, 0],
            "width": 400,
            "height": 300,
            "color": 3
        },
        {
            "name": "Output",
            "content": "## OUTPUT",
            "position": [1900, 0],
            "width": 400,
            "height": 300,
            "color": 7
        }
    ],
    "nodes": {
        # Colonne 1: Input
        "Telegram Trigger": [100, 100],
        "Switch: Type d'entrée": [250, 100],

        # Colonne 2-3: Processing
        "Get Audio File": [600, -100],
        "Download Audio": [800, -100],
        "Transcribe Audio": [1000, -100],
        "Format Audio Input": [1200, -100],

        "Format Text Input": [600, 200],

        # Colonne 4: AI
        "Agent Dev Ideas": [1500, 100],
        "Claude Sonnet 4.5": [1500, 250],
        "MCP Client - Projects": [1650, 250],
        "Simple Memory": [1350, 250],

        # Colonne 5: Output
        "Format Markdown for Telegram": [2000, 100],
        "Send Telegram Response": [2200, 100],
    }
}

# ============================================================================
# APPLY
# ============================================================================

def apply_layout(workflow_path, layout_config, name):
    print(f"🎨 {name}")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Clear sticky notes
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']

    # Add new sticky notes
    for sticky in layout_config["sticky_notes"]:
        workflow['nodes'].append({
            "parameters": {
                "content": sticky["content"],
                "height": sticky["height"],
                "width": sticky["width"],
                "color": sticky["color"]
            },
            "type": "n8n-nodes-base.stickyNote",
            "position": sticky["position"],
            "id": f"sticky_{sticky['name'].replace(' ', '_')}",
            "name": sticky["name"],
            "typeVersion": 1
        })

    # Reposition nodes
    for node in workflow['nodes']:
        if node['name'] in layout_config["nodes"]:
            node['position'] = layout_config["nodes"][node['name']]

    # Save
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"  ✅ {len(layout_config['sticky_notes'])} sticky notes")
    print(f"  ✅ {len(layout_config['nodes'])} nodes repositionnés")

def main():
    print("=" * 60)
    print("🎯 ULTRA SIMPLE LAYOUT")
    print("=" * 60)

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # MCP
    mcp_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"
    if mcp_path.exists():
        apply_layout(mcp_path, MCP_LAYOUT, "MCP")

    # Telegram
    telegram_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    if telegram_path.exists():
        apply_layout(telegram_path, TELEGRAM_LAYOUT, "Telegram")

    print("\n✅ Fait! Relance workflow-preview.py pour voir")

if __name__ == "__main__":
    main()