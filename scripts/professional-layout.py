#!/usr/bin/env python3
"""
Script de restructuration professionnelle des workflows n8n
Inspiré du workflow Gmail MCP - Design ultra-propre et organisé
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple

# ============================================================================
# CONFIGURATION DES LAYOUTS PROFESSIONNELS
# ============================================================================

# Workflow 1: MCP - Idée Dev Nico (Perso)
MCP_LAYOUT = {
    "sticky_notes": [
        {
            "name": "Usage Instructions",
            "content": """## 🚀 USAGE

Open the MCP Server Trigger node to obtain the SSE server URL.

Use that URL to configure your AI Agent (Claude, ChatGPT, etc.) to interact with your Notion projects and ideas.

**Available Tools:**
• 5 Project Management Tools
• 5 Idea Management Tools""",
            "position": [240, 100],
            "width": 400,
            "height": 280,
            "color": 6
        },
        {
            "name": "Project Tools Section",
            "content": """## 📦 PROJECT TOOLS

Manage your MHMS projects database:
• Search projects by keywords
• Get detailed project info
• Create new projects
• List available categories""",
            "position": [720, 100],
            "width": 600,
            "height": 440,
            "color": 4
        },
        {
            "name": "Idea Tools Section",
            "content": """## 💡 IDEA TOOLS

Manage ideas within projects:
• Create new ideas
• Search existing ideas
• Update idea content
• Delete ideas (irreversible!)
• Get idea details""",
            "position": [1400, 100],
            "width": 600,
            "height": 560,
            "color": 5
        },
        {
            "name": "Internal Processing",
            "content": """## ⚙️ INTERNAL PROCESSING

Backend nodes handling operations.
Not exposed as MCP tools.""",
            "position": [720, 700],
            "width": 1280,
            "height": 680,
            "color": 7
        }
    ],
    "nodes": {
        # MCP Server Trigger (en haut à gauche, visible)
        "MCP Server Trigger": [360, 300],

        # === PROJECT TOOLS (Section bleue) ===
        "search_projects": [800, 200],
        "get_project_by_id": [960, 200],
        "list_categories": [1120, 200],
        "create_project": [800, 360],
        "create_idea": [960, 360],

        # === IDEA TOOLS (Section violette) ===
        "search_ideas": [1480, 200],
        "get_idea_by_id": [1640, 200],
        "update_idea": [1800, 200],
        "delete_idea": [1480, 360],

        # === INTERNAL PROCESSING (Section orange, en bas) ===
        "Execute Workflow Trigger": [800, 800],
        "Switch Operation": [1000, 800],

        # Branche search projects
        "Notion - Search Projects": [800, 960],
        "Format Search Projects": [800, 1120],

        # Branche get project
        "Notion - Get Project By ID": [1000, 960],
        "Format Get Project By ID": [1000, 1120],

        # Branche list categories
        "List Categories": [1200, 960],

        # Branche create project
        "Generate Project ID": [800, 1280],
        "Notion - Create Project": [1000, 1280],
        "Format Create Project Response": [1200, 1280],

        # Branche create idea
        "Generate Idea ID": [1400, 800],
        "Notion - Get Project For Idea": [1400, 960],
        "Find Project Page ID": [1400, 1120],
        "Notion - Create Idea1": [1400, 1280],
        "Format Create Idea Response": [1600, 1280],

        # Branche search ideas
        "Notion - Search Ideas": [1600, 800],
        "Format Search Ideas": [1600, 960],

        # Branche get idea
        "Notion - Get Idea By ID": [1800, 800],
        "Format Get Idea": [1800, 960],

        # Branche update idea
        "Notion - Update Idea": [1600, 1120],
        "Prepare Update Idea": [1600, 1280],
        "Notion - Update Idea Page": [1800, 1280],
        "Format Update Response": [2000, 1280],

        # Branche delete idea
        "Notion - Delete Idea": [1800, 1120],
        "Prepare Delete Idea": [2000, 1120],
        "Format Delete Response": [2000, 1280],
    }
}

# Workflow 2: Agent Telegram - Dev Ideas
TELEGRAM_LAYOUT = {
    "sticky_notes": [
        {
            "name": "Workflow Overview",
            "content": """## 🚀 AGENT TELEGRAM - DEV IDEAS

**Ce workflow capture automatiquement tes idées depuis Telegram**

✅ Message texte → Traité directement
✅ Message vocal → Transcrit puis traité

