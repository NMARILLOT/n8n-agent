#!/usr/bin/env python3
"""
SPACED HORIZONTAL FLOW - Flux horizontal avec BEAUCOUP d'espace
Aucun croisement, titres visibles, branches bien séparées
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT MCP - FLUX HORIZONTAL TRÈS ESPACÉ
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "🚀 TRIGGER",
            "content": """## 🚀 MCP SERVER TRIGGER

Point d'entrée du workflow
Configure l'URL SSE ici""",
            "position": [-1000, -400],
            "width": 400,
            "height": 1200,
            "color": 6  # Vert
        },
        {
            "name": "📦 EXPOSED TOOLS",
            "content": """## 📦 TOOLS EXPOSÉS VIA MCP

9 outils disponibles pour l'agent IA""",
            "position": [-500, -600],
            "width": 400,
            "height": 1600,
            "color": 4  # Bleu
        },
        {
            "name": "⚙️ BACKEND PROCESSING",
            "content": """## ⚙️ TRAITEMENT BACKEND

Opérations Notion et formatage""",
            "position": [0, -800],
            "width": 3800,
            "height": 2000,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # COLONNE 1: Trigger (X = -800)
        "MCP Server Trigger": [-800, 200],

        # COLONNE 2: Tools exposés (X = -300, espacement de 150px)
        "search_projects": [-300, -500],
        "get_project_by_id": [-300, -350],
        "list_categories": [-300, -200],
        "create_project": [-300, -50],
        "create_idea": [-300, 100],
        "search_ideas": [-300, 250],
        "get_idea_by_id": [-300, 400],
        "update_idea": [-300, 550],
        "delete_idea": [-300, 700],

        # COLONNE 3: Backend trigger et switch (X = 200 et 500)
        "Execute Workflow Trigger": [200, 200],
        "Switch Operation": [500, 200],

        # BRANCHES PARALLÈLES DU BACKEND (espacement vertical de 150px)

        # Branche 1: Search Projects (Y = -600)
        "Notion - Search Projects": [900, -600],
        "Format Search Projects": [1300, -600],

        # Branche 2: Get Project By ID (Y = -450)
        "Notion - Get Project By ID": [900, -450],
        "Format Get Project By ID": [1300, -450],

        # Branche 3: List Categories (Y = -300)
        "List Categories": [900, -300],

        # Branche 4: Search Ideas (Y = -150)
        "Notion - Search Ideas": [900, -150],
        "Format Search Ideas": [1300, -150],

        # Branche 5: Get Idea By ID (Y = 0)
        "Notion - Get Idea By ID": [900, 0],
        "Format Get Idea": [1300, 0],

        # Branche 6: Create Project (Y = 150)
        "Generate Project ID": [900, 150],
        "Notion - Create Project": [1300, 150],
        "Format Create Project Response": [1700, 150],

        # Branche 7: Create Idea (Y = 300)
        "Generate Idea ID": [900, 300],
        "Notion - Get Project For Idea": [1300, 300],
        "Find Project Page ID": [1700, 300],
        "Notion - Create Idea1": [2100, 300],
        "Format Create Idea Response": [2500, 300],

        # Branche 8: Update Idea (Y = 450)
        "Notion - Update Idea": [900, 450],
        "Prepare Update Idea": [1300, 450],
        "Notion - Update Idea Page": [1700, 450],
        "Format Update Response": [2100, 450],

        # Branche 9: Delete Idea (Y = 600)
        "Notion - Delete Idea": [900, 600],
        "Prepare Delete Idea": [1300, 600],
        "Format Delete Response": [1700, 600],
    }
}

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "📨 ENTRÉE",
            "content": """## 📨 ENTRÉE TELEGRAM

Messages entrants""",
            "position": [-1000, -200],
            "width": 400,
            "height": 600,
            "color": 6  # Vert
        },
        {
            "name": "🔀 ROUTING",
            "content": """## 🔀 ROUTING

Switch par type de message""",
            "position": [-500, -200],
            "width": 400,
            "height": 600,
            "color": 4  # Bleu
        },
        {
            "name": "🎤 BRANCHE VOCALE",
            "content": """## 🎤 TRAITEMENT VOCAL

Pipeline audio → texte""",
            "position": [0, -500],
            "width": 2000,
            "height": 400,
            "color": 5  # Violet
        },
        {
            "name": "📝 BRANCHE TEXTE",
            "content": """## 📝 TRAITEMENT TEXTE

Format direct""",
            "position": [0, 100],
            "width": 600,
            "height": 400,
            "color": 4  # Bleu clair
        },
        {
            "name": "🤖 AGENT IA",
            "content": """## 🤖 INTELLIGENCE ARTIFICIELLE

Claude + MCP + Memory""",
            "position": [2200, -300],
            "width": 1000,
            "height": 800,
            "color": 3  # Rouge
        },
        {
            "name": "📤 SORTIE",
            "content": """## 📤 RÉPONSE

Envoi Telegram""",
            "position": [3400, -200],
            "width": 700,
            "height": 600,
            "color": 7  # Orange
        }
    ],
    "nodes": {
        # COLONNE 1: Entrée (X = -800)
        "Telegram Trigger": [-800, 100],

        # COLONNE 2: Switch (X = -300)
        "Switch: Type d'entrée": [-300, 100],

        # BRANCHE HAUTE: Traitement vocal (Y = -300, espacement de 400px)
        "Get Audio File": [200, -300],
        "Download Audio": [600, -300],
        "Transcribe Audio": [1000, -300],
        "Format Audio Input": [1400, -300],

        # BRANCHE BASSE: Traitement texte (Y = 300)
        "Format Text Input": [300, 300],

        # COLONNE 3: Merge (X = 1900)
        "Merge Inputs": [1900, 100],

        # COLONNE 4: Agent IA (X = 2400-2800, distribution verticale)
        "Agent Dev Ideas": [2700, 100],
        "Claude Sonnet 4.5": [2400, 350],
        "MCP Client - Projects": [2700, 350],
        "Simple Memory": [3000, 350],

        # COLONNE 5: Sortie (X = 3600-3900)
        "Format Markdown for Telegram": [3750, 100],
        "Send Telegram Response": [4050, 100],
    }
}

# ============================================================================
# APPLY
# ============================================================================

def apply_layout(workflow_path, layout_config, name):
    print(f"🎨 Applying spaced horizontal flow to: {name}")

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
    print(f"  ✅ {repositioned} nodes repositionnés avec espacement généreux")
    if not_found:
        print(f"  ℹ️ Nodes non trouvés: {', '.join(not_found)}")

def main():
    print("=" * 80)
    print("🌊 SPACED HORIZONTAL FLOW LAYOUT")
    print("=" * 80)
    print("\n✨ Améliorations:")
    print("  • Espacement vertical de 150px minimum entre branches")
    print("  • Espacement horizontal de 400px entre colonnes")
    print("  • Aucun croisement de lignes")
    print("  • Titres des nodes toujours visibles")
    print("  • Branches parallèles bien séparées")

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
    print("✅ SPACED FLOW APPLIED - Espacement généreux, aucun croisement!")
    print("=" * 80)

if __name__ == "__main__":
    main()