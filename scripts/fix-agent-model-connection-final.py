#!/usr/bin/env python3
"""
FIX FINAL - Switch Agent from Claude to GPT-4o
Problème: L'agent utilise toujours Claude malgré l'ajout de GPT-4o
Solution: SUPPRIMER la connection Claude et connecter GPT-4o
"""

import json
from pathlib import Path

def fix_agent_model_connection():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    changes_made = []

    # 1. Trouver l'agent
    agent_node = None
    for node in workflow['nodes']:
        if node['type'] == '@n8n/n8n-nodes-langchain.agent':
            agent_node = node
            break

    if not agent_node:
        print("❌ Agent not found")
        return []

    agent_name = agent_node['name']

    # 2. Vérifier que GPT-4o existe
    gpt4o_exists = any(n['name'] == 'GPT-4o' for n in workflow['nodes'])

    if not gpt4o_exists:
        print("❌ GPT-4o node not found - run fix-agent-use-gpt4o.py first")
        return []

    # 3. MODIFIER les connections
    connections = workflow.get('connections', {})

    # Supprimer TOUTES les connections ai_languageModel vers l'agent
    print("🔍 Connections actuelles vers l'agent:")
    for source_name, conn_types in list(connections.items()):
        for conn_type, target_lists in list(conn_types.items()):
            if conn_type == 'ai_languageModel':
                # Filtrer les connections vers l'agent
                new_target_lists = []
                for target_list in target_lists:
                    filtered_targets = [t for t in target_list if t['node'] != agent_name]
                    if filtered_targets:
                        new_target_lists.append(filtered_targets)

                if new_target_lists:
                    conn_types[conn_type] = new_target_lists
                else:
                    del conn_types[conn_type]

                if source_name != 'GPT-4o':
                    print(f"  ❌ Supprimé: {source_name} --[ai_languageModel]--> Agent")
                    changes_made.append(f"✓ Supprimé connection Claude → Agent")

    # 4. AJOUTER la connection GPT-4o → Agent
    if 'GPT-4o' not in connections:
        connections['GPT-4o'] = {}

    connections['GPT-4o']['ai_languageModel'] = [[{
        "node": agent_name,
        "type": "ai_languageModel",
        "index": 0
    }]]

    print(f"  ✅ Ajouté: GPT-4o --[ai_languageModel]--> Agent")
    changes_made.append("✓ Connecté GPT-4o → Agent")

    # 5. Vérifier les credentials GPT-4o
    for node in workflow['nodes']:
        if node['name'] == 'GPT-4o':
            if 'credentials' not in node or not node['credentials']:
                node['credentials'] = {
                    "openAiApi": {
                        "id": "CONFIGURE_IN_N8N",
                        "name": "OpenAI account"
                    }
                }
                changes_made.append("⚠️  GPT-4o needs credentials configuration in n8n")

    # 6. Sauvegarder
    with open(workflow_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    return changes_made

def main():
    print()
    print("=" * 80)
    print("🔧 FIX FINAL - SWITCH AGENT MODEL TO GPT-4o")
    print("=" * 80)
    print()

    changes = fix_agent_model_connection()

    if not changes:
        print("❌ Fix failed")
        return

    print()
    print("Changements appliqués:")
    for change in changes:
        print(f"  {change}")
    print()
    print("=" * 80)
    print("✅ L'agent utilise MAINTENANT GPT-4o")
    print()
    print("IMPORTANT:")
    print("  Tu DOIS configurer les credentials OpenAI dans n8n:")
    print("  1. Ouvre https://auto.mhms.fr")
    print("  2. Workflow 'Agent Telegram - Dev Ideas'")
    print("  3. Clique sur node 'GPT-4o'")
    print("  4. Configure OpenAI API Key")
    print("  5. Sauvegarde")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()
