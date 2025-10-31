#!/usr/bin/env python3
"""
Script pour ajouter les outils MCP de gestion des idées au workflow
"""

import json
import uuid
import sys
from pathlib import Path

def generate_id():
    """Génère un ID unique au format n8n"""
    return str(uuid.uuid4()).replace('-', '')[:24]

def create_tool_workflow_node(name, description, position, workflow_id):
    """Crée un node Tool Workflow"""
    return {
        "parameters": {
            "name": name,
            "description": description,
            "workflowId": {
                "__rl": True,
                "mode": "id",
                "value": f"={{{{ $workflow.id }}}}"
            },
            "workflowInputs": {
                "mappingMode": "defineBelow",
                "value": {
                    "operation": f"={{{{ /*n8n-auto-generated-fromAI-override*/ $fromAI('operation', ``, 'string') }}}}",
                    "query": f"={{{{ /*n8n-auto-generated-fromAI-override*/ $fromAI('query', ``, 'string') }}}}",
                    "id": f"={{{{ /*n8n-auto-generated-fromAI-override*/ $fromAI('id', ``, 'string') }}}}",
                    "idea_id": f"={{{{ /*n8n-auto-generated-fromAI-override*/ $fromAI('idea_id', ``, 'string') }}}}",
                    "project_id": f"={{{{ /*n8n-auto-generated-fromAI-override*/ $fromAI('project_id', ``, 'string') }}}}",
                    "title": f"={{{{ /*n8n-auto-generated-fromAI-override*/ $fromAI('title', ``, 'string') }}}}",
                    "content": f"={{{{ /*n8n-auto-generated-fromAI-override*/ $fromAI('content', ``, 'string') }}}}",
                    "category": f"={{{{ /*n8n-auto-generated-fromAI-override*/ $fromAI('category', ``, 'string') }}}}"
                },
                "matchingColumns": [],
                "schema": [
                    {"id": "operation", "displayName": "operation", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "query", "displayName": "query", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "id", "displayName": "id", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "idea_id", "displayName": "idea_id", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "project_id", "displayName": "project_id", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "title", "displayName": "title", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "content", "displayName": "content", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "category", "displayName": "category", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"}
                ],
                "attemptToConvertTypes": False,
                "convertFieldsToString": False
            }
        },
        "type": "@n8n/n8n-nodes-langchain.toolWorkflow",
        "typeVersion": 2.1,
        "position": position,
        "id": generate_id(),
        "name": name
    }

# Charger le workflow
script_dir = Path(__file__).parent
project_root = script_dir.parent
workflow_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"

with open(workflow_path, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

print("🔧 Ajout des nouveaux outils MCP...")

# Trouver le MCP Server Trigger
mcp_trigger = next(n for n in workflow['nodes'] if n['name'] == 'MCP Server Trigger')
mcp_trigger_id = mcp_trigger['id']

# Positions pour les nouveaux nodes (à droite des existants)
new_tools = [
    ("search_ideas", "Recherche d'idées par mot-clé dans le titre ou contenu. Retourne les idées avec leur ID, projet associé, catégorie et statut.", [-640, 560]),
    ("get_idea_by_id", "Récupère les détails complets d'une idée par son ID (format IDEA-XXX).", [-512, 640]),
    ("update_idea", "Modifie une idée existante. Paramètres : idea_id (string, format IDEA-XXX), title (optionnel), content (optionnel), category (optionnel).", [-384, 720]),
    ("delete_idea", "Supprime une idée par son ID (format IDEA-XXX). ATTENTION : action irréversible.", [-256, 800])
]

# Ajouter les nouveaux Tool Workflow nodes
new_node_ids = []
for name, description, position in new_tools:
    node = create_tool_workflow_node(name, description, position, workflow['id'])
    workflow['nodes'].append(node)
    new_node_ids.append((name, node['id']))
    print(f"  ✅ Ajout de {name}")

# Connecter les nouveaux tools au MCP Server Trigger
if 'connections' not in workflow:
    workflow['connections'] = {}

for name, node_id in new_node_ids:
    workflow['connections'][name] = {
        "ai_tool": [
            [
                {
                    "node": "MCP Server Trigger",
                    "type": "ai_tool",
                    "index": 0
                }
            ]
        ]
    }

# Mettre à jour le Switch Operation pour ajouter les nouvelles opérations
switch_node = next(n for n in workflow['nodes'] if n['name'] == 'Switch Operation')
switch_node['parameters']['rules']['values'].extend([
    {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [
                {
                    "leftValue": "={{ $json.operation }}",
                    "rightValue": "search_ideas",
                    "operator": {"type": "string", "operation": "equals"}
                }
            ],
            "combinator": "and"
        },
        "renameOutput": True,
        "outputKey": "search_ideas"
    },
    {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [
                {
                    "leftValue": "={{ $json.operation }}",
                    "rightValue": "get_idea_by_id",
                    "operator": {"type": "string", "operation": "equals"}
                }
            ],
            "combinator": "and"
        },
        "renameOutput": True,
        "outputKey": "get_idea"
    },
    {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [
                {
                    "leftValue": "={{ $json.operation }}",
                    "rightValue": "update_idea",
                    "operator": {"type": "string", "operation": "equals"}
                }
            ],
            "combinator": "and"
        },
        "renameOutput": True,
        "outputKey": "update_idea"
    },
    {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [
                {
                    "leftValue": "={{ $json.operation }}",
                    "rightValue": "delete_idea",
                    "operator": {"type": "string", "operation": "equals"}
                }
            ],
            "combinator": "and"
        },
        "renameOutput": True,
        "outputKey": "delete_idea"
    }
])

print("  ✅ Mise à jour du Switch Operation")

# Sauvegarder le workflow mis à jour
with open(workflow_path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"\n✨ Workflow mis à jour! ({len(new_tools)} nouveaux outils ajoutés)")
print(f"📁 Fichier: {workflow_path}")
