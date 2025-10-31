#!/usr/bin/env python3
"""
Script de FIX du layout visuel - VERSION RÉELLE
Basé sur l'analyse des screenshots - positions et tailles MASSIVES
"""

import json
from pathlib import Path

# ============================================================================
# CONFIGURATION RÉALISTE basée sur les screenshots
# ============================================================================

# Workflow 1: MCP - LAYOUT HORIZONTAL MASSIF avec GRANDES STICKY NOTES
MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "Usage Instructions",
            "content": """## 🚀 USAGE

**Obtiens l'URL SSE du serveur MCP:**
Ouvre le node "MCP Server Trigger" pour obtenir l'URL du serveur.

**Configure ton agent IA:**
Utilise cette URL dans Claude, ChatGPT, ou autre agent IA.

**9 outils disponibles:**
• 4 outils Projets (search, get, create, list)
• 5 outils Idées (create, search, get, update, delete)""",
            "position": [-800, -400],
            "width": 500,
            "height": 400,
            "color": 6
        },
        {
            "name": "Project Tools",
            "content": """## 📦 PROJECT TOOLS

**Gestion des projets MHMS:**

✅ search_projects - Recherche par mots-clés
✅ get_project_by_id - Détails d'un projet
✅ create_project - Nouveau projet
✅ list_categories - Liste des catégories""",
            "position": [400, -500],
            "width": 1400,
            "height": 600,
            "color": 4
        },
        {
            "name": "Idea Tools",
            "content": """## 💡 IDEA TOOLS

**Gestion des idées dans les projets:**

✅ create_idea - Nouvelle idée
✅ search_ideas - Recherche d'idées
✅ get_idea_by_id - Détails d'une idée
✅ update_idea - Modifier une idée
✅ delete_idea - Supprimer une idée (irréversible!)""",
            "position": [2200, -500],
            "width": 1400,
            "height": 600,
            "color": 5
        },
        {
            "name": "Internal Processing",
            "content": """## ⚙️ BACKEND PROCESSING

Traitement interne - Non exposé comme outils MCP

Switch → Notion Operations → Format → Return""",
            "position": [400, 400],
            "width": 3200,
            "height": 1400,
            "color": 7
        }
    ],
    "nodes": {
        # MCP Trigger visible en haut
        "MCP Server Trigger": [-200, -200],

        # === PROJECT TOOLS (Section bleue en haut) ===
        "search_projects": [600, -300],
        "get_project_by_id": [1000, -300],
        "list_categories": [1400, -300],
        "create_project": [600, 0],
        "create_idea": [1000, 0],

        # === IDEA TOOLS (Section violette en haut à droite) ===
        "search_ideas": [2400, -300],
        "get_idea_by_id": [2800, -300],
        "update_idea": [3200, -300],
        "delete_idea": [2400, 0],

        # === INTERNAL PROCESSING (Gros bloc en bas) ===
        "Execute Workflow Trigger": [600, 600],
        "Switch Operation": [1000, 600],

        # Branche search projects
        "Notion - Search Projects": [600, 900],
        "Format Search Projects": [600, 1200],

        # Branche get project
        "Notion - Get Project By ID": [1000, 900],
        "Format Get Project By ID": [1000, 1200],

        # Branche list categories
        "List Categories": [1400, 900],

        # Branche create project
        "Generate Project ID": [600, 1500],
        "Notion - Create Project": [1000, 1500],
        "Format Create Project Response": [1400, 1500],

        # Branche create idea
        "Generate Idea ID": [1800, 600],
        "Notion - Get Project For Idea": [1800, 900],
        "Find Project Page ID": [1800, 1200],
        "Notion - Create Idea1": [1800, 1500],
        "Format Create Idea Response": [2200, 1500],

        # Branche search ideas
        "Notion - Search Ideas": [2200, 600],
        "Format Search Ideas": [2200, 900],

        # Branche get idea
        "Notion - Get Idea By ID": [2600, 600],
        "Format Get Idea": [2600, 900],

        # Branche update idea
        "Notion - Update Idea": [2200, 1200],
        "Prepare Update Idea": [2200, 1500],
        "Notion - Update Idea Page": [2600, 1500],
        "Format Update Response": [3000, 1500],

        # Branche delete idea
        "Notion - Delete Idea": [2600, 1200],
        "Prepare Delete Idea": [3000, 1200],
        "Format Delete Response": [3000, 1500],
    }
}

