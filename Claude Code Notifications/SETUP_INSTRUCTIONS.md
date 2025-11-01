# 🚀 Instructions de Configuration - Claude Code Notifications

**Configuration complète du système de notifications Telegram pour Claude Code**

---

## 📋 Prérequis

✅ Bot Telegram créé: `@claude_code_nico_bot`
✅ Token bot disponible: `8271481273:AAGbWO6JFwyQo7S10nyszmWt5R1fhaCWeG0`
✅ Numéro de téléphone: `0684789511`

---

## 🔧 Étape 1: Créer la Credential Telegram dans n8n

1. Aller sur https://auto.mhms.fr/
2. Cliquer sur **Settings** (⚙️) → **Credentials**
3. Cliquer sur **Add Credential**
4. Chercher et sélectionner **"Telegram API"**
5. Remplir les informations:
   - **Credential Name**: `Claude Code Bot`
   - **Access Token**: `8271481273:AAGbWO6JFwyQo7S10nyszmWt5R1fhaCWeG0`
6. Cliquer sur **Save**
7. **Noter l'ID de credential généré** (format: `xxxxxxxxxxxx`)

---

## 🔧 Étape 2: Mettre à jour les Workflows avec le bon Credential ID

Les 2 workflows utilisent cette credential. Il faut remplacer `"NEW_CREDENTIAL_ID"` par le vrai ID:

### Workflow 1: Claude Code - Task Notifications.json

**Emplacement**: Node "Send Telegram Notification"

```json
"credentials": {
  "telegramApi": {
    "id": "REMPLACER_PAR_ID_CREDENTIAL",
    "name": "Claude Code Bot"
  }
}
```

### Workflow 2: Claude Code - Interactive Control.json

**Emplacements**:
- Node "Telegram Trigger"
- Node "Send Response"

```json
"credentials": {
  "telegramApi": {
    "id": "REMPLACER_PAR_ID_CREDENTIAL",
    "name": "Claude Code Bot"
  }
}
```

**Comment faire** :
1. Ouvrir chaque fichier JSON dans un éditeur de texte
2. Chercher `"NEW_CREDENTIAL_ID"`
3. Remplacer par l'ID de credential noté à l'étape 1
4. Sauvegarder les fichiers

---

## 🔧 Étape 3: Déployer les Workflows

```bash
# Test avec dry-run d'abord
./scripts/deploy.sh --dry-run --dir "Claude Code Notifications"

# Déploiement réel
./scripts/deploy.sh --dir "Claude Code Notifications"

# Push vers GitHub
git push origin main
```

---

## 🔧 Étape 4: Activer le Workflow Interactive Control

1. Aller sur https://auto.mhms.fr/
2. Ouvrir le workflow **"Claude Code - Interactive Control"**
3. Cliquer sur le toggle **"Active"** en haut à droite
4. Le workflow est maintenant actif et écoute les messages Telegram

---

## 🔧 Étape 5: Initialiser votre Chat ID

**Sur Telegram** :

1. Ouvrir Telegram
2. Chercher `@claude_code_nico_bot`
3. Envoyer `/nomade`

**Ce qui se passe** :
- Le bot reçoit votre message
- Il sauvegarde automatiquement votre Chat ID
- Il active le mode nomade
- Vous recevez une confirmation

**Message de confirmation attendu** :
```
🌍 Mode Nomade Activé

Tu recevras maintenant toutes les notifications et demandes d'approbation de Claude Code sur Telegram.

✅ Tu peux répondre directement aux messages pour contrôler Claude Code à distance.

💾 Ton Chat ID (XXXXXXXXX) est maintenant sauvegardé.

_Activé le DD/MM/YYYY HH:MM:SS_
```

---

## 🔧 Étape 6: Activer le Workflow Task Notifications

1. Aller sur https://auto.mhms.fr/
2. Ouvrir le workflow **"Claude Code - Task Notifications"**
3. Cliquer sur le toggle **"Active"**
4. Le workflow est maintenant prêt à recevoir des appels MCP

