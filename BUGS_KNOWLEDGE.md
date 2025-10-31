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

<!-- Les bugs liés à l'intégration MCP, serveurs SSE, tools, triggers -->

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

**Total bugs documentés**: 2
**Bugs résolus**: 2
**Bugs récurrents**: 0

**Dernière mise à jour**: 2025-10-31

**Par sévérité**:
- 🔴 Critique: 1 (Agent hallucination)
- 🟡 Important: 1 (delete_idea API limitation)
- 🟢 Mineur: 0

**Top 3 bugs les plus fréquents**:
1. _À venir_
2. _À venir_
3. _À venir_

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
