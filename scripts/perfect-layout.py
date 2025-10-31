#!/usr/bin/env python3
"""
PERFECT LAYOUT - Organisation parfaite comme les pros
Espacement TRÈS généreux, alignement parfait, sticky notes correctes
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT MCP - ESPACEMENT MAXIMAL
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "🚀 MCP SERVER",
            "content": """## 🚀 MCP SERVER

Ouvre ce node pour obtenir l'URL SSE.
Configure ton agent IA avec cette URL.""",
            "position": [-800, -400],
            "width": 450,
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
            "position": [-200, -600],
            "width": 900,
            "height": 700,
            "color": 4  # Bleu
        },
        {
            "name": "💡 IDEA TOOLS",
            "content": """## 💡 IDEA TOOLS

• search_ideas
• get_idea_by_id
• update_idea
• delete_idea""",
            "position": [800, -600],
            "width": 900,
            "height": 700,
            "color": 5  # Violet
        },
        {
            "name": "⚙️ BACKEND PROCESSING",
            "content": """## ⚙️ BACKEND PROCESSING

Traitement interne - Ne pas toucher""",
            "position": [-800, 200],
            "width": 2500,
            "height": 1800,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # === MCP Server (centré dans la sticky verte) ===
        "MCP Server Trigger": [-575, -225],

        # === PROJECT TOOLS (grille 3x2 espacée dans la sticky bleue) ===
        "search_projects": [-50, -450],
        "get_project_by_id": [200, -450],
        "list_categories": [450, -450],
        "create_project": [-50, -200],
        "create_idea": [200, -200],

        # === IDEA TOOLS (grille 2x2 espacée dans la sticky violette) ===
        "search_ideas": [950, -450],
        "get_idea_by_id": [1250, -450],
        "update_idea": [950, -200],
        "delete_idea": [1250, -200],

        # === BACKEND (dans la TRÈS grande sticky orange) ===
        # Entrée (tout en haut, bien espacé)
        "Execute Workflow Trigger": [-600, 400],
        "Switch Operation": [-300, 400],

        # Rangée 1: Notion operations (bien espacées)
        "Notion - Search Projects": [-600, 700],
        "Notion - Get Project By ID": [-300, 700],
        "Notion - Search Ideas": [0, 700],
        "Notion - Get Idea By ID": [300, 700],
        "Notion - Update Idea": [600, 700],
        "Notion - Delete Idea": [900, 700],
        "Notion - Get Project For Idea": [1200, 700],

        # Rangée 2: Format operations (alignées avec rangée 1)
        "Format Search Projects": [-600, 1000],
        "Format Get Project By ID": [-300, 1000],
        "Format Search Ideas": [0, 1000],
        "Format Get Idea": [300, 1000],
        "Prepare Update Idea": [600, 1000],
        "Prepare Delete Idea": [900, 1000],
        "Find Project Page ID": [1200, 1000],

        # Rangée 3: Create/Generate operations
        "List Categories": [-600, 1300],
        "Generate Project ID": [-300, 1300],
        "Notion - Create Project": [0, 1300],
        "Format Create Project Response": [300, 1300],
        "Generate Idea ID": [600, 1300],
        "Notion - Create Idea1": [900, 1300],
        "Format Create Idea Response": [1200, 1300],

        # Rangée 4: Final operations (centrées)
        "Notion - Update Idea Page": [0, 1600],
        "Format Update Response": [300, 1600],
        "Format Delete Response": [600, 1600],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "📨 INPUT",
            "content": """## 📨 INPUT

Messages Telegram entrants""",
            "position": [-800, -400],
            "width": 500,
            "height": 500,
            "color": 6  # Vert
        },
        {
            "name": "🎤 VOCAL",
            "content": """## 🎤 VOCAL PROCESSING

Traitement des messages vocaux""",
            "position": [-100, -600],
            "width": 1400,
            "height": 400,
            "color": 5  # Violet
        },
        {
            "name": "📝 TEXT",
            "content": """## 📝 TEXT PROCESSING