---

## ✅ Vérification de l'Installation

### Test 1: Commande /status

Envoyez `/status` au bot. Réponse attendue:
```
🌍 Mode Nomade

📊 Statut:
Toutes notifications actives sur Telegram

🕐 Activé le: DD/MM/YYYY HH:MM:SS
👤 Par: votre_username

_Dernière vérification: DD/MM/YYYY HH:MM:SS_
```

### Test 2: Workflow MCP (via Claude Code)

Claude Code peut maintenant appeler:
```javascript
notify_task_complete({
  task_title: "Test notification",
  summary: "Ceci est un test de notification depuis Claude Code",
  context: "Configuration terminée avec succès"
})
```

Vous devriez recevoir sur Telegram:
```
✅ Test notification

📋 Résumé:
Ceci est un test de notification depuis Claude Code

💡 Contexte:
Configuration terminée avec succès

_Notification envoyée par Claude Code_
```

---

## 🎮 Commandes Disponibles

Une fois configuré, vous pouvez contrôler Claude Code via Telegram:

| Commande | Description |
|----------|-------------|
| `/nomade` | Active le mode nomade (toutes notifications) |
| `/sédentaire` | Désactive le mode nomade (notifications limitées) |
| `/status` | Affiche l'état actuel de Claude Code |
| `approve`, `ok`, `oui` | Approuve une action de Claude Code |
| `deny`, `non` | Refuse une action de Claude Code |

---

## 🐛 Troubleshooting

### Le bot ne répond pas

**Vérifications** :
1. ✅ Workflow "Interactive Control" est actif
2. ✅ Credential Telegram correcte
3. ✅ Token bot valide
4. ✅ Bot Telegram existe et est accessible

**Solution** :
- Vérifier les logs d'exécution dans n8n
- Tester le token avec:
  ```bash
  curl "https://api.telegram.org/bot8271481273:AAGbWO6JFwyQo7S10nyszmWt5R1fhaCWeG0/getMe"
  ```

### Notifications non reçues

**Vérifications** :
1. ✅ Workflow "Task Notifications" est actif
2. ✅ Chat ID est sauvegardé (envoyer `/status` pour vérifier)
3. ✅ Mode nomade activé si vous voulez toutes les notifications

**Solution** :
- Envoyer `/nomade` à nouveau
- Vérifier les logs du workflow "Task Notifications"
- Tester manuellement le workflow dans n8n

### Chat ID non sauvegardé

**Solution** :
- Envoyer `/nomade` au bot
- Vérifier que le workflow "Interactive Control" s'exécute
- Consulter les logs d'exécution dans n8n

---

## 📚 Fichiers du Système

```
Claude Code Notifications/
├── README.md                            # Documentation complète
├── SETUP_INSTRUCTIONS.md                # Ce fichier
└── workflow/
    ├── Claude Code - Task Notifications.json      # Workflow MCP Tool
    └── Claude Code - Interactive Control.json     # Workflow bidirectionnel
```

---

## 🔒 Sécurité

⚠️ **IMPORTANT** :
- **Ne JAMAIS** commiter le token du bot dans Git
- Le token est déjà dans le `.gitignore` via les credentials n8n
- Les credentials n8n ne sont PAS exportées dans les JSON

---

## 🚀 Prochaines Étapes

Après configuration:
1. ✅ Workflows déployés et actifs
2. ✅ Chat ID sauvegardé
3. ✅ Mode nomade configuré
4. ✅ Claude Code peut envoyer des notifications
5. ✅ Vous pouvez contrôler Claude Code via Telegram

**Utilisez maintenant** :
- Claude Code enverra automatiquement des notifications quand des tâches sont terminées
- Vous pouvez activer/désactiver le mode nomade à volonté
- Vous pouvez répondre aux demandes d'approbation directement sur Telegram

---

**Créé le**: 2025-11-01
**Pour**: Nicolas Marillot
**Bot**: @claude_code_nico_bot