L'agent IA analyse ton message et crée/modifie des projets et idées dans Notion.""",
            "position": [-600, -500],
            "width": 500,
            "height": 320,
            "color": 6
        },
        {
            "name": "Input Processing",
            "content": """## 📨 RÉCEPTION DU MESSAGE

**Le Switch détecte automatiquement le type:**

🎤 Message vocal → Branche du haut
📝 Message texte → Branche du bas

⚠️ Une seule branche s'exécute à la fois""",
            "position": [100, -500],
            "width": 400,
            "height": 280,
            "color": 4
        },
        {
            "name": "Vocal Branch",
            "content": """## 🎤 TRAITEMENT VOCAL

**Étapes:**
1. Récupère le fichier audio
2. Télécharge depuis Telegram
3. Transcrit avec Whisper
4. Formate pour l'agent""",
            "position": [600, -700],
            "width": 850,
            "height": 200,
            "color": 5
        },
        {
            "name": "Text Branch",
            "content": """## 📝 TRAITEMENT TEXTE

**Étapes:**
1. Formate directement le texte
2. Prêt pour l'agent""",
            "position": [600, 150],
            "width": 400,
            "height": 180,
            "color": 7
        },
        {
            "name": "AI Processing",
            "content": """## 🤖 AGENT INTELLIGENCE ARTIFICIELLE

**Claude Sonnet 4.5** analyse ton message et:

🔍 Cherche des projets similaires (MCP)
💾 Sauvegarde le contexte (Memory)
📝 Crée/modifie dans Notion
✅ Répond sur Telegram

**Outils disponibles:**
• MCP Client (Notion Projects & Ideas)
• Simple Memory (Contexte conversation)""",
            "position": [1600, -500],
            "width": 500,
            "height": 420,
            "color": 3
        }
    ],
    "nodes": {
        # === INPUT SECTION ===
        "Telegram Trigger": [-400, 0],
        "Switch: Type d'entrée": [0, 0],

        # === VOCAL BRANCH (en haut) ===
        "Get Audio File": [600, -500],
        "Download Audio": [800, -500],
        "Transcribe Audio": [1000, -500],
        "Format Audio Input": [1200, -500],

        # === TEXT BRANCH (en bas) ===
        "Format Text Input": [600, 200],

        # === AI PROCESSING (droite) ===
        "Agent Dev Ideas": [1600, 0],
        "Claude Sonnet 4.5": [1600, 280],
        "MCP Client - Projects": [1800, 280],
        "Simple Memory": [1700, 280],

        # === OUTPUT ===
        "Format Markdown for Telegram": [2200, 0],
        "Send Telegram Response": [2400, 0],
    }
}

# ============================================================================
# FONCTIONS DE TRAITEMENT
# ============================================================================

def clear_existing_sticky_notes(workflow: Dict) -> Dict:
    """Supprime toutes les sticky notes existantes"""
    workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']
    return workflow

def create_sticky_note(config: Dict) -> Dict:
    """Crée une sticky note avec la config donnée"""
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

def reposition_nodes(workflow: Dict, positions: Dict[str, Tuple[int, int]]) -> Dict:
    """Repositionne les nodes selon la config"""
    for node in workflow['nodes']:
        node_name = node['name']
        if node_name in positions:
            old_pos = node['position']
            new_pos = positions[node_name]
            node['position'] = new_pos
            print(f"  ✅ {node_name}: {old_pos} → {new_pos}")
    return workflow

def apply_professional_layout(workflow_path: Path, layout_config: Dict) -> None:
    """Applique un layout professionnel à un workflow"""

    print(f"\n🎨 Application du layout professionnel: {workflow_path.name}")
    print("=" * 80)

    # Charger le workflow
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    # 1. Supprimer les anciennes sticky notes
    print("\n1️⃣ Suppression des anciennes sticky notes...")
    workflow = clear_existing_sticky_notes(workflow)
    print("  ✅ Anciennes sticky notes supprimées")

    # 2. Ajouter les nouvelles sticky notes
    print("\n2️⃣ Ajout des nouvelles sticky notes professionnelles...")
    for sticky_config in layout_config["sticky_notes"]:
        sticky_node = create_sticky_note(sticky_config)
        workflow['nodes'].append(sticky_node)
        print(f"  ✅ {sticky_config['name']} (color: {sticky_config.get('color', 4)})")

    # 3. Repositionner les nodes
    print("\n3️⃣ Repositionnement des nodes sur la grille professionnelle...")
    workflow = reposition_nodes(workflow, layout_config["nodes"])

    # 4. Sauvegarder
    print("\n4️⃣ Sauvegarde du workflow...")
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    print("  ✅ Workflow sauvegardé")

    # 5. Résumé
    print("\n" + "=" * 80)
    print("✨ LAYOUT PROFESSIONNEL APPLIQUÉ AVEC SUCCÈS!")
    print(f"  📊 {len(layout_config['sticky_notes'])} sticky notes créées")
    print(f"  📦 {len(layout_config['nodes'])} nodes repositionnés")
    print()

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("🎨 RESTRUCTURATION PROFESSIONNELLE DES WORKFLOWS N8N")
    print("Inspiré du workflow Gmail MCP - Design ultra-propre")
    print("=" * 80)

    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Workflow 1: MCP Server
    mcp_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"
    if mcp_path.exists():
        apply_professional_layout(mcp_path, MCP_LAYOUT)
    else:
        print(f"⚠️ Workflow MCP non trouvé: {mcp_path}")

    # Workflow 2: Agent Telegram
    telegram_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "Agent Telegram - Dev Ideas.json"
    if telegram_path.exists():
        apply_professional_layout(telegram_path, TELEGRAM_LAYOUT)
    else:
        print(f"⚠️ Workflow Telegram non trouvé: {telegram_path}")

    print("\n" + "=" * 80)
    print("🎯 PROCHAINES ÉTAPES:")
    print("  1. Ouvre les workflows dans n8n pour voir le résultat")
    print("  2. Ajuste les positions manuellement si besoin")
    print("  3. Déploie avec: ./scripts/deploy.sh")
    print()

if __name__ == "__main__":
    main()
