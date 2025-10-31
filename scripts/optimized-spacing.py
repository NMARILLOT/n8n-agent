#!/usr/bin/env python3
"""
OPTIMIZED SPACING - Plus d'espace vertical, moins d'espace horizontal
Pour éviter tout chevauchement et avoir un flux compact mais clair
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT MCP - ESPACEMENT VERTICAL MAXIMUM, HORIZONTAL COMPACT
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "🚀 TRIGGER",
            "content": """## 🚀 MCP SERVER TRIGGER

Point d'entrée du workflow
Configure l'URL SSE ici""",
            "position": [-800, -600],
            "width": 350,
            "height": 1800,
            "color": 6  # Vert
        },
        {
            "name": "📦 EXPOSED TOOLS",
            "content": """## 📦 TOOLS EXPOSÉS VIA MCP

9 outils disponibles pour l'agent IA""",
            "position": [-400, -900],
            "width": 350,
            "height": 2400,
            "color": 4  # Bleu
        },
        {
            "name": "⚙️ BACKEND PROCESSING",
            "content": """## ⚙️ TRAITEMENT BACKEND

Opérations Notion et formatage""",
            "position": [0, -1200],
            "width": 3200,
            "height": 3000,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # COLONNE 1: Trigger (X = -625)
        "MCP Server Trigger": [-625, 300],

        # COLONNE 2: Tools exposés (X = -225, espacement de 200px vertical)
        "search_projects": [-225, -800],
        "get_project_by_id": [-225, -600],
        "list_categories": [-225, -400],
        "create_project": [-225, -200],
        "create_idea": [-225, 0],
        "search_ideas": [-225, 200],
        "get_idea_by_id": [-225, 400],
        "update_idea": [-225, 600],
        "delete_idea": [-225, 800],

        # COLONNE 3: Backend trigger et switch (X = 150 et 350)
        "Execute Workflow Trigger": [150, 300],
        "Switch Operation": [350, 300],

        # BRANCHES PARALLÈLES DU BACKEND (espacement vertical de 200px)

        # Branche 1: Search Projects (Y = -1000)
        "Notion - Search Projects": [600, -1000],
        "Format Search Projects": [900, -1000],

        # Branche 2: Get Project By ID (Y = -800)
        "Notion - Get Project By ID": [600, -800],
        "Format Get Project By ID": [900, -800],

        # Branche 3: List Categories (Y = -600)
        "List Categories": [600, -600],

        # Branche 4: Search Ideas (Y = -400)
        "Notion - Search Ideas": [600, -400],
        "Format Search Ideas": [900, -400],

        # Branche 5: Get Idea By ID (Y = -200)
        "Notion - Get Idea By ID": [600, -200],
        "Format Get Idea": [900, -200],

        # Branche 6: Create Project (Y = 0)
        "Generate Project ID": [600, 0],
        "Notion - Create Project": [900, 0],
        "Format Create Project Response": [1200, 0],

        # Branche 7: Create Idea (Y = 200)
        "Generate Idea ID": [600, 200],
        "Notion - Get Project For Idea": [900, 200],
        "Find Project Page ID": [1200, 200],
        "Notion - Create Idea1": [1500, 200],
        "Format Create Idea Response": [1800, 200],

        # Branche 8: Update Idea (Y = 400)
        "Notion - Update Idea": [600, 400],
        "Prepare Update Idea": [900, 400],
        "Notion - Update Idea Page": [1200, 400],
        "Format Update Response": [1500, 400],

        # Branche 9: Delete Idea (Y = 600)
        "Notion - Delete Idea": [600, 600],
        "Prepare Delete Idea": [900, 600],
        "Format Delete Response": [1200, 600],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "📨 ENTRÉE",
            "content": """## 📨 ENTRÉE TELEGRAM

Messages entrants""",
            "position": [-800, -300],
            "width": 350,
            "height": 800,
            "color": 6  # Vert
        },
        {
            "name": "🔀 ROUTING",
            "content": """## 🔀 ROUTING

Switch par type de message""",
            "position": [-400, -300],
            "width": 350,
            "height": 800,
            "color": 4  # Bleu
        },
        {
            "name": "🎤 BRANCHE VOCALE",
            "content": """## 🎤 TRAITEMENT VOCAL

Pipeline audio → texte""",
            "position": [0, -700],
            "width": 1600,
            "height": 400,
            "color": 5  # Violet
        },
        {
            "name": "📝 BRANCHE TEXTE",
            "content": """## 📝 TRAITEMENT TEXTE

Format direct""",
            "position": [0, 300],
            "width": 500,
            "height": 400,
            "color": 4  # Bleu clair
        },
        {
            "name": "🤖 AGENT IA",
            "content": """## 🤖 INTELLIGENCE ARTIFICIELLE

Claude + MCP + Memory""",
            "position": [1700, -400],
            "width": 900,
            "height": 1000,
            "color": 3  # Rouge
        },
        {
            "name": "📤 SORTIE",
            "content": """## 📤 RÉPONSE

Envoi Telegram""",
            "position": [2700, -300],
            "width": 600,
            "height": 800,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # COLONNE 1: Entrée (X = -625)
        "Telegram Trigger": [-625, 100],

        # COLONNE 2: Switch (X = -225)
        "Switch: Type d'entrée": [-225, 100],

        # BRANCHE HAUTE: Traitement vocal (Y = -500, espacement horizontal de 300px)
        "Get Audio File": [150, -500],
        "Download Audio": [450, -500],
        "Transcribe Audio": [750, -500],
        "Format Audio Input": [1050, -500],

        # BRANCHE BASSE: Traitement texte (Y = 500)
        "Format Text Input": [250, 500],

        # COLONNE 3: Merge (X = 1400)
        "Merge Inputs": [1400, 100],

        # COLONNE 4: Agent IA (X = 1900-2300, distribution verticale espacée)
        "Agent Dev Ideas": [2150, 100],
        "Claude Sonnet 4.5": [1900, 400],
        "MCP Client - Projects": [2150, 400],
        "Simple Memory": [2400, 400],

        # COLONNE 5: Sortie (X = 3000-3200)
        "Format Markdown for Telegram": [3000, 100],
        "Send Telegram Response": [3200, 100],
    }
}

