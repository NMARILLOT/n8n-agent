# 🐛 Base de Connaissances - Bugs & Solutions n8n

**Objectif**: Répertorier tous les bugs rencontrés dans les workflows n8n pour éviter de les résoudre plusieurs fois.

**Utilisation**: Avant de débugger, TOUJOURS consulter ce fichier avec Grep/Read pour voir si le bug est connu.

---

## 📋 Index par Catégorie

- [Nodes n8n](#nodes-n8n)
- [Langchain & Agents](#langchain--agents)
- [MCP Integration](#mcp-integration)
- [Expressions & Variables](#expressions--variables)
- [API & Intégrations](#api--intégrations)
- [Performance & Mémoire](#performance--mémoire)
- [Credentials & Auth](#credentials--auth)

---

## Format de Documentation

Chaque bug suit ce format:

```markdown
### [BUG-XXX] Titre court du bug

**Date**: YYYY-MM-DD
**Catégorie**: [Node/API/Performance/etc.]
**Sévérité**: 🔴 Critique | 🟡 Important | 🟢 Mineur
**Workflow(s) affecté(s)**: Nom du/des workflow(s)

**🔍 Symptômes**:
- Description du comportement observé
- Messages d'erreur

**🎯 Cause racine**:
Explication technique de la cause

**✅ Solution**:
1. Étapes de résolution
2. Code/configuration à modifier
3. Validation

**🔄 Prévention**:
- Bonnes pratiques pour éviter ce bug
- Patterns à suivre

**🔗 Références**:
- Liens documentation n8n
- Discussions forum
- GitHub issues
```

---

## Nodes n8n

### [BUG-001] Placeholder - Premier bug à documenter

**Date**: 2025-10-31
**Catégorie**: Template
**Sévérité**: 🟢 Mineur
**Workflow(s) affecté(s)**: N/A

**🔍 Symptômes**:
- Ceci est un template d'exemple

**🎯 Cause racine**:
Template pour documentation future

**✅ Solution**:
Remplacer par de vrais bugs rencontrés

**🔄 Prévention**:
Documenter chaque bug dès qu'il est résolu

**🔗 Références**:
- https://docs.n8n.io/

---

## Langchain & Agents

### [BUG-002] Agent hallucine au lieu d'utiliser les tools MCP

**Date**: 2025-10-31
**Catégorie**: Langchain/Agent
**Sévérité**: 🔴 Critique
**Workflow(s) affecté(s)**: Agent Telegram - Dev Ideas

**🔍 Symptômes**:
- L'agent répond "✅ Suppression effectuée ! IDEA-XXX a été supprimée" SANS appeler `delete_idea()`
- Il invente des IDs et des confirmations
- L'utilisateur pense que l'action est faite alors qu'elle ne l'est pas
- Aucun tool call n'apparaît dans les logs d'exécution

**🎯 Cause racine**:
**Hallucination LLM** : Claude (et tous les LLMs) peuvent répondre directement au lieu d'appeler les tools disponibles, même si le system prompt dit "TOUJOURS utiliser les outils".

Causes techniques :
1. Le system prompt n'est pas assez **explicite et strict**
2. La température du LLM (0.7 par défaut) permet trop de créativité
3. Claude peut "penser" qu'il aide l'utilisateur en répondant rapidement
4. Pas de validation que les tools DOIVENT être appelés

C'est un problème connu avec les agents LangChain.

**✅ Solution**:
1. **System prompt BEAUCOUP plus strict** avec menaces explicites
2. **Checklist de vérification** avant chaque réponse
3. **Baisser la température** à 0.2 (plus déterministe)
4. **Instructions de fallback** si pas d'outil applicable
5. **(OPTIONNEL)** Utiliser `tool_choice='required'` dans l'API Anthropic

**🔄 Prévention**:
- **Toujours tester** l'agent après modification du prompt
- **Vérifier les logs d'exécution** pour confirmer que les tools sont appelés
- **Être TRÈS explicite** dans les system prompts
- **Température basse** (0.1-0.3) pour agents avec workflows stricts

**🔗 Références**:
- [Anthropic - Tool Choice](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

---

## MCP Integration

### [BUG-003] Tool delete_idea retourne "workflow did not return a response"

**Date**: 2025-10-31
**Catégorie**: MCP/LangChain Tool Workflow
**Sévérité**: 🔴 Critique
**Workflow(s) affecté(s)**: MCP - Idée Dev Nico (Perso)

**🔍 Symptômes**:
- Erreur: `The workflow did not return a response`
- Tool `delete_idea` échoue systématiquement
- Agent LLM reçoit "Missing required parameter: operation"
- LangChain schema validation error: "Received tool input did not match expected schema"

**🎯 Cause racine**:
**Paramètres tool mal configurés** : Le tool `delete_idea` avait 6 paramètres tous marqués comme `required: true`, alors que seul `idea_id` était nécessaire pour l'opération.

Causes techniques détaillées :
1. **Trop de paramètres requis** : `operation`, `query`, `idea_id`, `title`, `content`, `category` tous required
2. **LLM ne sait pas quoi remplir** : Claude ne peut pas deviner des valeurs pour `operation`, `query`, `title`, etc.
3. **Validation LangChain échoue** : Input ne correspond pas au schema attendu
4. **Workflow ne s'exécute jamais** : Bloqué dès la validation d'input
5. **Structure input incorrecte** : Data arrivait dans `{query: {operation, idea_id}}` au lieu de root level
6. **Node cache problème** : Ancien node avec mauvaise config restait en cache malgré modifications JSON

**✅ Solution**:

**1. Simplifier le tool à UN SEUL paramètre visible** :
```python
params['workflowInputs'] = {
    "mappingMode": "defineBelow",
    "value": {
        "idea_id": "={{ $fromAI('idea_id', '', 'string') }}",
        "__operation__": "delete_idea"  # Caché, pour routing interne
    },
    "schema": [
        {
            "id": "idea_id",
            "displayName": "idea_id",
            "required": True,  # SEUL paramètre requis
            "type": "string",
            "description": "ID de l'idée à archiver (format: IDEA-XXXXXXXX)"
        },
        {
            "id": "__operation__",
            "displayName": "__operation__",
            "required": False,
            "display": False,  # Caché à l'utilisateur
            "type": "string"
        }
    ]
}
```

**2. Adapter le Switch pour lire `__operation__`** :
```python
for rule in rules:
    if rule.get('outputKey') == 'delete_idea':
        rule['conditions']['conditions'][0]['leftValue'] = "={{ $json.__operation__ }}"
        rule['conditions']['conditions'][0]['rightValue'] = "delete_idea"
```

**3. Simplifier le code "Prepare Delete Idea"** :
```javascript
const input = $input.first().json;
const requestedId = (input.idea_id || '').trim();

console.log('[DELETE DEBUG] Input:', JSON.stringify(input));
console.log('[DELETE DEBUG] Requested ID:', requestedId);

if (!requestedId) {
  return [{ json: {
    response: '❌ Paramètre manquant.\n\nUtilisation: delete_idea(idea_id="IDEA-XXXXXXXX")',
    error: true
  } }];
}

const allIdeas = $('Notion - Get Ideas For Delete').all();
const idea = allIdeas.find(item => {
  const id = (item.json.property_id || '').trim();
  return id === requestedId;
});

if (!idea) {
  const errorResponse = `❌ Idée "${requestedId}" non trouvée.\n\nVérifie l'ID avec search_ideas().`;
  return [{ json: { response: errorResponse, error: true } }];
}

return [{
  json: {
    id: requestedId,
    notion_page_id: idea.json.id,
    title: idea.json.property_titre_de_l_id_e || 'Sans titre'
  }
}];
```

**4. Forcer nouveau node avec UUID frais** :
```python
# Supprimer complètement l'ancien node
workflow['nodes'] = [n for n in workflow['nodes'] if n['name'] != 'Notion - Get Ideas For Delete']

# Créer nouveau node avec nouveau UUID
new_node_id = str(uuid.uuid4()).replace('-', '')[:24]  # d7752c10dea141d0a2488dc4
new_node = {
    "parameters": search_ideas_node['parameters'].copy(),
    "type": "n8n-nodes-base.notion",
    "typeVersion": 2.2,
    "id": new_node_id,
    "name": "Notion - Get Ideas For Delete"
}
```

**5. Déployer avec script Python** :
```bash
python3 scripts/fix-delete-tool-params.py
./scripts/deploy.sh
```

**🔄 Prévention**:
- **Minimalisme des paramètres** : Ne demander QUE ce qui est strictement nécessaire
- **Regarder les tools qui fonctionnent** : S'inspirer de `create_idea`, `update_idea`, etc.
- **Tester avec l'agent** : Vérifier que l'agent peut réellement appeler le tool
- **Debug logging** : Ajouter `console.log('[DEBUG] Input:', JSON.stringify(input))` pour voir ce qui arrive
- **Paramètres cachés pour routing** : Utiliser `display: false` pour paramètres internes
- **Remplacer nodes problématiques** : Si cache persiste, supprimer et recréer avec nouveau UUID
- **Éviter Python boolean errors** : Utiliser `True/False` pas `true/false` dans scripts Python

**🔗 Références**:
- [LangChain Tool Workflow n8n](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.toolworkflow/)
- [n8n Expression Resolution](https://docs.n8n.io/code/expressions/)
- Script fix: `scripts/fix-delete-tool-params.py`
- Script deploy: `scripts/deploy.sh`

**💡 Leçons apprises**:
1. **KISS principle** : Simplifier au maximum, ne pas sur-ingénierer
2. **User feedback crucial** : "Regarde les tools qui fonctionnent" → clé de la solution
3. **Debugging méthodique** : Input structure → Routing → Execution → Response
4. **Ne JAMAIS utiliser boolean lowercase en Python** : `True` pas `true`

---

---

## Expressions & Variables

<!-- Les bugs liés aux expressions n8n, $json, $node(), etc. -->

---

## API & Intégrations

### [BUG-001] delete_idea prétend supprimer mais archive seulement

**Date**: 2025-10-31
**Catégorie**: API/Integration
**Sévérité**: 🟡 Important
**Workflow(s) affecté(s)**: MCP - Idée Dev Nico (Perso)

**🔍 Symptômes**:
- L'outil `delete_idea` retourne un message de succès "supprimée avec succès"
- L'idée reste visible dans la database Notion
- L'utilisateur pense que la suppression a échoué

**🎯 Cause racine**:
L'API Notion ne permet PAS la suppression définitive de pages. Seulement l'archivage.
Le node Notion utilise l'opération `archive` qui:
- Marque la page comme archivée
- La cache de la vue par défaut
- Mais ne la supprime PAS définitivement

C'est une **limitation de l'API Notion**, pas du workflow n8n.

**✅ Solution**:
1. Corriger la description du tool `delete_idea` pour être honnête:
   ```
   "Archive une idée dans Notion (équivalent à suppression).
   L'idée sera archivée et n'apparaîtra plus dans les recherches.
   Note: L'API Notion ne permet pas la suppression définitive."
   ```

2. Mettre à jour les notes du node "Notion - Delete Idea":
   ```
   ⚠️ Archive l'idée dans Notion

   IMPORTANT: L'API Notion ne permet pas la suppression définitive.
   La page est archivée et n'apparaît plus dans les vues.
   ```

3. Corriger les messages de succès pour dire "archivée" au lieu de "supprimée"

**🔄 Prévention**:
- Toujours vérifier les limitations de l'API externe avant de promettre des fonctionnalités
- Documenter clairement les limitations dans les descriptions des tools MCP
- Être transparent avec l'utilisateur sur ce qui se passe réellement

**🔗 Références**:
- [Notion API - Archive page](https://developers.notion.com/reference/archive-a-page)
- Note: Aucun endpoint "delete" n'existe dans l'API Notion

---

## Performance & Mémoire

<!-- Les bugs de performance, timeouts, mémoire excessive -->

---

## Credentials & Auth

<!-- Les bugs d'authentification, credentials, tokens -->

---

## 📊 Statistiques

**Total bugs documentés**: 3
**Bugs résolus**: 3
**Bugs récurrents**: 0

**Dernière mise à jour**: 2025-10-31

**Par sévérité**:
- 🔴 Critique: 2 (Agent hallucination, delete_idea workflow error)
- 🟡 Important: 1 (delete_idea API limitation)
- 🟢 Mineur: 0

**Top 3 bugs les plus fréquents**:
1. Tool parameters mal configurés (BUG-003)
2. Agent hallucination au lieu d'utiliser tools (BUG-002)
3. API limitations non documentées (BUG-001)

---

## 🔍 Guide de Recherche Rapide

### Par Symptôme
```bash
# Chercher par message d'erreur
grep -i "error message" BUGS_KNOWLEDGE.md

# Chercher par node
grep -i "Telegram" BUGS_KNOWLEDGE.md

# Chercher par workflow
grep -i "workflow-name" BUGS_KNOWLEDGE.md
```

### Par Catégorie
```bash
# Tous les bugs critiques
grep "🔴 Critique" BUGS_KNOWLEDGE.md

# Bugs d'un node spécifique
grep -A 20 "## Langchain & Agents" BUGS_KNOWLEDGE.md
```

---

## 🎓 Patterns de Bugs Récurrents

### Pattern 1: _À identifier_
**Fréquence**: _À mesurer_
**Impact**: _À évaluer_
**Solution générique**: _À documenter_

---

## 📝 Changelog

### 2025-10-31
- Création de la base de connaissances
- Structure initiale mise en place
