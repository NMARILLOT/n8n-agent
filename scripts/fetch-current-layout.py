#!/usr/bin/env python3
"""
Récupère les workflows actuels depuis n8n pour voir tes changements
"""

import json
import os
import subprocess

# Récupérer le workflow MCP
print("📥 Récupération des workflows depuis n8n...")

api_key = os.environ.get('N8N_API_KEY')
if not api_key:
    print("❌ N8N_API_KEY not found")
    exit(1)

# MCP workflow
mcp_cmd = f'curl -s -X GET "https://auto.mhms.fr/api/v1/workflows/zh79Jo1FWhNrSZwn" -H "X-N8N-API-KEY: {api_key}"'
mcp_result = subprocess.run(mcp_cmd, shell=True, capture_output=True, text=True)
mcp_workflow = json.loads(mcp_result.stdout)

# Telegram workflow
telegram_cmd = f'curl -s -X GET "https://auto.mhms.fr/api/v1/workflows/4lYuNSDjiyUjzHWL" -H "X-N8N-API-KEY: {api_key}"'
telegram_result = subprocess.run(telegram_cmd, shell=True, capture_output=True, text=True)
telegram_workflow = json.loads(telegram_result.stdout)

# Sauvegarder localement
with open('Agent Telegram - Dev Nico Perso/workflow/MCP - Idée Dev Nico (Perso) (1).json', 'w') as f:
    json.dump(mcp_workflow, f, indent=2, ensure_ascii=False)

with open('Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json', 'w') as f:
    json.dump(telegram_workflow, f, indent=2, ensure_ascii=False)

print("✅ Workflows récupérés et sauvegardés!")

# Analyser les positions pour comprendre ton style
print("\n=== ANALYSE DE TON ORGANISATION ===")

def analyze_workflow(workflow, name):
    print(f"\n📊 {name}:")

    nodes = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.stickyNote']
    sticky_notes = [n for n in workflow['nodes'] if n['type'] == 'n8n-nodes-base.stickyNote']

    print(f"  - {len(nodes)} nodes")
    print(f"  - {len(sticky_notes)} sticky notes")

    if nodes:
        x_positions = [n['position'][0] for n in nodes]
        y_positions = [n['position'][1] for n in nodes]

        # Calculer les espacements moyens
        x_sorted = sorted(set(x_positions))
        y_sorted = sorted(set(y_positions))

        if len(x_sorted) > 1:
            x_spacing = sum(x_sorted[i+1] - x_sorted[i] for i in range(len(x_sorted)-1)) / (len(x_sorted)-1)
            print(f"  - Espacement horizontal moyen: {x_spacing:.0f}px")

        if len(y_sorted) > 1:
            y_spacing = sum(y_sorted[i+1] - y_sorted[i] for i in range(len(y_sorted)-1)) / (len(y_sorted)-1)
            print(f"  - Espacement vertical moyen: {y_spacing:.0f}px")

        print(f"  - Range X: {min(x_positions)} à {max(x_positions)}")
        print(f"  - Range Y: {min(y_positions)} à {max(y_positions)}")

analyze_workflow(mcp_workflow, "MCP Workflow")
analyze_workflow(telegram_workflow, "Telegram Workflow")

print("\n✅ Tes changements ont été intégrés localement!")