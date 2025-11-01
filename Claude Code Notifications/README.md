# 📢 Claude Code - Task Notifications

Système de notifications Telegram pour signaler automatiquement la fin des tâches Claude Code.

---

## 🎯 Objectif

Permettre à Claude Code d'envoyer des notifications Telegram automatiques quand une tâche est terminée, avec un résumé et du contexte.

**Cas d'usage:**
- Notification de fin de tâches longues (déploiement, analyse, refactoring)
- Alertes de bugs résolus
- Confirmations de mise à jour de documentation
- Résumés de modifications de workflows

---

## 📋 Description Détaillée

Ce workflow expose une fonction MCP `notify_task_complete()` que Claude Code peut appeler pour envoyer des notifications Telegram formatées.

### Flux du Workflow

```
notify_task_complete (MCP Tool)
    ↓
Get User ChatId (Code)
    ↓
Format Message (Code)
    ↓
Send Telegram Notification (Telegram)
    ↓
Response Success (Respond to Webhook)
```

### Paramètres de la Fonction

| Paramètre | Type | Requis | Description |
|-----------|------|--------|-------------|
| `task_title` | string | ✅ Oui | Titre court de la tâche (ex: "Mise à jour CLAUDE.md") |
| `summary` | string | ✅ Oui | Résumé concis (2-3 phrases) |
| `context` | string | ❌ Non | Informations additionnelles (optionnel) |

### Format du Message

Le message Telegram est formaté automatiquement avec:
- **Emoji adapté** selon le type de tâche (bug, deploy, doc, etc.)
- **Titre en gras** (Markdown)
- **Résumé structuré**
- **Contexte** (si fourni)
- **Signature** Claude Code

**Exemple de message:**
```
🚀 **Déploiement workflow notifications**

📋 **Résumé:**
Création d'un nouveau workflow MCP pour envoyer des notifications Telegram quand Claude Code termine une tâche. Le workflow est prêt à être déployé.

💡 **Contexte:**
Le workflow utilise un MCP Tool Workflow avec 3 paramètres: task_title, summary, context. Configuration du chatId requise avant activation.

_Notification envoyée par Claude Code_
```

---

## 🔄 Workflows Inclus

### 1. Claude Code - Task Notifications.json

**Type:** Tool Workflow (MCP Server compatible)

**Fonction exposée:** `notify_task_complete(task_title, summary, context)`

**Nodes:**
1. **notify_task_complete** - MCP Tool Workflow trigger
2. **Get User ChatId** - Code node (récupère le chatId de Nicolas)
3. **Format Message** - Code node (formate le message avec Markdown)
4. **Send Telegram Notification** - Telegram node (envoi du message)
5. **Response Success** - Respond to Webhook (confirmation JSON)

**État:** ⚠️ Inactif (configuration chatId requise)

---

## 🔌 Intégrations Externes

### Telegram Bot

**Credential:** `Telegram Nico Dev (perso)` (ID: `tecnNETDK9d3pNmM`)

**Permissions requises:**
- `sendMessage` - Envoi de messages

**Configuration:**
- Parse mode: Markdown (pour formatage du texte)
- Chat ID: À configurer dans le node "Get User ChatId"

---

## 🔑 Credentials Nécessaires

| Service | Credential Name | ID | Utilisé Dans |
|---------|----------------|-----|--------------|
| Telegram | Telegram Nico Dev (perso) | `tecnNETDK9d3pNmM` | Send Telegram Notification |

---

## 🏗️ Architecture

### MCP Tool Workflow

Ce workflow est conçu comme un **Tool Workflow** compatible MCP:
- Exposé via MCP Server Trigger de n8n
- Appelable par Claude Code/Desktop via MCP Client
- Paramètres structurés avec validation de schema
- Réponse JSON pour confirmation

### Flow de Données

```json
Input (MCP Call):
{
  "task_title": "Mise à jour CLAUDE.md",
  "summary": "Résolution contradiction layout guidelines...",
  "context": "Ajout section distinguant team vs user preference"
}

↓ Get User ChatId

{
  ...input,
  "chatId": "123456789"
}

↓ Format Message

{
  "message": "✅ **Mise à jour CLAUDE.md**\n\n📋...",
  "parse_mode": "Markdown",
  "chatId": "123456789"
}

↓ Send Telegram

{
  "message_id": 12345,
  "chat": {...},
  "text": "..."
}

↓ Response Success

Output (MCP Response):
{
  "status": "success",
  "message": "Notification envoyée",
  "task": "Mise à jour CLAUDE.md"
}
```

---

## 💡 Cas d'Usage

### 1. Notification de Tâche Terminée

```javascript
// Claude Code appelle automatiquement:
notify_task_complete({
  task_title: "Création workflow notifications",
  summary: "Nouveau workflow MCP créé pour notifications Telegram. Inclut formatage automatique et gestion des emojis.",
  context: "Configuration chatId requise avant activation"
})
```

### 2. Alerte Bug Résolu

