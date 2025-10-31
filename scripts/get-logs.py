#!/usr/bin/env python3
"""
Script pour récupérer les logs d'erreur du workflow Agent Telegram
"""

import requests
import json
import os
from pathlib import Path

# Configuration
N8N_HOST = "https://auto.mhms.fr"
N8N_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJlZTNlMmRhMi04NjkxLTQ5YjQtYmZkYy05N2I3NWQ3NWM0MWMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYxOTE0MDkyfQ.Os_9hVPVwrzy-vFnUyv9nTsuvUzugOiI7zpJzWU4VKA"
WORKFLOW_ID = "4lYuNSDjiyUjzHWL"  # Agent Telegram - Dev Ideas

headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Accept": "application/json"
}

print("🔍 Récupération des logs du workflow Agent Telegram...")
print()

# Récupérer les dernières exécutions
response = requests.get(
    f"{N8N_HOST}/api/v1/executions",
    headers=headers,
    params={"workflowId": WORKFLOW_ID, "limit": 3}
)

if response.status_code != 200:
    print(f"❌ Erreur API: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()

if not data.get('data'):
    print("Aucune exécution trouvée")
    exit(0)

for i, execution in enumerate(data['data'], 1):
    print(f"{'='*60}")
    print(f"EXÉCUTION #{i}")
    print(f"{'='*60}")
    print(f"ID: {execution['id']}")
    print(f"Status: {execution['status']}")
    print(f"Mode: {execution.get('mode', 'N/A')}")
    print(f"Finished: {execution.get('finished', 'N/A')}")
    print(f"Started: {execution.get('startedAt', 'N/A')}")

    if execution.get('data'):
        result_data = execution['data'].get('resultData', {})

        # Afficher l'erreur globale si présente
        if 'error' in result_data:
            error = result_data['error']
            print(f"\n❌ ERREUR GLOBALE:")
            print(f"  Message: {error.get('message', 'N/A')}")
            if 'stack' in error:
                print(f"  Stack: {error['stack'][:200]}...")

        # Analyser les nodes exécutés
        run_data = result_data.get('runData', {})
        print(f"\n📊 Nodes exécutés: {len(run_data)}")

        for node_name, node_runs in run_data.items():
            if not node_runs or len(node_runs) == 0:
                continue

            node_exec = node_runs[0]

            # Vérifier les erreurs
            if node_exec.get('error'):
                error = node_exec['error']
                print(f"\n❌ ERREUR dans node '{node_name}':")
                print(f"  Message: {error.get('message', 'N/A')}")
                print(f"  Description: {error.get('description', 'N/A')}")

                if 'context' in error:
                    print(f"  Contexte: {json.dumps(error['context'], indent=2)}")

            # Afficher le statut d'exécution
            elif node_exec.get('executionStatus') == 'success':
                data_count = len(node_exec.get('data', {}).get('main', [[]])[0])
                print(f"  ✅ {node_name}: OK ({data_count} items)")

    print()
