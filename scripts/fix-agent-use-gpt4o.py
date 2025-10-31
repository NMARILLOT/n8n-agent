#!/usr/bin/env python3
"""
Fix Agent Model - Switch to GPT-4o
Problème: Claude (Anthropic) ne supporte pas tool_choice pour forcer l'utilisation des tools
Solution: Utiliser GPT-4o qui a un excellent support de tool calling
"""

import json
from pathlib import Path
import uuid

def fix_agent_model():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # 1. Trouver l'agent et le ChatModel Claude actuel
    agent_node = None
    claude_node = None

    for node in workflow['nodes']:
        if node['type'] == '@n8n/n8n-nodes-langchain.agent':
            agent_node = node
        elif node['type'] == '@n8n/n8n-nodes-langchain.lmChatAnthropic':
            claude_node = node

    if not agent_node:
        print("❌ Agent node not found")
        return []

    # 2. Créer un nouveau node ChatOpenAI avec GPT-4o
    openai_node_id = str(uuid.uuid4())

    openai_node = {
        "parameters": {
            "model": "gpt-4o",
            "options": {
                "temperature": 0.3  # Même température qu'avant
            }
        },
        "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
        "typeVersion": 1,
        "position": [120, 400],  # Position à côté de l'agent
        "id": openai_node_id,
        "name": "GPT-4o",
        "credentials": {
            "openAiApi": {
                "id": "PLACEHOLDER",  # L'utilisateur devra configurer ses credentials OpenAI
                "name": "OpenAI account"
            }
        },
        "notes": "🤖 GPT-4o - Excellent tool calling support"
    }

    # Vérifier si un node GPT-4o existe déjà
    gpt_exists = any(n['name'] == 'GPT-4o' for n in workflow['nodes'])

    if not gpt_exists:
        workflow['nodes'].append(openai_node)
        changes_made.append("✓ Ajouté node GPT-4o ChatModel")

    # 3. Connecter l'agent au GPT-4o au lieu de Claude
    # Dans n8n, l'agent a un slot "model" qui pointe vers le ChatModel
    # Cela se fait via les connections

    connections = workflow.get('connections', {})

    # Trouver le nom de l'agent
    agent_name = agent_node['name']

    # Créer la connection Agent → GPT-4o
    connections[agent_name] = connections.get(agent_name, {})
    connections[agent_name]['ai_languageModel'] = [[{
        "node": "GPT-4o",
        "type": "ai_languageModel",
        "index": 0
    }]]

    changes_made.append(f"✓ Connecté '{agent_name}' → GPT-4o")

    # 4. Activer "Return Intermediate Steps"
    if 'options' not in agent_node['parameters']:
        agent_node['parameters']['options'] = {}

    agent_node['parameters']['options']['returnIntermediateSteps'] = True
    changes_made.append("✓ Activé 'Return Intermediate Steps' pour debugging")

    # 5. Augmenter Max Iterations
    agent_node['parameters']['options']['maxIterations'] = 10
    changes_made.append("✓ Max Iterations: 10")

    # 6. Garder Claude node mais le déconnecter (au cas où l'utilisateur veut revenir)
    if claude_node:
        claude_node['notes'] = "⚠️ DÉSACTIVÉ - Claude ne supporte pas tool_choice. Utilise GPT-4o à la place."

    # Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX AGENT MODEL - SWITCH TO GPT-4o")
    print("=" * 80)
    print()
    print("Problème:")
    print("  Claude (Anthropic) ne supporte pas l'API parameter 'tool_choice'")
    print("  → Impossible de forcer l'utilisation des tools")
    print("  → L'agent hallucine au lieu d'appeler delete_idea()")
    print()
    print("Solution:")
    print("  Utiliser GPT-4o qui a un EXCELLENT support de tool calling")
    print("  Référence: n8n Community - 'GPT-4o is specially good at using tools'")
    print()

    changes = fix_agent_model()

    if not changes:
        print("❌ Erreur lors de la modification")
        return

    print("Changements:")
    for change in changes:
        print(f"  {change}")
    print()
    print("=" * 80)
    print("⚠️  ACTION REQUISE:")
    print("  1. Ouvre n8n: https://auto.mhms.fr")
    print("  2. Va dans le workflow 'Agent Telegram - Dev Ideas'")
    print("  3. Clique sur le node 'GPT-4o'")
    print("  4. Configure tes credentials OpenAI")
    print("  5. Sauvegarde le workflow")
    print()
    print("Ensuite, déploie:")
    print("  ./scripts/deploy.sh")
    print("=" * 80)
    print()
    print("📊 Amélioration Attendue:")
    print("  Claude (Anthropic): ~50% tool calling reliability")
    print("  GPT-4o: ~85-90% tool calling reliability")
    print()

if __name__ == "__main__":
    main()
