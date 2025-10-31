# 🚀 Déploiement des Workflows n8n

Ce document explique comment déployer automatiquement vos workflows locaux vers votre instance n8n hébergée sur `https://auto.mhms.fr/`.

## 📋 Table des matières

- [Prérequis](#prérequis)
- [Configuration initiale](#configuration-initiale)
- [Utilisation](#utilisation)
- [Fonctionnement](#fonctionnement)
- [Résolution de problèmes](#résolution-de-problèmes)

---

## ✅ Prérequis

1. **Node.js** installé (version 14 ou supérieure)
2. **Accès à votre instance n8n** (`https://auto.mhms.fr/`)
3. **Clé API n8n** (voir section Configuration)

---

## ⚙️ Configuration initiale

### 1. Obtenir votre clé API n8n

1. Connectez-vous à votre instance n8n: `https://auto.mhms.fr/`
2. Allez dans **Settings** > **API** (ou **Paramètres** > **API**)
3. Cliquez sur **Create API Key** (Créer une clé API)
4. Copiez la clé générée

### 2. Configurer les variables d'environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env
nano .env
```

Remplissez les valeurs dans `.env`:

```bash
# n8n instance URL
N8N_HOST=https://auto.mhms.fr

# n8n API Key (obtenue à l'étape 1)
N8N_API_KEY=n8n_api_1234567890abcdef

# Dry run mode (false pour déployer réellement)
DRY_RUN=false
```

**⚠️ IMPORTANT**: Ne commitez JAMAIS le fichier `.env` dans git (déjà ignoré par `.gitignore`)

---

## 🎯 Utilisation

### Déploiement de tous les workflows

```bash
./scripts/deploy.sh
```

### Test sans modification (Dry Run)

Recommandé pour la première fois:

```bash
./scripts/deploy.sh --dry-run
```

### Déploiement d'un dossier spécifique

```bash
./scripts/deploy.sh --dir "Agent Telegram - Dev Nico Perso"
```

### Aide et options

```bash
./scripts/deploy.sh --help
```

---

## 🔧 Fonctionnement

### Architecture du système

```
┌─────────────────────────┐
│  Workflows Locaux       │
│  (fichiers JSON)        │
└────────┬────────────────┘
         │
         │ 1. Lecture
         ▼
┌─────────────────────────┐
│  Script de déploiement  │
│  (deploy.js)            │
└────────┬────────────────┘
         │
         │ 2. API Request
         │ X-N8N-API-KEY
         ▼
┌─────────────────────────┐
│  n8n API REST           │
│  auto.mhms.fr           │
└────────┬────────────────┘
         │
         │ 3. Create/Update
         ▼
┌─────────────────────────┐
│  Workflows Déployés     │
│  (instance n8n)         │
└─────────────────────────┘
```

### Logique de déploiement

Le script effectue les opérations suivantes:

1. **Scan des workflows locaux**
   - Parcourt récursivement tous les dossiers
   - Cherche les dossiers nommés `workflow/`
   - Trouve tous les fichiers `.json`

2. **Récupération workflows distants**
   - Appelle `GET /api/v1/workflows`
   - Liste tous les workflows existants sur le serveur

3. **Comparaison par nom**
   - Compare `workflow.name` local vs distant
   - Si existe → **UPDATE** (PUT)
   - Si nouveau → **CREATE** (POST)

4. **Déploiement**
   - Envoie le JSON complet du workflow
   - Préserve l'ID pour les updates
   - Affiche le résultat (✅ succès, ❌ erreur)

### Endpoints API utilisés

| Endpoint | Méthode | Usage |
|----------|---------|-------|
| `/api/v1/workflows` | GET | Liste workflows existants |
| `/api/v1/workflows` | POST | Crée nouveau workflow |
| `/api/v1/workflows/:id` | PUT | Met à jour workflow existant |

### Authentification

```javascript
headers: {
  'X-N8N-API-KEY': 'votre_api_key',
  'Content-Type': 'application/json'
}
```

---

## 🔍 Exemples d'utilisation

### Exemple 1: Premier déploiement (Dry Run)

```bash
$ ./scripts/deploy.sh --dry-run

🚀 n8n Workflow Deployment
══════════════════════════════════════════════════
📍 Target: https://auto.mhms.fr
📁 Source: /Users/you/Devs/n8n Agent
🔍 DRY RUN MODE - No changes will be made
══════════════════════════════════════════════════

🔍 Scanning for workflows...
   Found 2 workflow(s)

🌐 Fetching remote workflows...
   Found 0 remote workflow(s)

📤 Deploying workflows...

📦 Processing: Agent Telegram - Dev Ideas.json
   ✨ Would create: Agent Telegram - Dev Ideas

📦 Processing: MCP - Idée Dev Nico (Perso) (1).json
   ✨ Would create: MCP - Idée Dev Nico (Perso)

══════════════════════════════════════════════════
📊 Deployment Summary
══════════════════════════════════════════════════
✅ Successful: 2/2
   📝 Created: 2
   🔄 Updated: 0

✨ Deployment completed successfully!
```

### Exemple 2: Déploiement réel

```bash
$ ./scripts/deploy.sh

🚀 n8n Workflow Deployment
══════════════════════════════════════════════════
📍 Target: https://auto.mhms.fr
📁 Source: /Users/you/Devs/n8n Agent
══════════════════════════════════════════════════

🔍 Scanning for workflows...
   Found 2 workflow(s)

🌐 Fetching remote workflows...
   Found 0 remote workflow(s)

📤 Deploying workflows...

📦 Processing: Agent Telegram - Dev Ideas.json
   ✨ Creating: Agent Telegram - Dev Ideas
   ✅ Created successfully (ID: Xa4F7kPQ91z5bYmR)

📦 Processing: MCP - Idée Dev Nico (Perso) (1).json
   ✨ Creating: MCP - Idée Dev Nico (Perso)
   ✅ Created successfully (ID: Yb3G8lQR82a6cZnS)

══════════════════════════════════════════════════
📊 Deployment Summary
══════════════════════════════════════════════════
✅ Successful: 2/2
   📝 Created: 2
   🔄 Updated: 0

✨ Deployment completed successfully!
```

### Exemple 3: Update d'un workflow existant

```bash
$ ./scripts/deploy.sh

📦 Processing: Agent Telegram - Dev Ideas.json
   🔄 Updating: Agent Telegram - Dev Ideas (ID: Xa4F7kPQ91z5bYmR)
   ✅ Updated successfully

══════════════════════════════════════════════════
📊 Deployment Summary
══════════════════════════════════════════════════
✅ Successful: 2/2
   📝 Created: 0
   🔄 Updated: 2
```

---

## 🚨 Résolution de problèmes

### Erreur: N8N_API_KEY not found

**Symptôme**:
```
❌ Error: N8N_API_KEY environment variable is required
```

**Solution**:
1. Vérifiez que le fichier `.env` existe
2. Vérifiez que `N8N_API_KEY` est défini dans `.env`
3. Vérifiez qu'il n'y a pas d'espaces autour du `=`

### Erreur: API Error 401

**Symptôme**:
```
❌ Failed: API Error 401: Unauthorized
```

**Solution**:
- Votre clé API est invalide ou expirée
- Générez une nouvelle clé dans n8n Settings > API
- Mettez à jour `.env` avec la nouvelle clé

### Erreur: API Error 404

**Symptôme**:
```
❌ Failed: API Error 404: Not Found
```

**Solution**:
- Vérifiez que `N8N_HOST` dans `.env` est correct
- Vérifiez que votre instance n8n est accessible
- Testez: `curl https://auto.mhms.fr/api/v1/workflows`

### Erreur: Failed to parse JSON

**Symptôme**:
```
❌ Failed to load workflow.json: Unexpected token
```

**Solution**:
- Le fichier JSON du workflow est corrompu
- Vérifiez la syntaxe JSON
- Testez avec: `node -e "JSON.parse(require('fs').readFileSync('workflow.json'))"`

### Workflow ne se met pas à jour

**Symptôme**:
Le workflow est marqué comme "Updated" mais les changements n'apparaissent pas dans n8n.

**Solution**:
- Rafraîchissez la page n8n (Ctrl+R ou Cmd+R)
- Vérifiez que le workflow n'est pas en cours d'édition par un autre utilisateur
- Vérifiez les logs n8n pour d'éventuelles erreurs

### Permission denied sur deploy.sh

**Symptôme**:
```
bash: ./scripts/deploy.sh: Permission denied
```

**Solution**:
```bash
chmod +x scripts/deploy.sh
chmod +x scripts/deploy.js
```

---

## 🔐 Sécurité

### Bonnes pratiques

1. **Ne JAMAIS commiter le fichier `.env`**
   - Le `.gitignore` l'empêche déjà
   - Double-vérifiez avant chaque commit

2. **Régénérer les clés API régulièrement**
   - Tous les 3-6 mois minimum
   - Immédiatement si compromises

3. **Limiter les permissions de la clé API**
   - Si n8n le permet, créez une clé avec accès limité aux workflows
   - Évitez les clés admin si possible

4. **Utiliser HTTPS uniquement**
   - Toujours `https://` dans `N8N_HOST`
   - Jamais `http://` pour éviter interception

5. **Sauvegarder avant déploiement**
   - Utilisez `--dry-run` pour tester
   - Faites un backup de votre instance n8n régulièrement

---

## 📚 Ressources

- [n8n API Documentation](https://docs.n8n.io/api/)
- [n8n REST API Reference](https://docs.n8n.io/api/authentication/)
- [n8n Community Forum](https://community.n8n.io/)

---

## 🆘 Support

En cas de problème:

1. Vérifiez cette documentation
2. Testez avec `--dry-run`
3. Vérifiez les logs de votre instance n8n
4. Consultez la [communauté n8n](https://community.n8n.io/)
