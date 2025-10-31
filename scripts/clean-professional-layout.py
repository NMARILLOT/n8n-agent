#!/usr/bin/env python3
"""
LAYOUT PROFESSIONNEL - Comme le workflow Gmail
Espacement généreux, organisation claire, sticky notes bien dimensionnées
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT MCP - Organisation claire et espacée
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "🚀 MCP SERVER",
            "content": """## 🚀 MCP SERVER

Ouvre ce node pour obtenir l'URL SSE.
Configure ton agent IA avec cette URL.""",
            "position": [-500, -300],
            "width": 500,
            "height": 350,
            "color": 6  # Vert
        },
        {
            "name": "📦 PROJECT TOOLS",
            "content": """## 📦 PROJECT TOOLS

• search_projects
• get_project_by_id
• list_categories
• create_project
• create_idea""",
            "position": [200, -500],
            "width": 700,
            "height": 600,
            "color": 4  # Bleu
        },
        {
            "name": "💡 IDEA TOOLS",
            "content": """## 💡 IDEA TOOLS

• search_ideas
• get_idea_by_id
• update_idea
• delete_idea""",
            "position": [1100, -500],
            "width": 700,
            "height": 600,
            "color": 5  # Violet
        },
        {
            "name": "⚙️ BACKEND PROCESSING",
            "content": """## ⚙️ BACKEND PROCESSING

Traitement interne - Ne pas toucher""",
            "position": [-500, 400],
            "width": 2300,
            "height": 1400,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # === MCP Server (dans la sticky verte) ===
        "MCP Server Trigger": [-250, -100],

        # === PROJECT TOOLS (dans la sticky bleue, en grille 2x3) ===
        "search_projects": [350, -350],
        "get_project_by_id": [600, -350],
        "list_categories": [350, -150],
        "create_project": [600, -150],
        "create_idea": [475, 50],

        # === IDEA TOOLS (dans la sticky violette, en grille 2x2) ===
        "search_ideas": [1250, -350],
        "get_idea_by_id": [1500, -350],
        "update_idea": [1250, -150],
        "delete_idea": [1500, -150],

        # === BACKEND (dans la grande sticky orange) ===
        # Entrée (rangée du haut)
        "Execute Workflow Trigger": [-300, 550],
        "Switch Operation": [0, 550],

        # Rangée 1: Notion operations (7 nodes)
        "Notion - Search Projects": [-300, 800],
        "Notion - Get Project By ID": [-50, 800],
        "Notion - Search Ideas": [200, 800],
        "Notion - Get Idea By ID": [450, 800],
        "Notion - Update Idea": [700, 800],
        "Notion - Delete Idea": [950, 800],
        "Notion - Get Project For Idea": [1200, 800],

        # Rangée 2: Format operations (7 nodes)
        "Format Search Projects": [-300, 1050],
        "Format Get Project By ID": [-50, 1050],
        "Format Search Ideas": [200, 1050],
        "Format Get Idea": [450, 1050],
        "Prepare Update Idea": [700, 1050],
        "Prepare Delete Idea": [950, 1050],
        "Find Project Page ID": [1200, 1050],

        # Rangée 3: Create/Update operations (7 nodes)
        "List Categories": [-300, 1300],
        "Generate Project ID": [-50, 1300],
        "Notion - Create Project": [200, 1300],
        "Format Create Project Response": [450, 1300],
        "Generate Idea ID": [700, 1300],
        "Notion - Create Idea1": [950, 1300],
        "Format Create Idea Response": [1200, 1300],

        # Rangée 4: Final operations (3 nodes)
        "Notion - Update Idea Page": [200, 1550],
        "Format Update Response": [450, 1550],
        "Format Delete Response": [700, 1550],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "📨 INPUT",
            "content": """## 📨 INPUT

Messages Telegram entrants""",
            "position": [-500, -300],
            "width": 500,
            "height": 400,
            "color": 6  # Vert
        },
        {
            "name": "🎤 VOCAL PROCESSING",
            "content": """## 🎤 VOCAL PROCESSING

Traitement des messages vocaux""",
            "position": [200, -500],
            "width": 1200,
            "height": 300,
            "color": 5  # Violet
        },
        {
            "name": "📝 TEXT PROCESSING",
            "content": """## 📝 TEXT PROCESSING

Traitement des messages texte""",
            "position": [200, 0],
            "width": 500,
            "height": 300,
            "color": 4  # Bleu
        },
        {
            "name": "🤖 AI AGENT",
            "content": """## 🤖 INTELLIGENCE ARTIFICIELLE

Claude Sonnet + MCP + Memory""",
            "position": [1600, -300],
            "width": 700,
            "height": 600,
            "color": 3  # Rouge
        },
        {
            "name": "📤 OUTPUT",
            "content": """## 📤 OUTPUT

Réponse Telegram""",
            "position": [2500, -300],
            "width": 500,
            "height": 400,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # === INPUT (dans la sticky verte) ===
        "Telegram Trigger": [-250, -100],
        "Switch: Type d'entrée": [-250, 100],

        # === VOCAL (dans la sticky violette, horizontal) ===
        "Get Audio File": [350, -350],
        "Download Audio": [600, -350],
        "Transcribe Audio": [850, -350],
        "Format Audio Input": [1100, -350],

        # === TEXT (dans la sticky bleue) ===
        "Format Text Input": [450, 150],

        # === AI (dans la sticky rouge) ===
        "Agent Dev Ideas": [1950, -100],
        "Claude Sonnet 4.5": [1750, 150],
        "MCP Client - Projects": [1950, 150],
        "Simple Memory": [2150, 150],

        # === OUTPUT (dans la sticky orange) ===
        "Format Markdown for Telegram": [2750, -100],
        "Send Telegram Response": [2750, 100],
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
            "id": f"sticky_{sticky['name'].replace(' ', '_').replace(':', '')}",
            "name": sticky["name"],
            "typeVersion": 1
        })

    # Reposition nodes
    count = 0
    for node in workflow['nodes']:
        if node['name'] in layout_config["nodes"]:
            node['position'] = layout_config["nodes"][node['name']]
            count += 1

    # Save
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"  ✅ {len(layout_config['sticky_notes'])} sticky notes")
    print(f"  ✅ {count} nodes repositionnés")

def main():
    print("=" * 60)
    print("🎯 LAYOUT PROFESSIONNEL CLEAN")
    print("=" * 60)
    print("\n✨ Principe:")
    print("  • Sticky notes bien dimensionnées")
    print("  • Nodes bien espacés (250px minimum)")
    print("  • Organisation en grilles claires")
    print("  • Sections logiques colorées")

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

    print("\n" + "=" * 60)
    print("✅ TERMINÉ - Layout professionnel appliqué")
    print("=" * 60)

if __name__ == "__main__":
    main()