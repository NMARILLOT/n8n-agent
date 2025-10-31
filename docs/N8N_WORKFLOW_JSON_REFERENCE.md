# n8n Workflow JSON - Référence Complète

Documentation technique complète de la structure JSON des workflows n8n, basée sur l'analyse des workflows réels et de la documentation officielle.

---

## 📋 Table des Matières

1. [Structure Globale](#structure-globale)
2. [Métadonnées du Workflow](#métadonnées-du-workflow)
3. [Nodes (Nœuds)](#nodes-nœuds)
4. [Connections (Connexions)](#connections-connexions)
5. [Credentials (Identifiants)](#credentials-identifiants)
6. [Types de Nodes Spéciaux](#types-de-nodes-spéciaux)
7. [Exemples Complets](#exemples-complets)
8. [Pièges Courants](#pièges-courants)

---

## Structure Globale

Un workflow n8n est un objet JSON avec la structure suivante :

```json
{
  "name": "Nom du Workflow",
  "active": true,
  "createdAt": "2025-10-29T15:10:53.560Z",
  "updatedAt": "2025-10-31T20:33:01.000Z",
  "id": "workflow-id",
  "nodes": [ /* array de nodes */ ],
  "connections": { /* objet de connexions */ },
  "settings": { /* paramètres d'exécution */ },
  "staticData": null,
  "meta": null,
  "pinData": {},
  "versionId": "uuid",
  "triggerCount": 1,
  "shared": [ /* partage et permissions */ ]
}
```

---

## Métadonnées du Workflow

### Champs Obligatoires

| Champ | Type | Description | Exemple |
|-------|------|-------------|---------|
| `name` | string | Nom du workflow | `"MCP - Idée Dev Nico (Perso)"` |
| `nodes` | array | Liste des nœuds | `[...]` |
| `connections` | object | Connexions entre nœuds | `{...}` |

### Champs Optionnels

| Champ | Type | Description | Défaut |
|-------|------|-------------|--------|
| `active` | boolean | Workflow actif/inactif | `false` |
| `createdAt` | ISO 8601 | Date de création | Auto |
| `updatedAt` | ISO 8601 | Dernière modification | Auto |
| `id` | string | ID unique du workflow | Auto |
| `versionId` | string | Version UUID | Auto |
| `triggerCount` | number | Nombre de triggers | `0` |
| `settings` | object | Paramètres d'exécution | `{}` |
| `staticData` | any | Données persistantes | `null` |
| `meta` | object | Métadonnées | `null` |
| `pinData` | object | Données épinglées pour test | `{}` |

### Exemple Complet de Métadonnées

```json
{
  "name": "Agent Telegram - Dev Ideas",
  "active": true,
  "createdAt": "2025-10-29T15:10:53.560Z",
  "updatedAt": "2025-10-31T20:33:01.000Z",
  "id": "4lYuNSDjiyUjzHWL",
  "versionId": "97d94a20-e057-48a8-ae74-f558adbc9f82",
  "triggerCount": 1,
  "settings": {
    "executionOrder": "v1"
  }
}
```

---

## Nodes (Nœuds)

### Structure d'un Node

```json
{
  "parameters": { /* configuration spécifique au node */ },
  "type": "n8n-nodes-base.nodeType",
  "typeVersion": 1.0,
  "position": [x, y],
  "id": "unique-node-id",
  "name": "Node Name",
  "credentials": { /* références aux credentials */ },
  "notes": "Description du node"
}
```

### Champs d'un Node

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| `type` | string | ✅ | Type du node (ex: `"n8n-nodes-base.notion"`) |
| `typeVersion` | number | ✅ | Version du type de node |
| `position` | [number, number] | ✅ | Position [x, y] dans l'éditeur |
| `id` | string | ✅ | ID unique du node |
| `name` | string | ✅ | Nom d'affichage du node |
| `parameters` | object | ⚠️ | Configuration (varie selon le type) |
| `credentials` | object | ❌ | Références aux credentials si nécessaire |
| `notes` | string | ❌ | Notes/description du node |
| `disabled` | boolean | ❌ | Node désactivé (ne s'exécute pas) |

### Exemples de Nodes Courants

#### 1. Trigger MCP

```json
{
  "parameters": {
    "authentication": "bearerAuth",
    "path": "projects-mhms"
  },
  "type": "@n8n/n8n-nodes-langchain.mcpTrigger",
  "typeVersion": 1,
  "position": [-1008, 256],
  "id": "6b1b5a12-894d-47ef-ae4e-de790b03be0d",
  "name": "MCP Server Trigger",
  "webhookId": "projects-mhms",
  "credentials": {
    "httpBearerAuth": {
      "id": "aCtUA2HFdnNADDGH",
      "name": "Notion MCPAuth"
    }
  }
}
```

#### 2. Node Notion

```json
{
  "parameters": {
    "resource": "databasePage",
    "operation": "getAll",
    "databaseId": {
      "__rl": true,
      "value": "29b2c1373ccc807d9347ce519cabcac4",
      "mode": "id"
    },
    "returnAll": true,
    "options": {}
  },
  "type": "n8n-nodes-base.notion",
  "typeVersion": 2.2,
  "position": [336, 240],
  "id": "1f8ac91cfc9e4f948ccf266d",
  "name": "Notion - Search Ideas",
  "credentials": {
    "notionApi": {
      "id": "cT2CMYYw9BByHYSg",
      "name": "Notion account - nicolas@mhms.fr"
    }
  }
}
```

#### 3. Code Node (JavaScript)

```json
{
  "parameters": {
    "jsCode": "const input = $input.first().json;\nconst id = input.idea_id;\n\nreturn [{ json: { id, processed: true } }];"
  },
  "type": "n8n-nodes-base.code",
  "typeVersion": 2,
  "position": [528, 240],
  "id": "57dc52d451b54eaca288b2c6",
  "name": "Process Data",
  "notes": "🔧 Traite les données d'entrée"
}
```

#### 4. Switch Node

```json
{
  "parameters": {
    "rules": {
      "values": [
        {
          "conditions": {
            "options": {
              "caseSensitive": true,
              "leftValue": "",
              "typeValidation": "strict",
              "version": 2
            },
            "conditions": [
              {
                "leftValue": "={{ $json.operation }}",
                "rightValue": "delete",
                "operator": {
                  "type": "string",
                  "operation": "equals"
                }
              }
            ],
            "combinator": "and"
          },
          "renameOutput": true,
          "outputKey": "delete_operation"
        }
      ]
    },
    "options": {}
  },
  "type": "n8n-nodes-base.switch",
  "typeVersion": 3.2,
  "position": [0, 304],
  "id": "14c022c3-9f32-42f5-8bfe-bd7fb91cc382",
  "name": "Switch Operation"
}
```

#### 5. Tool Workflow (LangChain)

```json
{
  "parameters": {
    "name": "delete_idea",
    "description": "Archive une idée dans Notion par son ID.",
    "workflowId": {
      "__rl": true,
      "mode": "id",
      "value": "={{ $workflow.id }}"
    },
    "workflowInputs": {
      "mappingMode": "defineBelow",
      "value": {
        "idea_id": "={{ $fromAI('idea_id', '', 'string') }}",
        "__operation__": "delete_idea"
      },
      "matchingColumns": [],
      "schema": [
        {
          "id": "idea_id",
          "displayName": "idea_id",
          "required": true,
          "defaultMatch": false,
          "display": true,
          "canBeUsedToMatch": true,
          "type": "string"
        }
      ],
      "attemptToConvertTypes": false,
      "convertFieldsToString": false
    }
  },
  "type": "@n8n/n8n-nodes-langchain.toolWorkflow",
  "typeVersion": 2.1,
  "position": [-624, 800],
  "id": "363886779c68477cbc61dfa3",
  "name": "delete_idea"
}
```

---

## Connections (Connexions)

### Structure des Connexions

```json
{
  "connections": {
    "Node Source": {
      "main": [
        [
          {
            "node": "Node Destination",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  }
}
```

### Types de Connexions

| Type | Description | Usage |
|------|-------------|-------|
| `main` | Connexion principale (données) | Flux de données standard |
| `ai_tool` | Connexion pour LangChain tools | Retour au trigger MCP |

### Connexions Multiples (Switch, IF)

Les nodes avec plusieurs sorties utilisent des **arrays imbriqués** :

```json
{
  "Switch Operation": {
    "main": [
      [ /* Output 0 */ { "node": "Branch A", "type": "main", "index": 0 } ],
      [ /* Output 1 */ { "node": "Branch B", "type": "main", "index": 0 } ],
      [ /* Output 2 */ { "node": "Branch C", "type": "main", "index": 0 } ]
    ]
  }
}
```

### Connexion Tool → Trigger

```json
{
  "delete_idea": {
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
}
```

---

## Credentials (Identifiants)

### Structure

```json
{
  "credentials": {
    "credentialType": {
      "id": "credential-uuid",
      "name": "Credential Display Name"
    }
  }
}
```

### Types Courants

| Type | Description | Exemple |
|------|-------------|---------|
| `notionApi` | API Notion | Accès bases de données |
| `httpBearerAuth` | Bearer token HTTP | Auth MCP |
| `telegramApi` | API Telegram | Bot Telegram |

### ⚠️ Important sur les Credentials

- **Les IDs sont spécifiques à l'instance n8n**
- Lors de l'import, les credentials doivent être **réassignés manuellement**
- **Les secrets ne sont JAMAIS exportés** dans le JSON
- Seuls les **noms et IDs** sont inclus

---

## Types de Nodes Spéciaux

### 1. Execute Workflow Trigger

```json
{
  "parameters": {
    "fields": {
      "values": [
        { "name": "operation" },
        { "name": "idea_id" },
        { "name": "title" }
      ]
    }
  },
  "type": "n8n-nodes-base.executeWorkflowTrigger",
  "typeVersion": 1.1,
  "position": [-208, 416],
  "id": "ae4d132b-f896-4408-8aca-e072b614a3c7",
  "name": "Execute Workflow Trigger"
}
```

### 2. LangChain Agent

```json
{
  "parameters": {
    "promptType": "define",
    "text": "={{ $json.query }}",
    "hasOutputParser": true,
    "options": {
      "systemMessage": "Tu es un assistant...",
      "temperature": 0.2,
      "maxIterations": 10
    }
  },
  "type": "@n8n/n8n-nodes-langchain.agent",
  "typeVersion": 1.8,
  "position": [1000, 100],
  "id": "agent-id",
  "name": "Agent Dev Ideas"
}
```

### 3. Sticky Note (Documentation)

```json
{
  "parameters": {
    "content": "## 🔧 Outils MCP\nCes outils permettent...",
    "height": 400,
    "width": 300,
    "color": 4
  },
  "type": "n8n-nodes-base.stickyNote",
  "typeVersion": 1,
  "position": [-1264, -500],
  "id": "sticky-note-id",
  "name": "Note"
}
```

---

## Exemples Complets

### Workflow Minimal

```json
{
  "name": "Minimal Workflow",
  "active": false,
  "nodes": [
    {
      "parameters": {},
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [0, 0],
      "id": "trigger-id",
      "name": "Manual Trigger"
    },
    {
      "parameters": {
        "jsCode": "return [{ json: { message: 'Hello World' } }];"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [200, 0],
      "id": "code-id",
      "name": "Process"
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [[{ "node": "Process", "type": "main", "index": 0 }]]
    }
  },
  "settings": {},
  "staticData": null
}
```

### Workflow avec MCP Tool

```json
{
  "name": "MCP Tool Example",
  "active": true,
  "nodes": [
    {
      "parameters": {
        "authentication": "bearerAuth",
        "path": "my-mcp-server"
      },
      "type": "@n8n/n8n-nodes-langchain.mcpTrigger",
      "typeVersion": 1,
      "position": [0, 0],
      "id": "mcp-trigger-id",
      "name": "MCP Server Trigger",
      "webhookId": "my-mcp-server",
      "credentials": {
        "httpBearerAuth": {
          "id": "auth-id",
          "name": "MCP Auth"
        }
      }
    },
    {
      "parameters": {
        "name": "my_tool",
        "description": "Description de l'outil",
        "workflowId": {
          "__rl": true,
          "mode": "id",
          "value": "={{ $workflow.id }}"
        },
        "workflowInputs": {
          "mappingMode": "defineBelow",
          "value": {
            "input_param": "={{ $fromAI('input_param', '', 'string') }}"
          },
          "schema": [
            {
              "id": "input_param",
              "displayName": "input_param",
              "required": true,
              "type": "string"
            }
          ]
        }
      },
      "type": "@n8n/n8n-nodes-langchain.toolWorkflow",
      "typeVersion": 2.1,
      "position": [-200, 0],
      "id": "tool-id",
      "name": "my_tool"
    },
    {
      "parameters": {},
      "type": "n8n-nodes-base.executeWorkflowTrigger",
      "typeVersion": 1.1,
      "position": [200, 0],
      "id": "exec-trigger-id",
      "name": "Execute Workflow Trigger"
    },
    {
      "parameters": {
        "jsCode": "const param = $input.first().json.input_param;\nreturn [{ json: { response: `Processed: ${param}` } }];"
      },
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [400, 0],
      "id": "process-id",
      "name": "Process Input"
    }
  ],
  "connections": {
    "my_tool": {
      "ai_tool": [[{ "node": "MCP Server Trigger", "type": "ai_tool", "index": 0 }]]
    },
    "Execute Workflow Trigger": {
      "main": [[{ "node": "Process Input", "type": "main", "index": 0 }]]
    }
  }
}
```

---

## Pièges Courants

### 1. ❌ Credentials Manquants Après Import

**Problème** : Les IDs de credentials sont invalides après import.

**Solution** : Toujours réassigner manuellement les credentials dans l'UI n8n.

### 2. ❌ Node Sans Connexion Sortante

**Problème** : "The workflow did not return a response"

**Cause** : Le dernier node n'a pas de connexion vers le trigger ou n'est jamais atteint.

**Solution** : Vérifier que le flux arrive bien jusqu'au node final.

### 3. ❌ Mauvaise Lecture des Données d'Input

**Problème** : `$input.first().json.field` retourne `undefined`

**Causes** :
- Les données arrivent dans un objet imbriqué (ex: `query.field`)
- Le node précédent a échoué et n'a rien retourné
- Mauvais nom de champ

**Solution** : Logger l'input complet :
```javascript
console.log('[DEBUG] Input:', JSON.stringify($input.first().json));
```

### 4. ❌ Switch Ne Route Pas Correctement

**Problème** : Le Switch n'active pas la bonne branche.

**Causes** :
- Path d'accès incorrect (`$json.field` vs `$json.query.field`)
- Type de comparaison incorrect (string vs number)
- Valeur attendue différente de celle reçue

**Solution** :
```json
{
  "leftValue": "={{ $json.query.operation }}",  // ✅ Bon path
  "rightValue": "delete",  // ✅ Bonne valeur
  "operator": {
    "type": "string",
    "operation": "equals"
  }
}
```

### 5. ❌ Tool Schema Invalide (LangChain)

**Problème** : "Received tool input did not match expected schema"

**Causes** :
- Paramètres non requis mais marqués comme `required: true`
- Type incorrect dans le schema
- Paramètres inutiles dans le schema

**Solution** : Simplifier le schema au minimum requis :
```json
{
  "schema": [
    {
      "id": "required_param",
      "displayName": "required_param",
      "required": true,
      "type": "string"
    }
  ]
}
```

### 6. ❌ ID de Node Dupliqué

**Problème** : Comportement imprévisible, connexions cassées.

**Solution** : **Toujours générer de nouveaux IDs uniques** lors de la duplication de nodes.

```python
import uuid
new_id = str(uuid.uuid4()).replace('-', '')[:24]
```

---

## Bonnes Pratiques

### ✅ Nommage

- **Nodes** : Noms descriptifs et uniques (`"Notion - Search Ideas"` pas `"Notion"`)
- **Workflows** : Inclure le contexte (`"MCP - Idée Dev Nico (Perso)"`)

### ✅ Organisation Visuelle

- **Position logique** : Gauche → Droite pour le flux principal
- **Espacement** : ~200px vertical, ~150-240px horizontal
- **Groupes logiques** : Aligner verticalement les branches parallèles

### ✅ Documentation

- **Notes** : Ajouter des notes aux nodes complexes
- **Sticky Notes** : Documenter les sections du workflow
- **Description du tool** : Claire et précise pour l'agent

### ✅ Gestion d'Erreurs

- **Logs de debug** : `console.log('[DEBUG]', ...)` dans les Code nodes
- **Messages d'erreur clairs** : Retourner `{ response: "❌ Erreur: ...", error: true }`
- **Validation d'input** : Vérifier les paramètres requis

### ✅ Versioning

- **Git** : Toujours versionner les workflows
- **Commits descriptifs** : Expliquer les changements
- **Backup avant modification** : Export JSON avant changements majeurs

---

## Ressources

- **Documentation officielle** : https://docs.n8n.io/
- **API Reference** : https://docs.n8n.io/api/
- **Community** : https://community.n8n.io/
- **GitHub** : https://github.com/n8n-io/n8n

---

**Dernière mise à jour** : 2025-10-31
**Version n8n** : 1.115.3
