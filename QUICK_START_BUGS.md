# 🐛 Guide Rapide - Gestion des Bugs

Guide de démarrage rapide pour le système de gestion des bugs.

---

## 🚀 Pour Claude Code

### Quand tu rencontres un bug

**Méthode 1: Automatique (RECOMMANDÉ)**
```bash
/bug
```

Cette commande unique gère tout automatiquement:
1. Recherche dans BUGS_KNOWLEDGE.md
2. Applique solution si bug connu
3. Résout et documente si bug nouveau
4. Met à jour statistiques
5. Sauvegarde checkpoint

**Méthode 2: Manuelle**
```bash
# 1. Recherche
grep -i "telegram" BUGS_KNOWLEDGE.md
grep -i "timeout" BUGS_KNOWLEDGE.md

# 2. Si trouvé → Applique solution
# 3. Si pas trouvé → Résous + documente
```

### Format de documentation

Utilise TOUJOURS ce format dans BUGS_KNOWLEDGE.md:

```markdown
### [BUG-XXX] Titre court descriptif

**Date**: 2025-10-31
**Catégorie**: Node | API | Performance | Expression | MCP | Integration | Auth
**Sévérité**: 🔴 Critique | 🟡 Important | 🟢 Mineur
**Workflow(s) affecté(s)**: Nom exact du workflow

**🔍 Symptômes**:
- Comportement exact observé
- Message d'erreur complet
- Étapes de reproduction

**🎯 Cause racine**:
Explication technique précise (PAS "ça marche pas")

**✅ Solution**:
1. Étape 1 précise
2. Code/config BEFORE → AFTER
3. Commande de validation

**🔄 Prévention**:
- Pattern à éviter
- Best practice à suivre
- Validation automatique si possible

**🔗 Références**:
- https://docs.n8n.io/relevant-page
- GitHub issue si applicable
```

---

## 👤 Pour Développeurs Humains

### Avant de debugger

**TOUJOURS consulter la base de connaissances**:

```bash
# Chercher par node
grep -i "telegram" BUGS_KNOWLEDGE.md
grep -i "http request" BUGS_KNOWLEDGE.md

# Chercher par erreur
grep -i "timeout" BUGS_KNOWLEDGE.md
grep -i "authentication failed" BUGS_KNOWLEDGE.md

# Chercher bugs critiques uniquement
grep "🔴 Critique" BUGS_KNOWLEDGE.md
```

### Après avoir résolu un bug

**IMMÉDIATEMENT documenter**:

1. Ouvrir `BUGS_KNOWLEDGE.md`
2. Trouver dernier numéro de bug:
   ```bash
   grep "### \[BUG-" BUGS_KNOWLEDGE.md | tail -1
   ```
3. Ajouter nouveau bug avec numéro suivant
4. Remplir TOUS les champs du template
5. Mettre à jour statistiques en bas du fichier

### Statistiques

Garder à jour:

```markdown
## 📊 Statistiques

**Total bugs documentés**: X
**Bugs résolus**: X
**Bugs récurrents**: X

**Top 3 bugs les plus fréquents**:
1. [BUG-XXX] - Nom (X occurrences)
2. [BUG-YYY] - Nom (Y occurrences)
3. [BUG-ZZZ] - Nom (Z occurrences)
```

---

## 📋 Catégories de Bugs

### Node
Problèmes liés à un node n8n spécifique
- Telegram node
- HTTP Request node
- Agent node
- Code node
- etc.

### API
Problèmes d'intégration API externe
- Timeout
- Rate limiting
- Authentication
- Response parsing

### Performance
Problèmes de performance
- Workflow trop lent
- Mémoire excessive
- Timeout execution

### Expression
Problèmes avec expressions n8n
- Syntaxe invalide
- Scope variables
- Type conversion

### MCP
Problèmes MCP (Model Context Protocol)
- Server SSE connection
- Tool registration
- Trigger activation

### Integration
Problèmes d'intégration services
- Notion API
- OpenAI API
- Telegram API

### Auth
Problèmes authentification
- Credentials invalides
- Token expiration
- Permissions

---

## 🎯 Exemples Concrets

### Exemple 1: Bug Telegram Timeout

```bash
# Recherche
grep -i "telegram" BUGS_KNOWLEDGE.md
grep -i "timeout" BUGS_KNOWLEDGE.md

# Si trouvé → Appliquer solution documentée
# Si pas trouvé → Documenter:
```

