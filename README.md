# 🤖 n8n Agent - Workflows Repository

Dépôt centralisé pour les workflows n8n organisés par système avec déploiement automatique vers `https://auto.mhms.fr/`.

## 📁 Structure du projet

```
n8n Agent/
├── README.md                          # Ce fichier
├── DEPLOYMENT.md                      # Guide de déploiement
├── claude.md                          # Instructions pour Claude (développeur IA)
├── BUGS_KNOWLEDGE.md                  # 🐛 Base de connaissances bugs (NOUVEAU)
├── .env.example                       # Template configuration
├── .env                               # Configuration (non versionné)
├── .gitignore                         # Fichiers ignorés par git
├── .claude/
│   ├── commands/
│   │   └── bug.md                    # Commande /bug workflow automatisé
│   └── settings.local.json
├── scripts/
│   ├── deploy.sh                      # Script de déploiement (bash)
│   └── deploy.js                      # Script de déploiement (node.js)
└── [Systèmes de workflows]/
    ├── Agent Telegram - Dev Nico Perso/
    │   ├── README.md                  # Documentation du système
    │   └── workflow/
    │       ├── workflow1.json
    │       └── workflow2.json
    └── [Autre système]/
        ├── README.md
        └── workflow/
            └── workflow.json
```

## 🎯 Organisation

### Systèmes de workflows

Chaque dossier de premier niveau représente un **système** ou **groupe de workflows** liés fonctionnellement.

**Exemple**: "Agent Telegram - Dev Nico Perso" contient:
- Un workflow Telegram bot avec agent IA
- Un workflow MCP server pour Notion
- Ces 2 workflows travaillent ensemble pour capturer des idées

### Documentation obligatoire

Chaque système DOIT avoir:
- Un dossier `workflow/` contenant les fichiers JSON
- Un fichier `README.md` expliquant:
  - 🎯 L'objectif du système
  - 📋 La description détaillée
  - 🔄 Les workflows inclus
  - 🔌 Les intégrations externes
  - 🔑 Les credentials nécessaires
  - 🏗️ L'architecture
  - 💡 Les cas d'usage
  - 🔧 Les notes de maintenance

## 🐛 Gestion des Bugs (NOUVEAU)

### Base de Connaissances

Le fichier **BUGS_KNOWLEDGE.md** répertorie tous les bugs rencontrés et résolus dans les workflows n8n.

**Objectif**: Éviter de résoudre deux fois le même problème.

### Workflow Automatisé

Utilise la commande `/bug` (pour Claude Code) qui lance automatiquement:

1. ✅ **Recherche** dans la base de connaissances
2. ✅ **Application** solution si bug connu
3. ✅ **Résolution** si bug nouveau
4. ✅ **Documentation** immédiate dans BUGS_KNOWLEDGE.md
5. ✅ **Statistiques** mises à jour

### Recherche Manuelle

```bash
# Chercher par node
grep -i "telegram" BUGS_KNOWLEDGE.md
grep -i "mcp client" BUGS_KNOWLEDGE.md

# Chercher par sévérité
grep "🔴 Critique" BUGS_KNOWLEDGE.md
grep "🟡 Important" BUGS_KNOWLEDGE.md

# Chercher par type d'erreur
grep -i "timeout" BUGS_KNOWLEDGE.md
grep -i "authentication" BUGS_KNOWLEDGE.md
```

### Format de Documentation

Chaque bug documenté suit une structure standardisée:

```markdown
### [BUG-XXX] Titre descriptif

**Date**: YYYY-MM-DD
**Catégorie**: Node/API/Performance/Expression/MCP/Integration/Auth
**Sévérité**: 🔴 Critique | 🟡 Important | 🟢 Mineur
**Workflow(s) affecté(s)**: Nom du workflow

**🔍 Symptômes**: Comportement observé et messages d'erreur
**🎯 Cause racine**: Explication technique précise
**✅ Solution**: Étapes de résolution avec code/config
**🔄 Prévention**: Bonnes pratiques pour éviter ce bug
**🔗 Références**: Liens documentation officielle
```

### Règle Critique

**AVANT de débugger**: TOUJOURS consulter BUGS_KNOWLEDGE.md
**APRÈS avoir résolu**: TOUJOURS documenter immédiatement

---

## 🚀 Déploiement

### Quick Start

```bash
# 1. Configurer votre clé API
cp .env.example .env
nano .env  # Ajoutez votre N8N_API_KEY

# 2. Lister les workflows existants
./scripts/list.sh

# 3. Tester le déploiement (sans modifications)
./scripts/deploy.sh --dry-run

# 4. Déployer réellement
./scripts/deploy.sh
```

### Commandes disponibles

**Liste des workflows**
```bash
./scripts/list.sh
```
Affiche tous les workflows déployés sur votre instance, groupés par statut (actif/pause).

**Déploiement**
```bash
./scripts/deploy.sh              # Déployer tous les workflows
./scripts/deploy.sh --dry-run    # Test sans modification
./scripts/deploy.sh --dir "Nom"  # Déployer un dossier spécifique
```

### Guide complet