```javascript
notify_task_complete({
  task_title: "Bug résolu: delete_idea",
  summary: "Le tool delete_idea fonctionne maintenant. Simplification des paramètres à 1 seul (idea_id).",
  context: "Bug documenté dans BUGS_KNOWLEDGE.md [BUG-003]"
})
```

### 3. Confirmation Déploiement

```javascript
notify_task_complete({
  task_title: "Déploiement réussi",
  summary: "3 workflows déployés sur auto.mhms.fr. Tous actifs et testés.",
  context: "Commit: a1b2c3d - Push vers GitHub effectué"
})
```

---

## 🔧 Configuration Requise

### ⚠️ AVANT ACTIVATION

**Étape 1: Obtenir votre Chat ID Telegram**

1. Ouvrez Telegram
2. Recherchez `@userinfobot`
3. Envoyez `/start`
4. Copiez le `Id` affiché (ex: `123456789`)

**Étape 2: Configurer le Workflow**

1. Ouvrez le workflow dans n8n
2. Éditez le node **"Get User ChatId"**
3. Remplacez `'YOUR_CHAT_ID_HERE'` par votre vrai chatId
4. Sauvegardez le workflow

**Étape 3: Activer le Workflow**

1. Dans n8n, cliquez sur le toggle "Active"
2. Le workflow est maintenant prêt à recevoir des appels MCP

---

## 🚀 Utilisation avec Claude Code

### Configuration MCP Client (Claude Code/Desktop)

**Prérequis:** n8n MCP Server doit être configuré et actif

1. Le workflow expose automatiquement `notify_task_complete` via MCP
2. Claude Code peut appeler directement cette fonction
3. Pas besoin de configuration supplémentaire côté Claude

### Appel depuis Claude Code

Claude Code appellera automatiquement cette fonction à la fin des tâches importantes:

```bash
# Exemple: Après avoir terminé une mise à jour
[Claude Code détecte fin de tâche]
  ↓
Appel MCP: notify_task_complete(...)
  ↓
Workflow n8n s'exécute
  ↓
Notification Telegram envoyée ✅
```

---

## 📊 Emojis Automatiques

Le workflow choisit automatiquement l'emoji selon le type de tâche:

| Type de Tâche | Emoji | Détection |
|---------------|-------|-----------|
| Bug résolu | 🐛✅ | "bug" dans task_title |
| Déploiement | 🚀 | "deploy" dans task_title |
| Workflow | 🔄✅ | "workflow" dans task_title |
| Documentation | 📝✅ | "doc" dans task_title |
| Fix/Correction | 🔧✅ | "fix" dans task_title |
| Défaut | ✅ | Autres cas |

---

## 🔧 Notes de Maintenance

### Modification du ChatId

Si vous changez de compte Telegram:
1. Obtenez le nouveau chatId via `@userinfobot`
2. Éditez le node "Get User ChatId"
3. Remplacez l'ancien chatId
4. Testez avec le workflow en mode test

### Ajout d'Emojis

Pour ajouter des emojis pour d'autres types de tâches:
1. Éditez le node "Format Message"
2. Ajoutez des conditions `if (taskTitle.includes('...'))`
3. Assignez l'emoji souhaité
4. Sauvegardez

### Multi-Utilisateurs

Pour envoyer à plusieurs personnes:
1. Éditez "Get User ChatId"
2. Retournez un array de chatIds
3. Modifiez "Send Telegram Notification" pour boucler sur l'array

---

## 🐛 Troubleshooting

### Notification non reçue

**Vérifications:**
1. ✅ Workflow est actif dans n8n
2. ✅ ChatId correct dans "Get User ChatId"
3. ✅ Credential Telegram valide
4. ✅ Bot Telegram a initié conversation avec vous (`/start`)

**Solution:**
- Envoyez `/start` à votre bot Telegram
- Vérifiez les logs d'exécution dans n8n
- Testez manuellement le workflow dans n8n

### Formatage incorrect

**Problème:** Message sans formatage Markdown

**Solution:**
- Vérifiez que `parse_mode: "Markdown"` est bien défini
- Évitez les caractères spéciaux non échappés (`_`, `*`, `[`, etc.)

### Erreur MCP Connection

**Problème:** Claude Code ne peut pas appeler la fonction

**Solution:**
- Vérifiez que n8n MCP Server est actif
- Vérifiez la configuration MCP Client dans Claude
- Redémarrez n8n si nécessaire

---

## 📚 Références

- [n8n Tool Workflow](https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.toolworkflow/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Markdown](https://core.telegram.org/bots/api#markdown-style)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

## ✨ Améliorations Futures

- [ ] Support multi-canaux (Email, Slack, Discord)
- [ ] Niveaux de priorité (Info, Important, Urgent)
- [ ] Historique des notifications (stockage Notion/DB)
- [ ] Templates de messages personnalisables
- [ ] Notifications groupées (digest)

---

**Créé le:** 2025-11-01
**Maintenu par:** Claude Code
**Version:** 1.0.0
