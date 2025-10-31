---
name: bug
description: "Workflow automatisé de gestion des bugs n8n (consultation et documentation)"
---

# 🐛 Bug Management Workflow

Tu dois exécuter le workflow complet de gestion des bugs selon le contexte.

## Contexte

L'utilisateur rencontre un problème avec un workflow n8n ou demande de l'aide pour un bug.

## Workflow Automatique

### ÉTAPE 1: CONSULTATION OBLIGATOIRE

**TOUJOURS commencer par chercher dans BUGS_KNOWLEDGE.md**

```bash
# Recherche multi-keywords automatique
grep -i "[keyword1]" BUGS_KNOWLEDGE.md
grep -i "[keyword2]" BUGS_KNOWLEDGE.md
grep -i "[keyword3]" BUGS_KNOWLEDGE.md
```

**Keywords à extraire du message utilisateur**:
- Nom du node (Telegram, HTTP Request, Agent, etc.)
- Type d'erreur (timeout, auth, parsing, etc.)
- Mots-clés du message d'erreur
- Nom du workflow affecté

### ÉTAPE 2: ANALYSE RÉSULTATS

**Si bug trouvé dans BUGS_KNOWLEDGE.md**:
1. Lire la section complète du bug
2. Afficher à l'utilisateur:
   ```
   🔍 Bug connu détecté: [BUG-XXX]

   📋 Solution documentée:
   [Copier la solution]

   ✅ Application de la solution...
   ```
3. Appliquer la solution documentée
4. Valider que ça fonctionne
5. Mettre à jour statistiques si bug récurrent

**Si bug NON trouvé**:
1. Informer l'utilisateur:
   ```
   🆕 Bug non documenté dans la base de connaissances

   🔧 Activation du mode troubleshooting...
   ```
2. Activer `/sc:troubleshoot` si besoin
3. Procéder à la résolution

### ÉTAPE 3: RÉSOLUTION (si bug nouveau)

1. **Diagnostic**: Identifier la cause racine (pas juste le symptôme)
2. **Solution**: Résoudre le problème complètement
3. **Validation**: Tester que la solution fonctionne
4. **Recherche**: Si nécessaire, `/sc:research` pour solutions officielles

### ÉTAPE 4: DOCUMENTATION (OBLIGATOIRE pour bugs nouveaux)

**IMMÉDIATEMENT après résolution, documenter le bug**:

1. Déterminer le prochain numéro de bug:
   ```bash
   grep "### \[BUG-" BUGS_KNOWLEDGE.md | tail -1
   # Incrémenter le numéro
   ```

2. Ajouter dans la section appropriée de BUGS_KNOWLEDGE.md:
   ```markdown
   ### [BUG-XXX] [Titre descriptif court]

   **Date**: 2025-10-31
   **Catégorie**: [Node/API/Performance/Expression/MCP/Integration/Auth]
   **Sévérité**: 🔴 Critique | 🟡 Important | 🟢 Mineur
   **Workflow(s) affecté(s)**: [Nom exact]

   **🔍 Symptômes**:
   - [Comportement observé exact]
   - [Message d'erreur complet]
   - [Conditions de reproduction]

   **🎯 Cause racine**:
   [Explication technique précise - PAS "ça marche pas"]

   **✅ Solution**:
   1. [Étape 1 de résolution]
   2. [Étape 2 avec code/config before/after]
   3. [Commande de validation]

   **🔄 Prévention**:
   - [Pattern à éviter]
   - [Best practice à suivre]

   **🔗 Références**:
   - [Liens docs n8n officielles]
   - [GitHub issues si applicable]
   ```

3. Mettre à jour les statistiques:
   ```markdown
   **Total bugs documentés**: X
   **Bugs résolus**: X
   ```

4. Si pattern récurrent détecté, mettre à jour:
   ```markdown
   ## 🎓 Patterns de Bugs Récurrents

   ### Pattern X: [Nom du pattern]
   **Fréquence**: X occurrences
   **Impact**: [Description]
   **Solution générique**: [Steps]
   ```

### ÉTAPE 5: FINALISATION

1. Informer l'utilisateur:
   ```
   ✅ Bug résolu et documenté: [BUG-XXX]

   📝 Documentation ajoutée à BUGS_KNOWLEDGE.md
   🔄 Statistiques mises à jour

   La prochaine fois que ce bug apparaît, la solution sera automatiquement disponible!
   ```

2. Checkpoint:
   ```bash
   /sc:save  # Sauvegarder contexte avec nouveau bug documenté
   ```

## Exemples de Keywords à Chercher

### Par Node
- "telegram"
- "http request"
- "agent"
- "mcp client"
- "code node"
- "merge"

### Par Type d'Erreur
- "timeout"
- "authentication"
- "parsing"
- "memory"
- "rate limit"
- "webhook"
- "expression"
- "credential"

### Par Message d'Erreur
- Extraire mots-clés uniques du message d'erreur
- Chercher stack trace signature
- Chercher code d'erreur HTTP

## Règles Critiques

1. **JAMAIS skip la consultation de BUGS_KNOWLEDGE.md**
2. **TOUJOURS documenter les bugs nouveaux IMMÉDIATEMENT**
3. **TOUJOURS identifier la cause racine, pas juste le symptôme**
4. **TOUJOURS mettre à jour les statistiques**
5. **TOUJOURS faire un checkpoint après documentation**

## Format de Réponse à l'Utilisateur

```
🐛 BUG WORKFLOW ACTIVÉ

🔍 RECHERCHE dans base de connaissances...
Keywords: [list]

[SI TROUVÉ]
✅ Bug connu: [BUG-XXX] - [Titre]
📋 Application solution documentée...
[Détails solution]

[SI NON TROUVÉ]
🆕 Nouveau bug détecté
🔧 Résolution en cours...
[Steps de résolution]
📝 Documentation dans BUGS_KNOWLEDGE.md...
✅ Bug [BUG-XXX] documenté

💾 Checkpoint sauvegardé
```