# Workflow 2: Agent Telegram - LAYOUT HORIZONTAL ÉTALÉ
TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "Workflow Overview",
            "content": """## 🚀 AGENT TELEGRAM

**Capture automatique des idées depuis Telegram**

✅ Message texte → Traité directement
✅ Message vocal → Transcrit puis traité

L'agent IA analyse et crée/modifie dans Notion automatiquement.""",
            "position": [-1400, -600],
            "width": 700,
            "height": 400,
            "color": 6
        },
        {
            "name": "Input Processing",
            "content": """## 📨 RÉCEPTION

**Détection automatique:**

🎤 Vocal → Branche du haut
📝 Texte → Branche du bas

Une seule branche s'exécute""",
            "position": [-400, -600],
            "width": 600,
            "height": 350,
            "color": 4
        },
        {
            "name": "Vocal Branch",
            "content": """## 🎤 TRAITEMENT VOCAL

Étapes: Get Audio → Download → Transcribe (Whisper) → Format""",
            "position": [600, -1000],
            "width": 1800,
            "height": 300,
            "color": 5
        },
        {
            "name": "Text Branch",
            "content": """## 📝 TRAITEMENT TEXTE

Étapes: Format Text Input (direct)""",
            "position": [600, 400],
            "width": 600,
            "height": 250,
            "color": 7
        },
        {
            "name": "AI Processing",
            "content": """## 🤖 INTELLIGENCE ARTIFICIELLE

**Claude Sonnet 4.5** analyse et utilise:

🔧 MCP Client (Projets & Idées Notion)
💾 Simple Memory (Contexte)

Actions: Recherche, Crée, Modifie dans Notion""",
            "position": [2800, -600],
            "width": 800,
            "height": 500,
            "color": 3
        }
    ],
    "nodes": {
        # === INPUT SECTION ===
        "Telegram Trigger": [-600, 0],
        "Switch: Type d'entrée": [0, 0],

        # === VOCAL BRANCH (en haut, bien espacé) ===
        "Get Audio File": [700, -700],
        "Download Audio": [1100, -700],
        "Transcribe Audio": [1500, -700],
        "Format Audio Input": [1900, -700],

        # === TEXT BRANCH (en bas) ===
        "Format Text Input": [700, 500],

        # === MERGE POINT ===
        # Note: pas de Merge node, connexions directes

        # === AI PROCESSING (droite) ===
        "Agent Dev Ideas": [2800, 0],
        "Claude Sonnet 4.5": [2800, 350],
        "MCP Client - Projects": [3100, 350],
        "Simple Memory": [2950, 350],

        # === OUTPUT ===
        "Format Markdown for Telegram": [3800, 0],
        "Send Telegram Response": [4200, 0],
    }
}

# ============================================================================
# FONCTIONS
# ============================================================================

def clear_existing_sticky_notes(workflow):
    """Supprime toutes les sticky notes existantes"""
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']
    return workflow

def create_sticky_note(config):
    """Crée une sticky note"""
    return {
        "parameters": {
            "content": config["content"],
            "height": config["height"],
            "width": config["width"],
            "color": config.get("color", 4)
        },
        "type": "n8n-nodes-base.stickyNote",
        "position": config["position"],
        "id": f"sticky_{config['name'].lower().replace(' ', '_')}",
        "name": config["name"],
        "typeVersion": 1
    }

def reposition_nodes(workflow, positions):
    """Repositionne les nodes"""
    repositioned = 0
    for node in workflow['nodes']:
        node_name = node['name']
        if node_name in positions:
            old_pos = node['position']
            new_pos = positions[node_name]
            node['position'] = new_pos
            print(f"  ✅ {node_name}")
            repositioned += 1
    return workflow, repositioned

def apply_layout(workflow_path, layout_config):
    """Applique le layout"""

    print(f"\n🎨 {workflow_path.name}")
    print("=" * 80)

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # 1. Supprimer anciennes sticky notes
    workflow = clear_existing_sticky_notes(workflow)
    print(f"✅ Anciennes sticky notes supprimées")

    # 2. Ajouter nouvelles sticky notes GRANDES
    print(f"\n📌 Ajout des sticky notes:")
    for sticky_config in layout_config["sticky_notes"]:
        sticky_node = create_sticky_note(sticky_config)
        workflow['nodes'].append(sticky_node)
        print(f"  ✅ {sticky_config['name']} ({sticky_config['width']}x{sticky_config['height']}px, color: {sticky_config.get('color', 4)})")

    # 3. Repositionner les nodes avec BEAUCOUP d'espace
    print(f"\n📐 Repositionnement des nodes:")
    workflow, count = reposition_nodes(workflow, layout_config["nodes"])

    # 4. Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print(f"\n✨ TERMINÉ: {len(layout_config['sticky_notes'])} sticky notes + {count} nodes repositionnés")
    print()

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("🔧 FIX DU LAYOUT VISUEL - VERSION RÉELLE")
    print("Basé sur l'analyse des screenshots")
    print("Sticky notes GRANDES + Espacement MASSIF")
    print("=" * 80)

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Workflow 1: MCP Server
    mcp_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"
    if mcp_path.exists():
        apply_layout(mcp_path, MCP_LAYOUT)

    # Workflow 2: Agent Telegram
    telegram_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    if telegram_path.exists():
        apply_layout(telegram_path, TELEGRAM_LAYOUT)

    print("=" * 80)
    print("🎯 PROCHAINES ÉTAPES:")
    print("  1. Déploie: ./scripts/deploy.sh")
    print("  2. Rafraîchis n8n dans le navigateur")
    print("  3. Vérifie le résultat")
    print()

if __name__ == "__main__":
    main()
