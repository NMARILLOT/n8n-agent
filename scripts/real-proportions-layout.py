#!/usr/bin/env python3
"""
VRAIES PROPORTIONS - Basé sur le screenshot
Les sticky notes doivent être ÉNORMES et contenir les nodes À L'INTÉRIEUR
"""

import json
from pathlib import Path

# ============================================================================
# PROPORTIONS RÉELLES BASÉES SUR LE SCREENSHOT
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "MCP SERVER",
            "content": """## 🚀 MCP SERVER

Ouvre ce node pour obtenir l'URL SSE.
Configure ton Agent IA avec cette URL.""",
            "position": [-400, -400],  # Bien à gauche
            "width": 600,
            "height": 400,
            "color": 6  # Vert
        },
        {
            "name": "PROJECT TOOLS",
            "content": """## 📦 PROJECT TOOLS

• search_projects
• get_project_by_id
• list_categories
• create_project
• create_idea""",
            "position": [400, -400],  # Centre
            "width": 800,
            "height": 800,  # GRANDE pour contenir 5 tools
            "color": 4  # Bleu
        },
        {
            "name": "IDEA TOOLS",
            "content": """## 💡 IDEA TOOLS

• search_ideas
• get_idea_by_id
• update_idea
• delete_idea""",
            "position": [1400, -400],  # Droite
            "width": 800,
            "height": 800,  # GRANDE
            "color": 5  # Violet
        },
        {
            "name": "BACKEND",
            "content": """## ⚙️ BACKEND

Ne pas toucher - Traitement interne""",
            "position": [-400, 600],  # En bas, très large
            "width": 2800,  # TRÈS LARGE
            "height": 1600,  # TRÈS HAUTE
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # === MCP SERVER (dans la sticky verte) ===
        "MCP Server Trigger": [-100, -200],

        # === PROJECT TOOLS (dans la sticky bleue) ===
        # En grille 2x3 DANS la sticky
        "search_projects": [500, -300],
        "get_project_by_id": [750, -300],
        "list_categories": [500, -50],
        "create_project": [750, -50],
        "create_idea": [500, 200],

        # === IDEA TOOLS (dans la sticky violette) ===
        # En grille 2x2 DANS la sticky
        "search_ideas": [1500, -300],
        "get_idea_by_id": [1750, -300],
        "update_idea": [1500, -50],
        "delete_idea": [1750, -50],

        # === BACKEND (dans la GRANDE sticky orange) ===
        # Entrée
        "Execute Workflow Trigger": [-200, 800],
        "Switch Operation": [100, 800],

        # Grille de nodes - BEAUCOUP plus espacés
        # Rangée 1
        "Notion - Search Projects": [-200, 1100],
        "Notion - Get Project By ID": [150, 1100],
        "Notion - Search Ideas": [500, 1100],
        "Notion - Get Idea By ID": [850, 1100],
        "Notion - Update Idea": [1200, 1100],
        "Notion - Delete Idea": [1550, 1100],
        "Notion - Get Project For Idea": [1900, 1100],

        # Rangée 2
        "Format Search Projects": [-200, 1400],
        "Format Get Project By ID": [150, 1400],
        "Format Search Ideas": [500, 1400],
        "Format Get Idea": [850, 1400],
        "Prepare Update Idea": [1200, 1400],
        "Prepare Delete Idea": [1550, 1400],
        "Find Project Page ID": [1900, 1400],

        # Rangée 3
        "List Categories": [-200, 1700],
        "Generate Project ID": [150, 1700],
        "Notion - Create Project": [500, 1700],
        "Format Create Project Response": [850, 1700],
        "Generate Idea ID": [1200, 1700],
        "Notion - Create Idea1": [1550, 1700],
        "Format Create Idea Response": [1900, 1700],

        # Rangée 4
        "Notion - Update Idea Page": [500, 2000],
        "Format Update Response": [850, 2000],
        "Format Delete Response": [1200, 2000],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "INPUT",
            "content": """## 📨 INPUT

Telegram messages entrants""",
            "position": [-400, -400],
            "width": 600,
            "height": 600,
            "color": 6  # Vert
        },
        {
            "name": "VOCAL PROCESSING",
            "content": """## 🎤 VOCAL

Traitement des messages vocaux""",
            "position": [400, -600],
            "width": 1400,  # LARGE pour 4 nodes
            "height": 400,
            "color": 5  # Violet
        },
        {
            "name": "TEXT PROCESSING",
            "content": """## 📝 TEXT

Traitement des messages texte""",
            "position": [400, 0],
            "width": 600,
            "height": 400,
            "color": 4  # Bleu
        },
        {
            "name": "AI AGENT",
            "content": """## 🤖 INTELLIGENCE ARTIFICIELLE

Claude Sonnet 4.5
+ MCP Client
+ Memory""",
            "position": [2000, -400],
            "width": 800,
            "height": 800,
            "color": 3  # Rouge
        },
        {
            "name": "OUTPUT",
            "content": """## 📤 OUTPUT

Réponse Telegram""",
            "position": [3000, -400],
            "width": 600,
            "height": 600,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # === INPUT (dans la sticky verte) ===
        "Telegram Trigger": [-200, -200],
        "Switch: Type d'entrée": [-200, 0],

        # === VOCAL (dans la sticky violette) ===
        "Get Audio File": [500, -400],
        "Download Audio": [800, -400],
        "Transcribe Audio": [1100, -400],
        "Format Audio Input": [1400, -400],

        # === TEXT (dans la sticky bleue) ===
        "Format Text Input": [600, 200],

        # === AI (dans la sticky rouge) ===
        "Agent Dev Ideas": [2200, -200],
        "Claude Sonnet 4.5": [2100, 100],
        "MCP Client - Projects": [2400, 100],
        "Simple Memory": [2250, 100],

        # === OUTPUT (dans la sticky orange) ===
        "Format Markdown for Telegram": [3200, -200],
        "Send Telegram Response": [3200, 0],
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

    # Add HUGE sticky notes
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

    # Reposition nodes INSIDE sticky notes
    for node in workflow['nodes']:
        if node['name'] in layout_config["nodes"]:
            node['position'] = layout_config["nodes"][node['name']]

    # Save
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"  ✅ {len(layout_config['sticky_notes'])} GRANDES sticky notes")
    print(f"  ✅ {len(layout_config['nodes'])} nodes repositionnés À L'INTÉRIEUR")

def main():
    print("=" * 80)
    print("🎯 VRAIES PROPORTIONS - Sticky notes ÉNORMES")
    print("=" * 80)
    print("\n📐 Basé sur ton screenshot:")
    print("  • Sticky notes de 600-2800px de large")
    print("  • Nodes À L'INTÉRIEUR des sticky notes")
    print("  • Espacement de 300-350px entre nodes")
    print("  • Backend dans une ÉNORME sticky")

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # MCP
    mcp_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"
    if mcp_path.exists():
        apply_layout(mcp_path, MCP_LAYOUT, "MCP - Idée Dev Nico (Perso)")

    # Telegram
    telegram_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    if telegram_path.exists():
        apply_layout(telegram_path, TELEGRAM_LAYOUT, "Agent Telegram - Dev Ideas")

    print("\n" + "=" * 80)
    print("✅ TERMINÉ avec les VRAIES proportions!")
    print("   Relance workflow-preview.py pour voir")
    print("=" * 80)

if __name__ == "__main__":
    main()