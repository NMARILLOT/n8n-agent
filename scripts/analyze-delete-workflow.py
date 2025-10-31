#!/usr/bin/env python3
"""
Analyse complète du workflow delete_idea pour trouver pourquoi il ne retourne pas de réponse
"""

import json
from pathlib import Path

def analyze_delete_workflow():
    workflow_path = Path("Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json")

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    print("=" * 80)
    print("🔍 ANALYSE COMPLÈTE DU WORKFLOW delete_idea")
    print("=" * 80)
    print()

    # 1. Vérifier le flux complet
    print("1. FLUX D'EXÉCUTION")
    print("-" * 80)

    connections = workflow['connections']
    nodes_dict = {node['name']: node for node in workflow['nodes']}

    # Trouver le flux depuis Switch
    switch_outputs = connections.get('Switch Operation', {}).get('main', [])
    if len(switch_outputs) > 8 and switch_outputs[8]:
        current = switch_outputs[8][0]['node']
        step = 1

        while current:
            node = nodes_dict.get(current)
            if not node:
                print(f"❌ ERREUR: Node '{current}' n'existe pas!")
                break

            print(f"\n{step}. {current}")
            print(f"   Type: {node['type']}")
            print(f"   ID: {node['id']}")

            # Afficher les paramètres clés
            if 'parameters' in node:
                params = node['parameters']
                if 'operation' in params:
                    print(f"   Operation: {params['operation']}")
                if 'databaseId' in params:
                    db_id = params['databaseId'].get('value', 'N/A')
                    print(f"   Database ID: {db_id}")
                if 'jsCode' in params:
                    code = params['jsCode']
                    print(f"   Code: {code[:100]}...")

            # Connexion suivante
            if current in connections and 'main' in connections[current]:
                next_nodes = connections[current]['main']
                if next_nodes and next_nodes[0]:
                    current = next_nodes[0][0]['node']
                    step += 1
                else:
                    print(f"\n   → FIN (pas de connexion sortante)")
                    break
            else:
                print(f"\n   → FIN (pas de connexion sortante)")
                break

    print()
    print("=" * 80)
    print("2. VÉRIFICATION DES DATABASES")
    print("-" * 80)

    # Trouver les database IDs
    db_ids = {}
    for node in workflow['nodes']:
        if 'parameters' in node and 'databaseId' in node['parameters']:
            db_id = node['parameters']['databaseId'].get('value', 'N/A')
            if db_id not in db_ids:
                db_ids[db_id] = []
            db_ids[db_id].append(node['name'])

    print(f"\nDatabases utilisées:")
    for db_id, node_names in db_ids.items():
        print(f"\n  Database: {db_id}")
        for name in node_names:
            print(f"    • {name}")

    print()
    print("=" * 80)
    print("3. ANALYSE DU CODE JS")
    print("-" * 80)

    # Analyser Prepare Delete Idea
    prepare_node = nodes_dict.get('Prepare Delete Idea')
    if prepare_node and 'jsCode' in prepare_node['parameters']:
        code = prepare_node['parameters']['jsCode']
        print(f"\nCode de 'Prepare Delete Idea':")
        print(code)
        print()

        # Vérifier les références
        if "$('Notion - Get Ideas For Delete')" in code:
            print("✅ Référence correcte: $('Notion - Get Ideas For Delete')")
        else:
            print("❌ Référence incorrecte dans le code!")

    # Analyser Format Delete Response
    format_node = nodes_dict.get('Format Delete Response')
    if format_node and 'jsCode' in format_node['parameters']:
        code = format_node['parameters']['jsCode']
        print(f"\nCode de 'Format Delete Response':")
        print(code)
        print()

        # Vérifier qu'il retourne bien { response }
        if "{ response }" in code or "{ json: { response } }" in code:
            print("✅ Retourne bien { json: { response } }")
        else:
            print("❌ Ne retourne pas le bon format!")

    print()
    print("=" * 80)
    print("4. COMPARAISON AVEC update_idea (QUI FONCTIONNE)")
    print("-" * 80)

    # Comparer avec update_idea
    update_flow = []
    if len(switch_outputs) > 7 and switch_outputs[7]:
        current = switch_outputs[7][0]['node']
        while current:
            update_flow.append(current)
            if current in connections and 'main' in connections[current]:
                next_nodes = connections[current]['main']
                if next_nodes and next_nodes[0]:
                    current = next_nodes[0][0]['node']
                else:
                    break
            else:
                break

    delete_flow = []
    if len(switch_outputs) > 8 and switch_outputs[8]:
        current = switch_outputs[8][0]['node']
        while current:
            delete_flow.append(current)
            if current in connections and 'main' in connections[current]:
                next_nodes = connections[current]['main']
                if next_nodes and next_nodes[0]:
                    current = next_nodes[0][0]['node']
                else:
                    break
            else:
                break

    print(f"\nFlux update_idea ({len(update_flow)} nodes):")
    for i, node_name in enumerate(update_flow, 1):
        print(f"  {i}. {node_name}")

    print(f"\nFlux delete_idea ({len(delete_flow)} nodes):")
    for i, node_name in enumerate(delete_flow, 1):
        print(f"  {i}. {node_name}")

    print()
    print("=" * 80)
    print("5. DIAGNOSTIC FINAL")
    print("-" * 80)
    print()

    issues = []

    # Vérifier que tous les nodes existent
    for node_name in delete_flow:
        if node_name not in nodes_dict:
            issues.append(f"❌ Node '{node_name}' n'existe pas dans le workflow")

    # Vérifier la database
    get_ideas_node = nodes_dict.get('Notion - Get Ideas For Delete')
    if get_ideas_node:
        db_id = get_ideas_node['parameters']['databaseId'].get('value', 'N/A')
        # Comparer avec Notion - Search Ideas
        search_ideas_node = nodes_dict.get('Notion - Search Ideas')
        if search_ideas_node:
            search_db_id = search_ideas_node['parameters']['databaseId'].get('value', 'N/A')
            if db_id == search_db_id:
                print(f"✅ Database correcte: {db_id}")
            else:
                issues.append(f"❌ Database différente: Get Ideas For Delete ({db_id}) vs Search Ideas ({search_db_id})")

    # Vérifier que Format Delete Response existe et a le bon format
    if 'Format Delete Response' in nodes_dict:
        print(f"✅ Node 'Format Delete Response' existe")
    else:
        issues.append(f"❌ Node 'Format Delete Response' n'existe pas")

    if issues:
        print("\n⚠️  PROBLÈMES IDENTIFIÉS:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("\n✅ Structure du workflow semble correcte")
        print("\n⚠️  HYPOTHÈSE: Le problème vient probablement d'une ERREUR D'EXÉCUTION")
        print("    - Peut-être que 'Prepare Delete Idea' ne trouve pas l'idée")
        print("    - Peut-être une erreur dans 'Notion - Archive Idea'")
        print("    - BESOIN DES LOGS D'EXÉCUTION n8n pour confirmer!")

    print()
    print("=" * 80)
    print("6. RECOMMANDATIONS")
    print("-" * 80)
    print()
    print("Pour débugger davantage:")
    print("  1. Aller dans n8n → Executions")
    print("  2. Cliquer sur la dernière exécution de 'MCP - Idée Dev Nico (Perso)'")
    print("  3. Vérifier quel node est:")
    print("     • Vert ✅ (exécuté avec succès)")
    print("     • Rouge ❌ (erreur)")
    print("     • Gris (pas exécuté)")
    print("  4. Copier le message d'erreur du node rouge")
    print()

if __name__ == "__main__":
    analyze_delete_workflow()
