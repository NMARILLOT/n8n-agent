# 🔧 Guide de Configuration - Global Error Handler

## 📋 Prérequis

Avant de déployer le workflow d'erreur, vous devez avoir :

1. ✅ **Google Sheets Credential** configuré dans n8n
2. ✅ **Telegram Bot Credential** configuré dans n8n
3. ✅ **Google Spreadsheet** créé pour les logs d'erreurs
4. ✅ **Telegram Chat ID** où recevoir les notifications

---

## 🚀 Installation Rapide

### Étape 1: Créer le Google Sheet

1. Créer un nouveau Google Spreadsheet
2. Nommer le: **"n8n Error Logs"**
3. Créer les colonnes suivantes dans Sheet1 (ligne 1):

```
Timestamp | Error ID | Severity | Error Type | Workflow Name | Workflow ID | Node Name | Node Type | Error Message | Stack Trace | Input Data | Execution ID | Execution URL | Duration | Mode
```

4. **Copier le Spreadsheet ID** depuis l'URL:
   ```
   https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_ICI/edit
   ```

### Étape 2: Obtenir votre Telegram Chat ID

**Méthode Simple**:
1. Ouvrir Telegram
2. Chercher le bot `@userinfobot`
3. Envoyer `/start`
4. Il vous donnera votre Chat ID (exemple: `123456789`)

**Alternative avec votre bot**:
1. Envoyer un message à votre bot Telegram
2. Aller sur: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Chercher `"chat":{"id":123456789}`

### Étape 3: Configurer le Workflow

Après déploiement, ouvrir le workflow "Global Error Handler" dans n8n et modifier:

#### Node "Log to Google Sheets"
1. Cliquer sur le node
2. Dans **Document ID**: Sélectionner votre spreadsheet "n8n Error Logs"
3. Dans **Sheet**: Sélectionner "Sheet1"
4. Vérifier que toutes les colonnes sont bien mappées
5. Sauvegarder

#### Node "Format Telegram Alert"
1. Cliquer sur le node
2. Ouvrir l'éditeur de code
3. Ligne 36, remplacer `'YOUR_TELEGRAM_CHAT_ID'` par votre Chat ID (exemple: `'123456789'`)
4. Sauvegarder

#### Node "Send Telegram Alert"
1. Cliquer sur le node
2. Dans **Credentials**: Sélectionner votre credential Telegram
3. Sauvegarder

### Étape 4: Personnaliser les Workflows Critiques

Dans le node "Analyze Error Context", ligne 55-60:

```javascript
const criticalWorkflows = [
  'Agent Telegram - Dev Ideas',           // Vos workflows critiques
  'MCP - Idée Dev Nico (Perso)',
  'Production API',                        // Ajouter les vôtres ici
  'Payment Processing'
];
```

Modifier cette liste avec les noms exacts de VOS workflows critiques.

### Étape 5: Activer le Workflow

1. Dans n8n, activer le workflow "Global Error Handler" (toggle en haut à droite)
2. Vérifier qu'il est bien actif (indicateur vert)

---

## 🔗 Assigner le Workflow d'Erreur

Pour que vos workflows utilisent ce gestionnaire d'erreur:

### Pour chaque workflow à monitorer:

1. Ouvrir le workflow dans n8n
2. Cliquer sur **Settings** (⚙️ en haut)
3. Onglet **Error Workflow**
4. Sélectionner **"Global Error Handler"**
5. Cliquer **Save**
6. Activer le workflow

**Exemple**: Agent Telegram - Dev Ideas
```
Settings → Error Workflow → Select "Global Error Handler" → Save
```

---

## 🧪 Tester le Workflow

### Test Simple

1. Créer un workflow de test:
   - Ajouter un node "Manual Trigger"
   - Ajouter un node "Code" avec du code qui génère une erreur:
     ```javascript
     throw new Error('Test error for Global Error Handler');
     ```
2. Dans Settings, assigner "Global Error Handler" comme Error Workflow
3. Exécuter le workflow
4. Vérifier:
   - ✅ Ligne ajoutée dans Google Sheets
   - ✅ Notification Telegram reçue (si configuré comme critique)

### Test d'Erreur Réelle

1. Temporairement désactiver "Continue on Fail" sur un node qui peut échouer
2. Assigner le workflow d'erreur
3. Déclencher une condition d'échec
4. Vérifier les logs dans Google Sheets

---

## 📊 Comprendre les Logs

### Colonnes du Google Sheet

| Colonne | Description | Exemple |
|---------|-------------|---------|
| **Timestamp** | Date/heure de l'erreur | 2025-01-01T12:34:56.789Z |
| **Error ID** | Identifiant unique | ERR-1704110096789-abc123def |
| **Severity** | Critique, Important, Mineur | Critique |
| **Error Type** | Classification automatique | Authentication |
| **Workflow Name** | Nom du workflow source | Agent Telegram - Dev Ideas |
| **Workflow ID** | ID n8n du workflow | 4lYuNSDjiyUjzHWL |
| **Node Name** | Node qui a échoué | Download Audio |
| **Node Type** | Type de node | n8n-nodes-base.httpRequest |
| **Error Message** | Message d'erreur complet | Request timeout after 30000ms |
| **Stack Trace** | Trace d'exécution | at HttpRequest.execute... |
| **Input Data** | Données d'entrée du node | {"url": "https://..."} |
| **Execution ID** | ID de l'exécution | xyz789 |
| **Execution URL** | Lien direct vers n8n | https://auto.mhms.fr/... |
| **Duration** | Temps avant erreur | 31s |
| **Mode** | Mode d'exécution | manual, trigger, webhook |