Traitement des messages texte""",
            "position": [-100, -100],
            "width": 600,
            "height": 400,
            "color": 4  # Bleu
        },
        {
            "name": "🤖 AI AGENT",
            "content": """## 🤖 INTELLIGENCE ARTIFICIELLE

Claude Sonnet + MCP + Memory""",
            "position": [1400, -400],
            "width": 800,
            "height": 700,
            "color": 3  # Rouge
        },
        {
            "name": "📤 OUTPUT",
            "content": """## 📤 OUTPUT

Réponse Telegram""",
            "position": [2300, -400],
            "width": 500,
            "height": 500,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # === INPUT (centré dans la sticky verte) ===
        "Telegram Trigger": [-550, -200],
        "Switch: Type d'entrée": [-550, 0],

        # === VOCAL (4 nodes espacés horizontalement) ===
        "Get Audio File": [50, -400],
        "Download Audio": [400, -400],
        "Transcribe Audio": [750, -400],
        "Format Audio Input": [1100, -400],

        # === TEXT (centré dans la sticky bleue) ===
        "Format Text Input": [200, 100],

        # === AI (disposé dans la sticky rouge) ===
        "Agent Dev Ideas": [1800, -200],
        "Claude Sonnet 4.5": [1600, 100],
        "MCP Client - Projects": [1800, 100],
        "Simple Memory": [2000, 100],

        # === OUTPUT (centré dans la sticky orange) ===
        "Format Markdown for Telegram": [2550, -200],
        "Send Telegram Response": [2550, 0],
    }
}

# ============================================================================
# APPLY
# ============================================================================

def apply_layout(workflow_path, layout_config, name):
    print(f"🎨 Applying perfect layout to: {name}")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Clear ALL sticky notes
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']

    # Add new sticky notes with proper structure
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
            "id": f"sticky_{sticky['name'].replace(' ', '_').replace('🚀', '').replace('📦', '').replace('💡', '').replace('⚙️', '').replace('📨', '').replace('🎤', '').replace('📝', '').replace('🤖', '').replace('📤', '')}",
            "name": sticky["name"]
        })

    # Reposition ALL nodes with exact coordinates
    repositioned = 0
    missing = []
    for node in workflow['nodes']:
        if node['type'] != 'n8n-nodes-base.stickyNote':
            if node['name'] in layout_config["nodes"]:
                node['position'] = layout_config["nodes"][node['name']]
                repositioned += 1
            else:
                missing.append(node['name'])

    # Save the updated workflow
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"  ✅ Added {len(layout_config['sticky_notes'])} sticky notes")
    print(f"  ✅ Repositioned {repositioned} nodes")
    if missing:
        print(f"  ⚠️ Nodes not repositioned: {', '.join(missing)}")

def main():
    print("=" * 80)
    print("🎯 PERFECT PROFESSIONAL LAYOUT")
    print("=" * 80)
    print("\n✨ Features:")
    print("  • Maximum spacing (300px between nodes)")
    print("  • Perfect grid alignment")
    print("  • Sticky notes properly sized")
    print("  • Nodes centered in sticky notes")
    print("  • Clear visual hierarchy")

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Apply to MCP workflow
    mcp_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"
    if mcp_path.exists():
        apply_layout(mcp_path, MCP_LAYOUT, "MCP - Idée Dev Nico (Perso)")
    else:
        print(f"  ❌ MCP workflow not found")

    # Apply to Telegram workflow
    telegram_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    if telegram_path.exists():
        apply_layout(telegram_path, TELEGRAM_LAYOUT, "Agent Telegram - Dev Ideas")
    else:
        print(f"  ❌ Telegram workflow not found")

    print("\n" + "=" * 80)
    print("✅ PERFECT LAYOUT APPLIED - Ready to deploy!")
    print("=" * 80)

if __name__ == "__main__":
    main()