Consultez [DEPLOYMENT.md](./DEPLOYMENT.md) pour:
- Configuration détaillée
- Toutes les options disponibles
- Résolution de problèmes
- Bonnes pratiques de sécurité

## 📚 Systèmes disponibles

### 1. Agent Telegram - Dev Nico Perso

Bot Telegram intelligent pour capturer et organiser automatiquement des idées de développement dans Notion.

**Workflows**:
- `Agent Telegram - Dev Ideas.json` - Bot principal avec agent Claude
- `MCP - Idée Dev Nico (Perso) (1).json` - Serveur MCP pour Notion

**Technologies**: Telegram, Claude Sonnet 4.5, OpenAI Whisper, Notion, MCP

[📖 Documentation complète](./Agent%20Telegram%20-%20Dev%20Nico%20Perso/README.md)

---

## 🛠️ Développement

### Ajouter un nouveau système

1. **Créer le dossier du système**
   ```bash
   mkdir "Nouveau Système"
   mkdir "Nouveau Système/workflow"
   ```

2. **Créer le README.md**
   ```bash
   # Utiliser le template depuis claude.md
   nano "Nouveau Système/README.md"
   ```

3. **Ajouter vos workflows JSON**
   ```bash
   # Exporter depuis n8n ou créer manuellement
   cp workflow.json "Nouveau Système/workflow/"
   ```

4. **Déployer**
   ```bash
   ./scripts/deploy.sh --dir "Nouveau Système"
   ```

### Modifier un workflow existant

1. **Éditer le fichier JSON local**
   ```bash
   nano "Système/workflow/workflow.json"
   ```

2. **Mettre à jour le README si nécessaire**
   ```bash
   nano "Système/README.md"
   ```

3. **Déployer les changements**
   ```bash
   ./scripts/deploy.sh --dir "Système"
   ```

## 🤖 Claude AI Developer

Ce projet utilise Claude Code avec le **SuperClaude Framework** complet. Le fichier `claude.md` contient toutes les instructions et le contexte pour qu'il puisse:

- Créer de nouveaux workflows
- Modifier des workflows existants
- Maintenir la documentation à jour
- Optimiser les architectures
- **Résoudre des problèmes avec workflow automatisé** (`/bug`)
- **Consulter automatiquement** la base de connaissances avant debugging
- **Documenter systématiquement** les bugs résolus
- Utiliser 25+ commandes spécialisées et 15+ agents experts
- **Autonomie complète** sur décisions techniques

## 🔐 Sécurité

### Fichiers sensibles (non versionnés)

- `.env` - Contient votre clé API n8n
- Credentials dans les workflows (si applicable)

### Bonnes pratiques

1. **Ne jamais commiter** de clés API ou credentials
2. **Utiliser `.env`** pour toute configuration sensible
3. **Régénérer les clés** régulièrement
4. **Tester avec `--dry-run`** avant déploiement production

## 📖 Documentation

- [README.md](./README.md) - Ce fichier (vue d'ensemble)
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Guide de déploiement complet
- [CLAUDE.md](./CLAUDE.md) - Instructions pour Claude Code avec SuperClaude
- [BUGS_KNOWLEDGE.md](./BUGS_KNOWLEDGE.md) - Base de connaissances bugs (NOUVEAU)
- [.claude/commands/bug.md](./.claude/commands/bug.md) - Workflow automatisé `/bug`
- [Systèmes individuels](.) - README.md dans chaque dossier de système

## 🆘 Support

### Problèmes de déploiement

Consultez la section [Résolution de problèmes](./DEPLOYMENT.md#résolution-de-problèmes) dans DEPLOYMENT.md

### Questions sur n8n

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Community](https://community.n8n.io/)
- [n8n API Reference](https://docs.n8n.io/api/)

## 📝 Changelog

### 2025-10-31 v2.0 - Système de Gestion des Bugs

- 🐛 **NOUVEAU**: Base de connaissances bugs (BUGS_KNOWLEDGE.md)
- 🤖 **NOUVEAU**: Commande `/bug` pour workflow automatisé
- 📊 **NOUVEAU**: Statistiques et patterns de bugs
- 🚀 **AMÉLIORATION**: SuperClaude Framework intégration complète
- 🎯 **AMÉLIORATION**: Autonomie totale Claude Code
- 📚 **AMÉLIORATION**: Documentation enrichie avec process de debugging

### 2025-10-31 v1.0 - Release Initiale

- ✨ Mise en place du système de déploiement automatique
- 📚 Documentation complète (README, DEPLOYMENT, claude.md)
- 🤖 Configuration Claude AI comme développeur expert
- 📦 Premier système: Agent Telegram - Dev Nico Perso

## 🚀 Roadmap

- [ ] CI/CD avec GitHub Actions pour déploiement auto sur push
- [ ] Validation des workflows avant déploiement
- [ ] Backup automatique avant chaque déploiement
- [ ] Dashboard de monitoring des workflows déployés
- [ ] Tests automatisés des workflows
- [ ] Versionning sémantique des workflows

## 📄 License

Private - Usage personnel Nicolas Marillot

---

**Maintenu par**: Claude AI + Nicolas Marillot
**Instance n8n**: https://auto.mhms.fr/
