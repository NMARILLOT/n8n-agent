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

<!-- Les bugs liés aux agents, LLM, memory, etc. -->

---

## MCP Integration

<!-- Les bugs liés à l'intégration MCP, serveurs SSE, tools, triggers -->

---

## Expressions & Variables

<!-- Les bugs liés aux expressions n8n, $json, $node(), etc. -->

---

## API & Intégrations

<!-- Les bugs liés aux appels API externes, webhooks, etc. -->

---

## Performance & Mémoire

<!-- Les bugs de performance, timeouts, mémoire excessive -->

---

## Credentials & Auth

<!-- Les bugs d'authentification, credentials, tokens -->

---

## 📊 Statistiques

**Total bugs documentés**: 0
**Bugs résolus**: 0
**Bugs récurrents**: 0

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
