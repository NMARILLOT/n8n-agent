#!/usr/bin/env python3
"""
LAYOUT SIMPLE ET PROPRE - Version qui MARCHE vraiment
Pas de fantaisie, juste de l'organisation basique et claire
"""

import json
from pathlib import Path

# ============================================================================
# PRINCIPE: TOUT EN LIGNE, BIEN ESPACÉ, SIMPLE
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "1. MCP Server",
            "content": """## 🚀 MCP SERVER

Ouvre ce node pour obtenir l'URL SSE.
Configure ton agent IA avec cette URL.""",
            "position": [-200, -200],
            "width": 400,
            "height": 300,
            "color": 6  # Vert
        },
        {
            "name": "2. Project Tools",
            "content": """## 📦 PROJECT TOOLS

• search_projects
• get_project_by_id
• list_categories
• create_project
• create_idea""",
            "position": [300, -200],
            "width": 500,
            "height": 400,
            "color": 4  # Bleu
        },
        {
            "name": "3. Idea Tools",
            "content": """## 💡 IDEA TOOLS

• search_ideas
• get_idea_by_id
• update_idea
• delete_idea""",
            "position": [900, -200],
            "width": 500,
            "height": 400,
            "color": 5  # Violet
        },
        {
            "name": "4. Internal Processing",
            "content": """## ⚙️ BACKEND

Ne pas toucher - Traitement interne""",
            "position": [-200, 500],
            "width": 1600,
            "height": 800,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # === SECTION 1: MCP Server (Gauche) ===
        "MCP Server Trigger": [0, 0],

        # === SECTION 2: Project Tools (Centre-gauche) ===
        "search_projects": [400, -100],
        "get_project_by_id": [400, 0],
        "list_categories": [400, 100],
        "create_project": [600, -100],
        "create_idea": [600, 0],

        # === SECTION 3: Idea Tools (Centre-droit) ===
        "search_ideas": [1000, -100],
        "get_idea_by_id": [1000, 0],
        "update_idea": [1200, -100],
        "delete_idea": [1200, 0],

        # === SECTION 4: Backend (En bas, en grille) ===
        # Ligne 1: Trigger et Switch
        "Execute Workflow Trigger": [0, 600],
        "Switch Operation": [200, 600],

        # Ligne 2: Nodes Notion (Get/Search)
        "Notion - Search Projects": [0, 800],
        "Notion - Get Project By ID": [200, 800],
        "Notion - Search Ideas": [400, 800],
        "Notion - Get Idea By ID": [600, 800],
        "Notion - Update Idea": [800, 800],
        "Notion - Delete Idea": [1000, 800],
        "Notion - Get Project For Idea": [1200, 800],

        # Ligne 3: Format et Prepare
        "Format Search Projects": [0, 1000],
        "Format Get Project By ID": [200, 1000],
        "Format Search Ideas": [400, 1000],
        "Format Get Idea": [600, 1000],
        "Prepare Update Idea": [800, 1000],
        "Prepare Delete Idea": [1000, 1000],
        "Find Project Page ID": [1200, 1000],

        # Ligne 4: Operations
        "List Categories": [0, 1200],
        "Generate Project ID": [200, 1200],
        "Notion - Create Project": [400, 1200],
        "Generate Idea ID": [600, 1200],
        "Notion - Create Idea1": [800, 1200],
        "Notion - Update Idea Page": [1000, 1200],
        "Format Delete Response": [1200, 1200],

        # Ligne 5: Format final
        "Format Create Project Response": [200, 1400],
        "Format Create Idea Response": [400, 1400],
        "Format Update Response": [600, 1400],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "1. Entrée",
            "content": """## 📨 ENTRÉE

Telegram Trigger → Switch""",
            "position": [-200, -200],
            "width": 400,
            "height": 250,
            "color": 6  # Vert
        },
        {
            "name": "2. Vocal",
            "content": """## 🎤 VOCAL

Audio → Download → Transcribe → Format""",
            "position": [300, -350],
            "width": 1000,
            "height": 200,
            "color": 5  # Violet
        },
        {
            "name": "3. Texte",
            "content": """## 📝 TEXTE

Format direct""",
            "position": [300, 50],
            "width": 400,
            "height": 200,
            "color": 4  # Bleu
        },
        {
            "name": "4. IA",
            "content": """## 🤖 AGENT IA

Claude + MCP + Memory""",
            "position": [1400, -200],
            "width": 600,
            "height": 400,
            "color": 3  # Rouge
        },
        {
            "name": "5. Sortie",
            "content": """## 📤 SORTIE

Format → Send""",
            "position": [2100, -200],
            "width": 400,
            "height": 250,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # === SECTION 1: Entrée ===
        "Telegram Trigger": [-100, 0],
        "Switch: Type d'entrée": [100, 0],

        # === SECTION 2: Vocal (en haut) ===
        "Get Audio File": [400, -250],
        "Download Audio": [600, -250],
        "Transcribe Audio": [800, -250],
        "Format Audio Input": [1000, -250],

        # === SECTION 3: Texte (en bas) ===
        "Format Text Input": [400, 150],

        # === SECTION 4: IA ===
        "Agent Dev Ideas": [1500, 0],
        "Claude Sonnet 4.5": [1500, 200],
        "MCP Client - Projects": [1700, 200],
        "Simple Memory": [1600, 200],

        # === SECTION 5: Sortie ===
        "Format Markdown for Telegram": [2200, 0],
        "Send Telegram Response": [2400, 0],
    }
}

# ============================================================================
# FONCTIONS SIMPLES
# ============================================================================

def apply_layout(workflow_path, layout_config, name):
    print(f"\n🎨 {name}")
    print("=" * 60)

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Supprimer sticky notes
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']

    # Ajouter nouvelles sticky notes
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
            "id": f"sticky_{sticky['name'].replace(' ', '_').replace('.', '')}",
            "name": sticky["name"],
            "typeVersion": 1
        })

    # Repositionner nodes
    count = 0
    for node in workflow['nodes']:
        if node['name'] in layout_config["nodes"]:
            node['position'] = layout_config["nodes"][node['name']]
            count += 1

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"✅ {len(layout_config['sticky_notes'])} sticky notes")
    print(f"✅ {count} nodes repositionnés")

def main():
    print("=" * 60)
    print("🧹 LAYOUT SIMPLE ET PROPRE")
    print("=" * 60)
    print("\n✨ Principe:")
    print("  • Sections numérotées (1, 2, 3, 4, 5)")
    print("  • Tout en ligne horizontale")
    print("  • Espacement régulier de 200px")
    print("  • Sticky notes simples et claires")
    print("  • Pas de fantaisie, juste de l'ordre")

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
    print("✅ TERMINÉ - Layout simple appliqué")
    print("=" * 60)

if __name__ == "__main__":
    main()