# ============================================================================
# APPLY
# ============================================================================

def apply_layout(workflow_path, layout_config, name):
    print(f"🎨 Applying optimized spacing to: {name}")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Clear ALL sticky notes
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
            "typeVersion": 1,
            "position": sticky["position"],
            "id": f"sticky_{sticky['name'].replace(' ', '_').replace('🚀', '').replace('📦', '').replace('💡', '').replace('⚙️', '').replace('📨', '').replace('🎤', '').replace('📝', '').replace('🤖', '').replace('📤', '').replace('🔀', '')}",
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

    print(f"  ✅ {len(layout_config['sticky_notes'])} sticky notes ajoutées")
    print(f"  ✅ {repositioned} nodes repositionnés avec espacement optimisé")
    if not_found:
        print(f"  ℹ️ Nodes non trouvés: {', '.join(not_found)}")

def main():
    print("=" * 80)
    print("⚡ OPTIMIZED SPACING LAYOUT")
    print("=" * 80)
    print("\n✨ Optimisations:")
    print("  • Espacement VERTICAL de 200px (augmenté)")
    print("  • Espacement HORIZONTAL de 300px (réduit)")
    print("  • Branches vocale/texte séparées de 1000px")
    print("  • Flux plus compact horizontalement")
    print("  • Zero chevauchement garanti")

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
    print("✅ OPTIMIZED SPACING APPLIED - Vertical max, horizontal compact!")
    print("=" * 80)

if __name__ == "__main__":
    main()