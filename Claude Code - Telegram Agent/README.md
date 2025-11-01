# Claude Code - Telegram Agent

Agent Telegram intelligent avec architecture triple-trigger pour interaction conversationnelle et notifications Claude Code.

## 📋 Vue d'ensemble

Workflow n8n unifié combinant:
- 🤖 **Agent IA conversationnel** avec mémoire persistante MongoDB
- 📱 **Bot Telegram** pour interactions texte et vocal
- 🔔 **Notifications Claude Code** via webhook
- ✅ **Mode nomade** avec boutons approve/deny

## 🏗️ Architecture

### Triple-Trigger System

```
┌─────────────────────────────────────────────────────────────┐
│                    ENTRY POINTS (Triggers)                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Telegram Trigger → Messages utilisateur (texte/vocal)  │
│  2. Webhook Trigger  → Notifications Claude Code           │
│  3. MCP Server       → (Future) Claude Code direct access   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
                     ┌────────────────┐
                     │  Input Router  │
                     │    (Switch)    │
                     └────────────────┘
                              ↓
           ┌──────────────────┴──────────────────┐
           ↓                                     ↓
    ┌─────────────┐                    ┌─────────────────┐
    │ Notification│                    │ Telegram Message│
    │  Handler    │                    │  Type Switch    │
    └─────────────┘                    └─────────────────┘
           ↓                                     ↓
    Format → Send                     ┌──────────┴──────────┐
    → Webhook Response                ↓                     ↓
                                  ┌──────┐            ┌──────┐
                                  │Vocal │            │ Text │
                                  └──────┘            └──────┘
                                     ↓                     ↓
                              Get Audio → Download    Format Input
                              → Whisper → Format           ↓
                                     ↓                     ↓
                                  ┌──────────────────────┐
                                  │     AI Agent         │
                                  │  + GPT-4o + Memory   │
                                  │  + MCP Client Tools  │
                                  └──────────────────────┘
                                            ↓
                                  Send Telegram Response
```

## 🎯 Fonctionnalités

### 1. Conversation avec Agent IA

- **Texte**: Envoyez des messages texte au bot
- **Vocal**: Envoyez des messages vocaux (transcription automatique via Whisper)
- **Mémoire**: Conversation persistante via MongoDB (60 derniers messages)
- **Outils Notion**: Accès aux 9 outils de gestion d'idées et projets

### 2. Notifications Claude Code

Webhook POST: `https://auto.mhms.fr/webhook/claude-code-notification`

**Payload**:
```json
{
  "notification": true,
  "task_title": "Titre de la tâche",
  "summary": "Résumé court",
  "context": "Contexte détaillé",
  "requires_approval": false
}
```

**Réponse**:
- Message Telegram formaté
- Boutons inline approve/deny si `requires_approval=true`

### 3. Mode Nomade

Quand vous activez le mode nomade dans Claude Code:
- Vous recevez des notifications de fin de tâche
- Vous pouvez approuver/refuser via boutons Telegram
- Vous pouvez discuter avec Claude Code via le bot

## 🔧 Configuration

### Credentials Utilisées

| Credential | ID | Usage |
|------------|-----|-------|
| Telegram Claude Code | `GyCvAZHBuXIAzVAC` | Bot Telegram |
| OpenAI | (à configurer) | GPT-4o + Whisper |
| MCP Auth | (à configurer) | MCP Client Notion |

### Triggers

| Trigger | Type | Webhook ID | URL |
|---------|------|------------|-----|
| Telegram | Message updates | `claude-code-agent` | Auto (Telegram) |
| Webhook | POST | `claude-code-webhook` | `/webhook/claude-code-notification` |

### Agent Configuration

- **Model**: GPT-4o (OpenAI)
- **Temperature**: 0.3 (précis mais créatif)
- **Memory**: MongoDB Chat Memory (60 messages)
- **Tools**: MCP Client → 9 outils Notion
- **System Prompt**: 277 lignes avec règles strictes d'appel d'outils

## 📱 Bot Telegram

