#!/usr/bin/env python3
"""
COPIE EXACTE DU STYLE GMAIL MCP
Analyse du screenshot screen2 pour positions réelles
"""

import json
from pathlib import Path

# ============================================================================
# ANALYSE DU SCREENSHOT GMAIL MCP (screen2)
# ============================================================================
#
# Ce que je vois:
# - Gmail MCP Server au CENTRE (environ position 480, 320 dans leur grille)
# - Sticky notes GRANDES et LÉGÈRES en arrière-plan
# - 4 sections: Message Tools (gauche-bas), Label Tools (centre-haut),
#              Draft Tools (droite-haut), Thread Tools (droite-bas)
# - Nodes en GRILLE SERRÉE dans chaque sticky (spacing ~150px)
# - Connexions en ÉTOILE depuis le centre
#
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        # En haut à gauche - USAGE
        {
            "name": "Usage",
            "content": """## USAGE

Open the MCP Server Trigger node to obtain the SSE server URL.

Use that to configure an N8N AI Agent flow or other AI tool.""",
            "position": [80, 100],  # Haut gauche
            "width": 280,
            "height": 240,
            "color": 6
        },
        # Gauche - PROJECT TOOLS (comme Message Tools)
        {
            "name": "Project Tools",
            "content": """## PROJECT TOOLS""",
            "position": [80, 420],  # Gauche, en dessous
            "width": 660,
            "height": 460,
            "color": 4
        },
        # Haut centre - IDEA TOOLS (comme Label Tools)
        {
            "name": "Idea Tools",
            "content": """## IDEA TOOLS""",
            "position": [820, 100],  # Centre-haut
            "width": 380,
            "height": 440,
            "color": 5
        },
        # Droite - BACKEND (comme Thread Tools)
        {
            "name": "Backend Processing",
            "content": """## BACKEND PROCESSING""",
            "position": [820, 620],  # Droite-bas
            "width": 520,
            "height": 440,
            "color": 7
        }
    ],
    "nodes": {
        # === CENTRE: MCP Server Trigger ===
        "MCP Server Trigger": [480, 320],

        # === GAUCHE (PROJECT TOOLS) - 2 colonnes x 3 lignes ===
        "search_projects": [160, 500],
        "get_project_by_id": [320, 500],

        "list_categories": [160, 640],
        "create_project": [320, 640],

        "create_idea": [160, 780],

        # === HAUT (IDEA TOOLS) - 2 colonnes x 2 lignes ===
        "search_ideas": [900, 180],
        "get_idea_by_id": [1060, 180],

        "update_idea": [900, 320],
        "delete_idea": [1060, 320],

        # === BAS (BACKEND PROCESSING) ===
        # Entrée
        "Execute Workflow Trigger": [900, 700],
        "Switch Operation": [1060, 700],

        # Grille de traitement (3 colonnes x 6 lignes, très serré)
        # Colonne 1
        "Notion - Search Projects": [160, 980],
        "Format Search Projects": [160, 1120],

        # Colonne 2
        "Notion - Get Project By ID": [320, 980],
        "Format Get Project By ID": [320, 1120],

        # Colonne 3
        "List Categories": [480, 980],

        # Colonne 4
        "Generate Project ID": [640, 980],
        "Notion - Create Project": [640, 1120],
        "Format Create Project Response": [640, 1260],

        # Colonne 5
        "Generate Idea ID": [800, 980],
        "Notion - Get Project For Idea": [800, 1120],
        "Find Project Page ID": [800, 1260],
        "Notion - Create Idea1": [800, 1400],
        "Format Create Idea Response": [800, 1540],

        # Colonne 6
        "Notion - Search Ideas": [960, 980],
        "Format Search Ideas": [960, 1120],

        # Colonne 7
        "Notion - Get Idea By ID": [1120, 980],
        "Format Get Idea": [1120, 1120],

        # Colonne 8 - Update
        "Notion - Update Idea": [160, 1400],
        "Prepare Update Idea": [320, 1400],
        "Notion - Update Idea Page": [480, 1400],
        "Format Update Response": [640, 1400],

        # Colonne 9 - Delete
        "Notion - Delete Idea": [800, 1680],
        "Prepare Delete Idea": [960, 1680],
        "Format Delete Response": [1120, 1680],
    }
}

