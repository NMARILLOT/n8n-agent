#!/usr/bin/env python3
"""
Script de layout STYLE GMAIL MCP - Le vrai design professionnel
Sticky notes EN ARRIÈRE-PLAN + Layout en ÉTOILE + Nodes bien placés
"""

import json
from pathlib import Path

# ============================================================================
# LAYOUT STYLE GMAIL MCP - ÉTOILE DEPUIS LE CENTRE
# ============================================================================

MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "Usage",
            "content": """## USAGE

Open the MCP Server Trigger node to obtain the SSE server URL.

Use that to configure an N8N AI Agent flow or other AI tool.""",
            "position": [100, 800],
            "width": 600,
            "height": 280,
            "color": 6  # Vert pastel
        },
        {
            "name": "Project Tools",
            "content": """## PROJECT TOOLS""",
            "position": [900, -100],
            "width": 1000,
            "height": 500,
            "color": 4  # Bleu pastel
        },
        {
            "name": "Idea Tools",
            "content": """## IDEA TOOLS""",
            "position": [2100, -100],
            "width": 1000,
            "height": 500,
            "color": 5  # Violet pastel
        },
        {
            "name": "Backend Processing",
            "content": """## BACKEND PROCESSING""",
            "position": [900, 700],
            "width": 2200,
            "height": 1200,
            "color": 7  # Orange pastel
        }
    ],
    "nodes": {
        # === CENTRE: MCP Server Trigger ===
        "MCP Server Trigger": [800, 400],

        # === NORD (en haut): MCP TOOLS exposés ===
        # Rangée 1 - Project tools
        "search_projects": [1100, 80],
        "get_project_by_id": [1400, 80],
        "list_categories": [1700, 80],

        # Rangée 2 - Project tools (suite)
        "create_project": [1100, 280],
        "create_idea": [1400, 280],

        # Rangée 3 - Idea tools
        "search_ideas": [2300, 80],
        "get_idea_by_id": [2600, 80],
        "update_idea": [2900, 80],

        # Rangée 4 - Idea tools (suite)
        "delete_idea": [2300, 280],

        # === SUD (en bas): BACKEND PROCESSING ===
        "Execute Workflow Trigger": [1100, 900],
        "Switch Operation": [1100, 1100],

        # Colonne 1 - Search Projects
        "Notion - Search Projects": [1100, 1300],
        "Format Search Projects": [1100, 1500],

        # Colonne 2 - Get Project
        "Notion - Get Project By ID": [1400, 1300],
        "Format Get Project By ID": [1400, 1500],

        # Colonne 3 - List Categories
        "List Categories": [1700, 1300],

        # Colonne 4 - Create Project
        "Generate Project ID": [2000, 1300],
        "Notion - Create Project": [2000, 1500],
        "Format Create Project Response": [2000, 1700],

        # Colonne 5 - Create Idea
        "Generate Idea ID": [2300, 900],
        "Notion - Get Project For Idea": [2300, 1100],
        "Find Project Page ID": [2300, 1300],
        "Notion - Create Idea1": [2300, 1500],
        "Format Create Idea Response": [2300, 1700],

        # Colonne 6 - Search Ideas
        "Notion - Search Ideas": [2600, 1300],
        "Format Search Ideas": [2600, 1500],

        # Colonne 7 - Get Idea
        "Notion - Get Idea By ID": [2900, 1300],
        "Format Get Idea": [2900, 1500],

        # Colonne 8 - Update Idea
        "Notion - Update Idea": [1100, 1800],
        "Prepare Update Idea": [1400, 1800],
        "Notion - Update Idea Page": [1700, 1800],
        "Format Update Response": [2000, 1800],

        # Colonne 9 - Delete Idea
        "Notion - Delete Idea": [2300, 1800],
        "Prepare Delete Idea": [2600, 1800],
        "Format Delete Response": [2900, 1800],
    }
}

# ============================================================================
# TELEGRAM LAYOUT - FLUX HORIZONTAL CLAIR
# ============================================================================

TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "Agent Telegram Overview",
            "content": """## AGENT TELEGRAM - DEV IDEAS

Ce workflow capture automatiquement les idées depuis Telegram.

Support texte ET vocal.""",
            "position": [-800, -200],
            "width": 600,
            "height": 380,
            "color": 6  # Vert
        },
        {
            "name": "Input Processing",
            "content": """## RÉCEPTION DU MESSAGE

Le Switch détecte automatiquement:
🎤 Vocal → Branche du haut
📝 Texte → Branche du bas""",
            "position": [-100, -200],
            "width": 500,
            "height": 380,
            "color": 4  # Bleu
        },
        {
            "name": "Vocal Branch",
            "content": """## TRAITEMENT VOCAL

Étapes: Get Audio → Download → Transcribe → Format""",
            "position": [600, -600],
            "width": 1600,
            "height": 280,
            "color": 5  # Violet
        },
        {
            "name": "Text Branch",
            "content": """## TRAITEMENT TEXTE

Format direct du texte""",
            "position": [600, 300],
            "width": 500,
            "height": 200,
            "color": 7  # Orange
        },
        {
            "name": "AI Processing",
            "content": """## INTELLIGENCE ARTIFICIELLE

Claude Sonnet 4.5 analyse et utilise:
• MCP Client (Projets & Idées)
• Simple Memory (Contexte)""",
            "position": [2400, -200],
            "width": 800,
            "height": 380,
            "color": 3  # Rouge
        }
    ],
    "nodes": {
        # === INPUT ===
        "Telegram Trigger": [-400, 0],
        "Switch: Type d'entrée": [0, 0],

        # === VOCAL BRANCH (en haut) ===
        "Get Audio File": [700, -400],
        "Download Audio": [1000, -400],
        "Transcribe Audio": [1300, -400],
        "Format Audio Input": [1600, -400],

        # === TEXT BRANCH (en bas) ===
        "Format Text Input": [700, 400],

        # === AI PROCESSING ===
        "Agent Dev Ideas": [2400, 0],

        # Outils sous l'agent (en ligne)
        "Claude Sonnet 4.5": [2200, 300],
        "Simple Memory": [2400, 300],
        "MCP Client - Projects": [2600, 300],

        # === OUTPUT ===
        "Format Markdown for Telegram": [3400, 0],
        "Send Telegram Response": [3700, 0],
    }
}

# ============================================================================
# FONCTIONS
# ============================================================================

def clear_sticky_notes(workflow):
    """Supprime les sticky notes"""
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']
    return workflow

def create_sticky(config):
    """Crée une sticky note"""
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
    """Repositionne les nodes"""
    count = 0
    for node in workflow['nodes']:
        if node['name'] in positions:
            node['position'] = positions[node['name']]
            count += 1
    return count

def apply_layout(workflow_path, layout_config, workflow_name):
    """Applique le layout"""

    print(f"\n{'=' * 80}")
    print(f"🎨 {workflow_name}")
    print('=' * 80)

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # Supprimer anciennes sticky notes
    workflow = clear_sticky_notes(workflow)
    print("✅ Anciennes sticky notes supprimées")

    # Ajouter nouvelles sticky notes
    print(f"\n📌 Création des sticky notes:")
    for sticky_config in layout_config["sticky_notes"]:
        sticky_node = create_sticky(sticky_config)
        workflow['nodes'].append(sticky_node)
        print(f"  • {sticky_config['name']} ({sticky_config['width']}x{sticky_config['height']}px)")

    # Repositionner les nodes
    print(f"\n📐 Repositionnement des nodes...")
    count = reposition_nodes(workflow, layout_config["nodes"])
    print(f"  ✅ {count} nodes repositionnés")

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"\n✨ Layout appliqué avec succès!")

def main():
    print("=" * 80)
    print("🎨 LAYOUT STYLE GMAIL MCP - Version Finale")
    print("=" * 80)
    print("\n✨ Design:")
    print("  • Sticky notes EN ARRIÈRE-PLAN (pastels)")
    print("  • Layout en ÉTOILE pour MCP")
    print("  • Flux HORIZONTAL pour Telegram")
    print("  • Texte MINIMAL et lisible")
    print("  • Nodes BIEN ESPACÉS")

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # MCP Workflow
    mcp_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"
    if mcp_path.exists():
        apply_layout(mcp_path, MCP_LAYOUT, "MCP - Idée Dev Nico (Perso)")
    else:
        print(f"⚠️ MCP workflow non trouvé")

    # Telegram Workflow
    telegram_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    if telegram_path.exists():
        apply_layout(telegram_path, TELEGRAM_LAYOUT, "Agent Telegram - Dev Ideas")
    else:
        print(f"⚠️ Telegram workflow non trouvé")

    print("\n" + "=" * 80)
    print("🎯 PROCHAINES ÉTAPES:")
    print("  1. Déploie: ./scripts/deploy.sh")
    print("  2. Rafraîchis n8n (F5)")
    print("  3. Admire le résultat! 🚀")
    print("=" * 80)

if __name__ == "__main__":
    main()
