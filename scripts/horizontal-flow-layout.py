#!/usr/bin/env python3
"""
HORIZONTAL FLOW LAYOUT - Flux gauche → droite avec branches parallèles
Comme un vrai workflow professionnel avec des lignes de connexion propres
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT MCP - FLUX HORIZONTAL AVEC BRANCHES PARALLÈLES
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "🚀 TRIGGER",
            "content": """## 🚀 MCP SERVER TRIGGER

Point d'entrée du workflow
Configure l'URL SSE ici""",
            "position": [-800, -200],
            "width": 400,
            "height": 600,
            "color": 6  # Vert
        },
        {
            "name": "📦 EXPOSED TOOLS",
            "content": """## 📦 TOOLS EXPOSÉS VIA MCP

9 outils disponibles pour l'agent IA""",
            "position": [-300, -400],
            "width": 600,
            "height": 1000,
            "color": 4  # Bleu
        },
        {
            "name": "⚙️ BACKEND PROCESSING",
            "content": """## ⚙️ TRAITEMENT BACKEND

Opérations Notion et formatage""",
            "position": [400, -600],
            "width": 3000,
            "height": 1400,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # COLONNE 1: Trigger (X = -600)
        "MCP Server Trigger": [-600, 100],

        # COLONNE 2: Tools exposés (X = -100, branches parallèles)
        "search_projects": [-100, -300],
        "get_project_by_id": [-100, -200],
        "list_categories": [-100, -100],
        "create_project": [-100, 0],
        "create_idea": [-100, 100],
        "search_ideas": [-100, 200],
        "get_idea_by_id": [-100, 300],
        "update_idea": [-100, 400],
        "delete_idea": [-100, 500],

        # COLONNE 3: Backend trigger et switch (X = 600)
        "Execute Workflow Trigger": [600, 100],
        "Switch Operation": [900, 100],

        # BRANCHES PARALLÈLES DU BACKEND (flux horizontal)

        # Branche 1: Search Projects (Y = -400)
        "Notion - Search Projects": [1200, -400],
        "Format Search Projects": [1500, -400],

        # Branche 2: Get Project By ID (Y = -300)
        "Notion - Get Project By ID": [1200, -300],
        "Format Get Project By ID": [1500, -300],

        # Branche 3: Search Ideas (Y = -200)
        "Notion - Search Ideas": [1200, -200],
        "Format Search Ideas": [1500, -200],

        # Branche 4: Get Idea By ID (Y = -100)
        "Notion - Get Idea By ID": [1200, -100],
        "Format Get Idea": [1500, -100],

        # Branche 5: Update Idea (Y = 0)
        "Notion - Update Idea": [1200, 0],
        "Prepare Update Idea": [1500, 0],
        "Notion - Update Idea Page": [1800, 0],
        "Format Update Response": [2100, 0],

        # Branche 6: Delete Idea (Y = 100)
        "Notion - Delete Idea": [1200, 100],
        "Prepare Delete Idea": [1500, 100],
        "Format Delete Response": [1800, 100],

        # Branche 7: Create Project (Y = 200)
        "Generate Project ID": [1200, 200],
        "Notion - Create Project": [1500, 200],
        "Format Create Project Response": [1800, 200],

        # Branche 8: Create Idea (Y = 300)
        "Generate Idea ID": [1200, 300],
        "Notion - Get Project For Idea": [1500, 300],
        "Find Project Page ID": [1800, 300],
        "Notion - Create Idea1": [2100, 300],
        "Format Create Idea Response": [2400, 300],

        # Branche 9: List Categories (Y = 400)
        "List Categories": [1200, 400],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "📨 ENTRÉE",
            "content": """## 📨 ENTRÉE TELEGRAM

Messages entrants""",
            "position": [-800, -200],
            "width": 400,
            "height": 600,
            "color": 6  # Vert
        },
        {
            "name": "🔀 ROUTING",
            "content": """## 🔀 ROUTING

Switch par type de message""",
            "position": [-300, -200],
            "width": 400,
            "height": 600,
            "color": 4  # Bleu
        },
        {
            "name": "🎤 BRANCHE VOCALE",
            "content": """## 🎤 TRAITEMENT VOCAL

Pipeline audio → texte""",
            "position": [200, -400],
            "width": 1600,
            "height": 300,
            "color": 5  # Violet
        },
        {
            "name": "📝 BRANCHE TEXTE",
            "content": """## 📝 TRAITEMENT TEXTE

Format direct""",
            "position": [200, 0],
            "width": 400,
            "height": 300,
            "color": 4  # Bleu clair
        },
        {
            "name": "🤖 AGENT IA",
            "content": """## 🤖 INTELLIGENCE ARTIFICIELLE

Claude + MCP + Memory""",
            "position": [1900, -200],
            "width": 800,
            "height": 600,
            "color": 3  # Rouge
        },
        {
            "name": "📤 SORTIE",
            "content": """## 📤 RÉPONSE

Envoi Telegram""",
            "position": [2800, -200],
            "width": 600,
            "height": 600,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # COLONNE 1: Entrée (X = -600)
        "Telegram Trigger": [-600, 100],

        # COLONNE 2: Switch (X = -100)
        "Switch: Type d'entrée": [-100, 100],

        # BRANCHE HAUTE: Traitement vocal (Y = -250)
        "Get Audio File": [400, -250],
        "Download Audio": [700, -250],
        "Transcribe Audio": [1000, -250],
        "Format Audio Input": [1300, -250],

        # BRANCHE BASSE: Traitement texte (Y = 150)
        "Format Text Input": [400, 150],

        # COLONNE 3: Merge (X = 1600) - si ce node existe
        "Merge Inputs": [1600, 100],

        # COLONNE 4: Agent IA (X = 2100, distribution verticale)
        "Agent Dev Ideas": [2300, 100],
        "Claude Sonnet 4.5": [2100, 250],
        "MCP Client - Projects": [2300, 250],
        "Simple Memory": [2500, 250],

        # COLONNE 5: Sortie (X = 3000)
        "Format Markdown for Telegram": [3100, 100],
        "Send Telegram Response": [3400, 100],
    }
}

# ============================================================================
# APPLY
# ============================================================================

def apply_layout(workflow_path, layout_config, name):
    print(f"🎨 Applying horizontal flow to: {name}")

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
    print(f"  ✅ {repositioned} nodes repositionnés en flux horizontal")
    if not_found:
        print(f"  ℹ️ Nodes non trouvés: {', '.join(not_found)}")

def main():
    print("=" * 80)
    print("🌊 HORIZONTAL FLOW LAYOUT")
    print("=" * 80)
    print("\n✨ Principe:")
    print("  • Flux gauche → droite")
    print("  • Branches parallèles propres")
    print("  • Connexions alignées horizontalement")
    print("  • Pas de croisements de lignes")
    print("  • Organisation en colonnes verticales")

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
    print("✅ HORIZONTAL FLOW APPLIED - Flux propre de gauche à droite!")
    print("=" * 80)

if __name__ == "__main__":
    main()