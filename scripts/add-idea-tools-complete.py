#!/usr/bin/env python3
"""
Script complet pour ajouter les outils MCP de gestion des idées
Ajoute les Tool Workflow nodes, les nodes Notion, les nodes Code et toutes les connexions
"""

import json
import uuid
from pathlib import Path

def generate_id():
    """Génère un ID unique au format n8n"""
    return str(uuid.uuid4()).replace('-', '')[:24]

# Charger le workflow
script_dir = Path(__file__).parent
project_root = script_dir.parent
workflow_path = project_root / "Agent Telegram - Dev Nico Perso" / "workflow" / "MCP - Idée Dev Nico (Perso) (1).json"

with open(workflow_path, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

print("🔧 Ajout des nouveaux outils MCP pour la gestion des idées...")
print()

# IDs pour les nouveaux nodes
ids = {
    'search_ideas_tool': generate_id(),
    'get_idea_tool': generate_id(),
    'update_idea_tool': generate_id(),
    'delete_idea_tool': generate_id(),
    'notion_search_ideas': generate_id(),
    'notion_get_idea': generate_id(),
    'notion_update_idea': generate_id(),
    'notion_delete_idea': generate_id(),
    'code_format_search_ideas': generate_id(),
    'code_format_get_idea': generate_id(),
    'code_format_update_idea': generate_id(),
    'code_format_delete_idea': generate_id()
}

# Database IDs
DB_IDEAS = "29b2c1373ccc807d9347ce519cabcac4"
DB_PROJECTS = "29b2c1373ccc8042a8e2e096b12ca4e4"

# === 1. TOOL WORKFLOW NODES ===
print("📦 Ajout des Tool Workflow nodes...")

tool_workflows = [
    {
        "id": ids['search_ideas_tool'],
        "name": "search_ideas",
        "description": "Recherche d'idées par mot-clé dans le titre ou contenu. Retourne les idées avec leur ID, projet associé, titre, catégorie et statut.",
        "position": [-640, 480]
    },
    {
        "id": ids['get_idea_tool'],
        "name": "get_idea_by_id",
        "description": "Récupère les détails complets d'une idée spécifique par son ID (format IDEA-XXX).",
        "position": [-512, 560]
    },
    {
        "id": ids['update_idea_tool'],
        "name": "update_idea",
        "description": "Modifie une idée existante. Paramètres : idea_id (string, format IDEA-XXX, REQUIS), title (string, optionnel), content (string, optionnel), category (string, optionnel: Nouvelle fonctionnalité|Amélioration|Bug fix|Refactoring|Documentation).",
        "position": [-384, 640]
    },
    {
        "id": ids['delete_idea_tool'],
        "name": "delete_idea",
        "description": "Supprime définitivement une idée par son ID (format IDEA-XXX). ⚠️ ATTENTION : Cette action est IRRÉVERSIBLE. Toujours confirmer avec l'utilisateur avant d'exécuter.",
        "position": [-256, 720]
    }
]

for tool in tool_workflows:
    node = {
        "parameters": {
            "name": tool['name'],
            "description": tool['description'],
            "workflowId": {
                "__rl": True,
                "mode": "id",
                "value": "={{ $workflow.id }}"
            },
            "workflowInputs": {
                "mappingMode": "defineBelow",
                "value": {
                    "operation": "={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('operation', ``, 'string') }}",
                    "query": "={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('query', ``, 'string') }}",
                    "idea_id": "={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('idea_id', ``, 'string') }}",
                    "title": "={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('title', ``, 'string') }}",
                    "content": "={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('content', ``, 'string') }}",
                    "category": "={{ /*n8n-auto-generated-fromAI-override*/ $fromAI('category', ``, 'string') }}"
                },
                "matchingColumns": [],
                "schema": [
                    {"id": "operation", "displayName": "operation", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "query", "displayName": "query", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
                    {"id": "idea_id", "displayName": "idea_id", "required": False, "defaultMatch": False, "display": True, "canBeUsedToMatch": True, "type": "string"},
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
        "position": tool['position'],
        "id": tool['id'],
        "name": tool['name']
    }
    workflow['nodes'].append(node)
    print(f"  ✅ {tool['name']}")

# === 2. NOTION NODES ===
print("\n📄 Ajout des Notion nodes...")

# 2.1 Search Ideas
workflow['nodes'].append({
    "parameters": {
        "resource": "databasePage",
        "operation": "getAll",
        "databaseId": {"__rl": True, "value": DB_IDEAS, "mode": "id"},
        "returnAll": True,
        "options": {}
    },
    "type": "n8n-nodes-base.notion",
    "typeVersion": 2.2,
    "position": [80, 1040],
    "id": ids['notion_search_ideas'],
    "name": "Notion - Search Ideas",
    "credentials": {
        "notionApi": {
            "id": "cT2CMYYw9BByHYSg",
            "name": "Notion account - nicolas@mhms.fr"
        }
    }
})
print("  ✅ Notion - Search Ideas")

# 2.2 Get Idea By ID
workflow['nodes'].append({
    "parameters": {
        "resource": "databasePage",
        "operation": "getAll",
        "databaseId": {"__rl": True, "value": DB_IDEAS, "mode": "id"},
        "returnAll": True,
        "options": {}
    },
    "type": "n8n-nodes-base.notion",
    "typeVersion": 2.2,
    "position": [80, 1120],
    "id": ids['notion_get_idea'],
    "name": "Notion - Get Idea By ID",
    "credentials": {
        "notionApi": {
            "id": "cT2CMYYw9BByHYSg",
            "name": "Notion account - nicolas@mhms.fr"
        }
    }
})
print("  ✅ Notion - Get Idea By ID")

# 2.3 Update Idea (get first, then update)
workflow['nodes'].append({
    "parameters": {
        "resource": "databasePage",
        "operation": "getAll",
        "databaseId": {"__rl": True, "value": DB_IDEAS, "mode": "id"},
        "returnAll": True,
        "options": {}
    },
    "type": "n8n-nodes-base.notion",
    "typeVersion": 2.2,
    "position": [80, 1200],
    "id": ids['notion_update_idea'],
    "name": "Notion - Update Idea",
    "credentials": {
        "notionApi": {
            "id": "cT2CMYYw9BByHYSg",
            "name": "Notion account - nicolas@mhms.fr"
        }
    },
    "notes": "📝 Récupère d'abord l'idée existante pour pouvoir la mettre à jour"
})
print("  ✅ Notion - Update Idea")

# 2.4 Delete Idea
workflow['nodes'].append({
    "parameters": {
        "resource": "databasePage",
        "operation": "getAll",
        "databaseId": {"__rl": True, "value": DB_IDEAS, "mode": "id"},
        "returnAll": True,
        "options": {}
    },
    "type": "n8n-nodes-base.notion",
    "typeVersion": 2.2,
    "position": [80, 1280],
    "id": ids['notion_delete_idea'],
    "name": "Notion - Delete Idea",
    "credentials": {
        "notionApi": {
            "id": "cT2CMYYw9BByHYSg",
            "name": "Notion account - nicolas@mhms.fr"
        }
    },
    "notes": "⚠️ Suppression définitive de l'idée"
})
print("  ✅ Notion - Delete Idea")

# === 3. CODE NODES POUR FORMATER LES RÉPONSES ===
print("\n💻 Ajout des Code nodes de formatage...")

# 3.1 Format Search Ideas
workflow['nodes'].append({
    "parameters": {
        "jsCode": """const query = ($input.first().json.query || '').toLowerCase();
const allIdeas = $('Notion - Search Ideas').all();

const matching = allIdeas.filter(item => {
  const props = item.json;
  const title = (props.property_titre_de_l_id_e || '').toLowerCase();
  const content = (props.property_contenu || '').toLowerCase();
  const id = (props.property_id || '').toLowerCase();

  return title.includes(query) || content.includes(query) || id.includes(query);
});

const results = matching.map(item => {
  const props = item.json;
  const id = props.property_id || 'N/A';
  const title = props.property_titre_de_l_id_e || '';
  const category = props.property_cat_gorie || 'N/A';
  const status = props.property_trait_ || 'N/A';
  const projectName = props.property_projet_li_ && props.property_projet_li_[0] ? props.property_projet_li_[0].name : 'N/A';
  const url = props.url || '';

  return `[${id}] ${title}\\nProjet: ${projectName} | Catégorie: ${category}\\nStatut: ${status}\\nURL: ${url}`;
});

const response = results.length > 0
  ? results.join('\\n\\n---\\n\\n')
  : `Aucune idée trouvée pour "${query}".`;

return [{ json: { response } }];"""
    },
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [288, 1040],
    "id": ids['code_format_search_ideas'],
    "name": "Format Search Ideas",
    "notes": "🔍 Recherche et formate les idées par mots-clés"
})
print("  ✅ Format Search Ideas")

# 3.2 Format Get Idea By ID
workflow['nodes'].append({
    "parameters": {
        "jsCode": """const requestedId = ($input.first().json.idea_id || '').trim();
const allIdeas = $('Notion - Get Idea By ID').all();

const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  return [{ json: { response: `Idée "${requestedId}" non trouvée.` } }];
}

const props = idea.json;
const id = props.property_id || 'N/A';
const title = props.property_titre_de_l_id_e || '';
const content = props.property_contenu || 'N/A';
const category = props.property_cat_gorie || 'N/A';
const status = props.property_trait_ || 'N/A';
const projectName = props.property_projet_li_ && props.property_projet_li_[0] ? props.property_projet_li_[0].name : 'N/A';
const url = props.url || '';

const response = `[${id}] ${title}\\n\\nContenu: ${content}\\n\\nProjet: ${projectName}\\nCatégorie: ${category}\\nStatut: ${status}\\n\\nURL: ${url}`;

return [{ json: { response, notion_page_id: props.id } }];"""
    },
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [288, 1120],
    "id": ids['code_format_get_idea'],
    "name": "Format Get Idea",
    "notes": "📋 Récupère et formate les détails d'une idée spécifique"
})
print("  ✅ Format Get Idea")

# 3.3 Format Update Idea (plus complexe - nécessite update puis format)
workflow['nodes'].append({
    "parameters": {
        "jsCode": """const requestedId = ($input.first().json.idea_id || '').trim();
const allIdeas = $('Notion - Update Idea').all();

const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  throw new Error(`Idée "${requestedId}" non trouvée. Impossible de modifier.`);
}

const notionPageId = idea.json.id;
const currentTitle = idea.json.property_titre_de_l_id_e || '';
const currentContent = idea.json.property_contenu || '';
const currentCategory = idea.json.property_cat_gorie || '';

// Get update values from input
const newTitle = $input.first().json.title || currentTitle;
const newContent = $input.first().json.content || currentContent;
const newCategory = $input.first().json.category || currentCategory;

return [{
  json: {
    id: requestedId,
    notion_page_id: notionPageId,
    title: newTitle,
    content: newContent,
    category: newCategory
  }
}];"""
    },
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [288, 1200],
    "id": ids['code_format_update_idea'],
    "name": "Prepare Update Idea",
    "notes": "⚙️ Prépare les données pour la mise à jour (merge ancien + nouveau)"
})
print("  ✅ Prepare Update Idea")

# 3.4 Format Delete Idea
workflow['nodes'].append({
    "parameters": {
        "jsCode": """const requestedId = ($input.first().json.idea_id || '').trim();
const allIdeas = $('Notion - Delete Idea').all();

const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  return [{ json: { response: `Idée "${requestedId}" non trouvée.` } }];
}

const notionPageId = idea.json.id;
const title = idea.json.property_titre_de_l_id_e || '';

return [{
  json: {
    id: requestedId,
    notion_page_id: notionPageId,
    title: title
  }
}];"""
    },
    "type": "n8n-nodes-base.code",
    "typeVersion": 2,
    "position": [288, 1280],
    "id": ids['code_format_delete_idea'],
    "name": "Prepare Delete Idea",
    "notes": "🗑️ Prépare la suppression de l'idée"
})
print("  ✅ Prepare Delete Idea")

# === 4. UPDATE SWITCH OPERATION ===
print("\n🔀 Mise à jour du Switch Operation...")

switch_node = next(n for n in workflow['nodes'] if n['name'] == 'Switch Operation')
switch_node['parameters']['rules']['values'].extend([
    {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [{"leftValue": "={{ $json.operation }}", "rightValue": "search_ideas", "operator": {"type": "string", "operation": "equals"}}],
            "combinator": "and"
        },
        "renameOutput": True,
        "outputKey": "search_ideas"
    },
    {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [{"leftValue": "={{ $json.operation }}", "rightValue": "get_idea_by_id", "operator": {"type": "string", "operation": "equals"}}],
            "combinator": "and"
        },
        "renameOutput": True,
        "outputKey": "get_idea"
    },
    {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [{"leftValue": "={{ $json.operation }}", "rightValue": "update_idea", "operator": {"type": "string", "operation": "equals"}}],
            "combinator": "and"
        },
        "renameOutput": True,
        "outputKey": "update_idea"
    },
    {
        "conditions": {
            "options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict", "version": 2},
            "conditions": [{"leftValue": "={{ $json.operation }}", "rightValue": "delete_idea", "operator": {"type": "string", "operation": "equals"}}],
            "combinator": "and"
        },
        "renameOutput": True,
        "outputKey": "delete_idea"
    }
])

# === 5. CONNEXIONS ===
print("\n🔗 Ajout des connexions...")

# Tool workflows → MCP Trigger
for tool_id, tool_name in [
    (ids['search_ideas_tool'], 'search_ideas'),
    (ids['get_idea_tool'], 'get_idea_by_id'),
    (ids['update_idea_tool'], 'update_idea'),
    (ids['delete_idea_tool'], 'delete_idea')
]:
    workflow['connections'][tool_name] = {
        "ai_tool": [[{"node": "MCP Server Trigger", "type": "ai_tool", "index": 0}]]
    }

# Switch → Notion nodes
workflow['connections']['Switch Operation']['main'].extend([
    [{"node": "Notion - Search Ideas", "type": "main", "index": 0}],  # search_ideas
    [{"node": "Notion - Get Idea By ID", "type": "main", "index": 0}],  # get_idea
    [{"node": "Notion - Update Idea", "type": "main", "index": 0}],  # update_idea
    [{"node": "Notion - Delete Idea", "type": "main", "index": 0}]  # delete_idea
])

# Notion → Code formatting
workflow['connections']['Notion - Search Ideas'] = {
    "main": [[{"node": "Format Search Ideas", "type": "main", "index": 0}]]
}
workflow['connections']['Notion - Get Idea By ID'] = {
    "main": [[{"node": "Format Get Idea", "type": "main", "index": 0}]]
}
workflow['connections']['Notion - Update Idea'] = {
    "main": [[{"node": "Prepare Update Idea", "type": "main", "index": 0}]]
}
workflow['connections']['Notion - Delete Idea'] = {
    "main": [[{"node": "Prepare Delete Idea", "type": "main", "index": 0}]]
}

print("  ✅ Toutes les connexions ajoutées")

# === 6. SAUVEGARDER ===
print("\n💾 Sauvegarde du workflow...")
with open(workflow_path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"\n✨ Workflow mis à jour avec succès!")
print(f"📁 Fichier: {workflow_path}")
print(f"📊 Nouveaux outils MCP: 4")
print(f"📊 Nouveaux nodes Notion: 4")
print(f"📊 Nouveaux nodes Code: 4")
print(f"📊 Total nouveaux nodes: 12")
print()
print("⚠️  ATTENTION: Il reste à ajouter manuellement dans n8n:")
print("   - Node Notion Update (après Prepare Update Idea)")
print("   - Node Notion Delete (après Prepare Delete Idea)")
print("   - Nodes de formatage final pour update et delete")