# ============================================================================
# TELEGRAM - SIMPLIFIÉ
# ============================================================================

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "Overview",
            "content": """## AGENT TELEGRAM

Capture automatique des idées depuis Telegram.
Support texte ET vocal.""",
            "position": [60, 80],
            "width": 380,
            "height": 240,
            "color": 6
        },
        {
            "name": "Input",
            "content": """## RÉCEPTION""",
            "position": [520, 80],
            "width": 380,
            "height": 240,
            "color": 4
        },
        {
            "name": "Vocal Branch",
            "content": """## TRAITEMENT VOCAL""",
            "position": [980, 60],
            "width": 800,
            "height": 200,
            "color": 5
        },
        {
            "name": "Text Branch",
            "content": """## TRAITEMENT TEXTE""",
            "position": [980, 340],
            "width": 380,
            "height": 160,
            "color": 7
        },
        {
            "name": "AI",
            "content": """## INTELLIGENCE ARTIFICIELLE""",
            "position": [1860, 80],
            "width": 480,
            "height": 240,
            "color": 3
        }
    ],
    "nodes": {
        # Input
        "Telegram Trigger": [180, 180],
        "Switch: Type d'entrée": [420, 180],

        # Vocal (haut)
        "Get Audio File": [1060, 140],
        "Download Audio": [1260, 140],
        "Transcribe Audio": [1460, 140],
        "Format Audio Input": [1660, 140],

        # Text (bas)
        "Format Text Input": [1060, 420],

        # AI
        "Agent Dev Ideas": [1980, 180],
        "Claude Sonnet 4.5": [1860, 360],
        "Simple Memory": [2020, 360],
        "MCP Client - Projects": [2180, 360],

        # Output
        "Format Markdown for Telegram": [2440, 180],
        "Send Telegram Response": [2680, 180],
    }
}

# ============================================================================
# FONCTIONS
# ============================================================================

def clear_sticky_notes(workflow):
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']
    return workflow

def create_sticky(config):
    return {
        "parameters": {
            "content": config["content"],
            "height": config["height"],
            "width": config["width"],
            "color": config["color"]
        },
        "type": "n8n-nodes-base.stickyNote",
        "position": config["position"],
        "id": f"sticky_{config['name'].lower().replace(' ', '_')}",
        "name": config["name"],
        "typeVersion": 1
    }

def reposition_nodes(workflow, positions):
    count = 0
    for node in workflow['nodes']:
        if node['name'] in positions:
            node['position'] = positions[node['name']]
            count += 1
    return count

def apply_layout(workflow_path, layout_config, workflow_name):
    print(f"\n{'=' * 80}")
    print(f"🎨 {workflow_name}")
    print('=' * 80)

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    workflow = clear_sticky_notes(workflow)
    print("✅ Anciennes sticky notes supprimées")

    print(f"\n📌 Sticky notes (style Gmail MCP):")
    for sticky_config in layout_config["sticky_notes"]:
        sticky_node = create_sticky(sticky_config)
        workflow['nodes'].append(sticky_node)
        pos = sticky_config['position']
        size = f"{sticky_config['width']}x{sticky_config['height']}"
        print(f"  • {sticky_config['name']:20s} pos:[{pos[0]:4d}, {pos[1]:4d}] {size}")

    print(f"\n📐 Repositionnement des nodes...")
    count = reposition_nodes(workflow, layout_config["nodes"])
    print(f"  ✅ {count} nodes repositionnés")

    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"\n✨ Layout appliqué!")

def main():
    print("=" * 80)
    print("🎨 COPIE EXACTE DU STYLE GMAIL MCP")
    print("=" * 80)
    print("\nBasé sur l'analyse du screenshot screen2 (Gmail MCP)")
    print("Positions et tailles copiées précisément")

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    mcp_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"
    if mcp_path.exists():
        apply_layout(mcp_path, MCP_LAYOUT, "MCP - Idée Dev Nico (Perso)")

    telegram_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    if telegram_path.exists():
        apply_layout(telegram_path, TELEGRAM_LAYOUT, "Agent Telegram - Dev Ideas")

    print("\n" + "=" * 80)
    print("🎯 DÉPLOIE MAINTENANT:")
    print("  ./scripts/deploy.sh")
    print("=" * 80)

if __name__ == "__main__":
    main()