```markdown
### [BUG-001] Telegram webhook timeout après 60 secondes

**Date**: 2025-10-31
**Catégorie**: Integration
**Sévérité**: 🟡 Important
**Workflow(s) affecté(s)**: Agent Telegram - Dev Ideas

**🔍 Symptômes**:
- Webhook Telegram timeout après 60s
- Message erreur: "Request timeout after 60000ms"
- Workflows longs (>60s) échouent

**🎯 Cause racine**:
Telegram impose timeout 60s sur webhooks. Workflows avec
processing long (transcription audio, LLM) dépassent cette limite.

**✅ Solution**:
1. Passer en mode polling au lieu de webhook
2. Dans Telegram Trigger node:
   - Mode: Polling
   - Interval: 10 seconds
3. Ou découper workflow en 2 parties:
   - Partie 1: Réception rapide + ACK
   - Partie 2: Processing long en async

**🔄 Prévention**:
- Utiliser polling pour workflows >30s
- Découper processing long en async
- Toujours ACK webhook rapidement (<5s)

**🔗 Références**:
- https://docs.n8n.io/integrations/builtin/trigger-nodes/n8n-nodes-base.telegramtrigger/
- https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this
```

### Exemple 2: Bug MCP Server Connection

```markdown
### [BUG-002] MCP Server SSE connection failed

**Date**: 2025-10-31
**Catégorie**: MCP
**Sévérité**: 🔴 Critique
**Workflow(s) affecté(s)**: MCP - Idée Dev Nico (Perso)

**🔍 Symptômes**:
- MCP Client node erreur "SSE connection failed"
- Workflow ne peut pas démarrer
- Server MCP accessible manuellement

**🎯 Cause racine**:
Port MCP server changé dans config mais pas mis à jour
dans MCP Client node.

**✅ Solution**:
1. Vérifier port dans MCP server config
2. Mettre à jour MCP Client node:
   - Server URL: http://localhost:CORRECT_PORT
3. Tester connexion

**🔄 Prévention**:
- Centraliser config ports dans .env
- Documenter ports dans README système
- Valider connexion MCP avant déploiement

**🔗 Références**:
- https://modelcontextprotocol.io/
```

---

## ⚡ Commandes Utiles

```bash
# Statistiques
echo "Total bugs: $(grep -c '### \[BUG-' BUGS_KNOWLEDGE.md)"
echo "Bugs critiques: $(grep -c '🔴 Critique' BUGS_KNOWLEDGE.md)"

# Derniers bugs
grep "### \[BUG-" BUGS_KNOWLEDGE.md | tail -5

# Bugs non résolus (si marqués comme tels)
grep -A 5 "🔴 Non résolu" BUGS_KNOWLEDGE.md

# Recherche multi-termes
grep -E "(telegram|webhook)" BUGS_KNOWLEDGE.md

# Bugs d'un workflow spécifique
grep -A 10 "Workflow.*Agent Telegram" BUGS_KNOWLEDGE.md
```

---

## 🔄 Workflow Complet (Exemple)

### Scénario: Workflow Telegram échoue avec erreur timeout

```bash
# 1. CONSULTATION (OBLIGATOIRE)
grep -i "telegram" BUGS_KNOWLEDGE.md
grep -i "timeout" BUGS_KNOWLEDGE.md

# 2a. SI BUG CONNU (ex: BUG-001)
#     → Lire solution
#     → Appliquer: passer en mode polling
#     → Valider: tester workflow
#     → Incrémenter compteur récurrent si applicable

# 2b. SI BUG NOUVEAU
#     → Diagnostic: identifier cause (webhook 60s limit)
#     → Solution: mode polling
#     → Test: valider que ça marche
#     → Documentation: ajouter BUG-00X dans BUGS_KNOWLEDGE.md

# 3. DOCUMENTATION
#    → Ouvrir BUGS_KNOWLEDGE.md
#    → Trouver prochain numéro: BUG-00X
#    → Ajouter dans section "Integration"
#    → Remplir template complet
#    → Mettre à jour statistiques

# 4. FINALISATION
#    → Commit changements
#    → /sc:save (pour Claude)
```

---

## 📚 Ressources

### Documentation
- [BUGS_KNOWLEDGE.md](./BUGS_KNOWLEDGE.md) - Base complète
- [CLAUDE.md](./CLAUDE.md) - Instructions Claude
- [README.md](./README.md) - Vue d'ensemble projet

### Commandes Claude
- `/bug` - Workflow automatisé complet
- `/sc:troubleshoot` - Aide au debugging
- `/sc:research` - Recherche solutions
- `/sc:save` - Checkpoint

### Documentation n8n
- https://docs.n8n.io/
- https://community.n8n.io/
- https://docs.n8n.io/api/

---

## ✅ Checklist Debugging

- [ ] Consulter BUGS_KNOWLEDGE.md AVANT de commencer
- [ ] Rechercher minimum 3 keywords différents
- [ ] Si bug connu, appliquer solution exacte
- [ ] Si bug nouveau, identifier cause racine (pas juste symptôme)
- [ ] Tester solution avant de documenter
- [ ] Documenter IMMÉDIATEMENT après résolution
- [ ] Suivre format template à 100%
- [ ] Mettre à jour statistiques
- [ ] Commit et checkpoint

---

**Maintenu par**: Claude Code + SuperClaude Framework
**Dernière mise à jour**: 2025-10-31