### Classification Automatique

Le workflow classe automatiquement les erreurs:

| Type d'Erreur | Détecté par | Sévérité par Défaut |
|---------------|-------------|---------------------|
| **Authentication** | 401, 403, Unauthorized | 🔴 Critique |
| **Timeout** | timeout, ETIMEDOUT | 🟡 Important |
| **Rate Limit** | 429, rate limit | 🟡 Important |
| **Server Error** | 500, 502, 503 | 🟡 Important |
| **Validation** | 400, validation | 🟢 Mineur |
| **Network** | network, ECONNREFUSED | 🟡 Important |
| **Database** | database, SQL | 🔴 Critique |
| **Application** | Autres erreurs | 🟡 Important |

**Note**: Les erreurs dans les workflows critiques sont automatiquement surclassées en "Critique".

---

## 🎨 Personnalisation Avancée

### Modifier les Critères de Criticité

Dans "Analyze Error Context", modifier la logique de classification:

```javascript
// Exemple: Toutes les erreurs API externes sont critiques
if (node.type.includes('httpRequest') && errorMessage.includes('500')) {
  severity = 'Critique';
}

// Exemple: Ignorer certains types d'erreurs
if (errorMessage.includes('expected warning')) {
  severity = 'Mineur';
}
```

### Ajouter d'Autres Canaux de Notification

**Slack**:
1. Ajouter un node "Slack" après "Is Critical Error?"
2. Connecter à la branche "true"
3. Configurer le message avec les données d'erreur

**Email**:
1. Ajouter un node "Send Email"
2. Utiliser les mêmes données formatées
3. Envoyer aux responsables techniques

**PagerDuty** (pour production):
1. Ajouter un node "HTTP Request" vers PagerDuty API
2. Créer un incident automatiquement
3. Uniquement pour erreurs critiques

### Enrichir les Logs

Ajouter des colonnes personnalisées dans Google Sheets:

```javascript
// Dans "Analyze Error Context", ajouter:
environment: process.env.NODE_ENV || 'production',
affectedUser: errorData.execution?.data?.userId || 'system',
retryCount: errorData.execution?.retryCount || 0,
```

---

## 🔍 Maintenance

### Nettoyage Mensuel

1. Ouvrir le Google Sheet
2. Créer un nouvel onglet "Archives [Mois-Année]"
3. Copier les lignes > 90 jours
4. Supprimer de Sheet1

### Review Hebdomadaire

Créer un pivot table dans Google Sheets:
- **Lignes**: Workflow Name
- **Valeurs**: COUNT(Error ID)
- **Filtre**: Derniers 7 jours

Identifier les workflows avec le plus d'erreurs.

### Dashboard (Optionnel)

Google Sheets peut générer des graphiques automatiques:
1. Sélectionner les données
2. Insert → Chart
3. Types utiles:
   - **Line Chart**: Erreurs par jour (Timestamp vs COUNT)
   - **Pie Chart**: Distribution par type d'erreur
   - **Bar Chart**: Top workflows avec erreurs

---

## ⚠️ Troubleshooting

### "Workflow d'erreur ne se déclenche pas"

✅ **Vérifier**:
1. Workflow "Global Error Handler" est ACTIF
2. Workflow source a bien "Global Error Handler" assigné dans Settings
3. L'erreur n'est pas capturée par "Continue on Fail"

### "Pas de notification Telegram"

✅ **Vérifier**:
1. L'erreur est bien classée "Critique"
2. Chat ID correct dans "Format Telegram Alert"
3. Credential Telegram valide
4. Bot a les permissions d'envoyer des messages

### "Google Sheets ne reçoit pas les logs"

✅ **Vérifier**:
1. Spreadsheet ID correct
2. Credential Google Sheets valide
3. Permissions d'écriture sur le sheet
4. Colonnes exactement comme spécifié

### "Erreur: Cannot read property 'id' of undefined"

✅ **Solution**:
Le workflow d'erreur lui-même a une erreur. Vérifier:
1. Tous les credentials sont configurés
2. Spreadsheet ID et Chat ID sont bien renseignés
3. Tester avec un workflow simple d'abord

---

## 📚 Ressources

- [n8n Error Workflow Docs](https://docs.n8n.io/workflows/error-handling/)
- [Google Sheets Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.googlesheets/)
- [Telegram Node](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.telegram/)

---

**Créé**: 2025-11-01
**Maintenu par**: Claude Code + Nicolas Marillot
**Support**: Consulter BUGS_KNOWLEDGE.md pour problèmes connus