- **Username**: `@claude_code_nico_bot`
- **Token**: `8271481273:AAGbWO6JFwyQo7S10nyszmWt5R1fhaCWeG0`
- **Target User**: `0684789511` (pour notifications)

## 🛠️ Outils Disponibles (via MCP)

**Projets**:
- `search_projects(query)` - Chercher des projets
- `get_project_by_id(id)` - Récupérer un projet
- `list_categories()` - Lister les catégories
- `create_project(...)` - Créer un projet

**Idées**:
- `create_idea(...)` - Créer une idée
- `search_ideas(query)` - Chercher des idées
- `get_idea_by_id(id)` - Récupérer une idée
- `update_idea(...)` - Modifier une idée
- `delete_idea(idea_id)` - Archiver une idée

## 🔄 Workflow Vocal

```
Message vocal Telegram
  ↓
Get Audio File (Telegram API)
  ↓
Download Audio (HTTP Request)
  ↓
Whisper Transcription (OpenAI)
  ↓
Format Input (texte extrait)
  ↓
AI Agent
```

## 📊 System Prompt

Le system prompt (277 lignes) contient:
- 🚨 Règles critiques d'appel d'outils
- 📝 Workflow obligatoire: Réception → Validation → Appel outil → Résultat → Confirmation
- 🚫 Interdictions absolues (ne JAMAIS confirmer sans appeler l'outil)
- 💬 Format des réponses (conversation vs action)
- 📚 Exemples complets (bon et mauvais usage)
- 📌 Mode nomade (gestion des notifications)

## 🧪 Tests

### Test 1: Message texte
```
Envoyer à @claude_code_nico_bot: "Crée une idée: Test workflow"
```

Résultat attendu:
- Agent appelle `create_idea()`
- Reçoit confirmation de Notion
- Répond avec ID et lien Notion

### Test 2: Message vocal
```
Envoyer un message vocal: "Cherche les projets en cours"
```

Résultat attendu:
- Transcription Whisper
- Agent appelle `search_projects()`
- Répond avec liste des projets

### Test 3: Notification
```bash
curl -X POST https://auto.mhms.fr/webhook/claude-code-notification \
  -H "Content-Type: application/json" \
  -d '{
    "notification": true,
    "task_title": "Workflow créé",
    "summary": "Triple-trigger architecture implémentée",
    "context": "Telegram + Webhook + MCP",
    "requires_approval": true
  }'
```

Résultat attendu:
- Message Telegram avec détails
- Boutons ✅ Approve / ❌ Deny

## 📈 Évolutions Futures

- [ ] MCP Server Trigger pour accès direct Claude Code
- [ ] Gestion des callbacks (approve/deny) via Telegram updates
- [ ] Statistiques d'utilisation (nombre d'idées créées, etc.)
- [ ] Support multi-utilisateurs avec gestion de permissions
- [ ] Integration avec autres outils (GitHub, Linear, etc.)

## 🐛 Troubleshooting

### Workflow ne répond pas
- Vérifier que workflow est actif
- Vérifier credentials Telegram
- Checker logs d'exécution

### Transcription vocale échoue
- Vérifier credential OpenAI
- Vérifier format audio supporté par Whisper
- Checker timeout settings

### Outils Notion ne fonctionnent pas
- Vérifier MCP Server accessible
- Vérifier credential MCP Auth
- Tester outils indépendamment

### Notifications ne s'envoient pas
- Vérifier webhook URL accessible
- Vérifier format payload JSON
- Vérifier chat_id destinataire

## 📚 Documentation

- **CLAUDE.md**: Guide complet n8n pour Claude Code
- **claudedocs/n8n_comprehensive_documentation_2025.md**: Knowledge base technique complète
- **WORKFLOW_GUIDELINES.md**: Standards de layout visuel

## 🔗 Liens

- n8n Instance: https://auto.mhms.fr/
- Bot Telegram: https://t.me/claude_code_nico_bot
- MCP Server: (URL du serveur MCP Notion)

---

**Créé par**: Claude Code (claude.ai/code)
**Framework**: SuperClaude
**Date**: 2025-01-01
