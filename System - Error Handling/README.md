# 🚨 System - Error Handling

**Objectif**: Workflow centralisé de gestion des erreurs pour tous les workflows n8n avec logging complet et notifications intelligentes.

## 📋 Description

Système de monitoring et logging d'erreurs qui capture automatiquement toutes les erreurs des workflows configurés, les analyse, les enregistre dans Google Sheets, et envoie des notifications Telegram pour les erreurs critiques.

## 🔄 Workflows inclus

### 1. **Global Error Handler**
- **Fichier**: `workflow/Global Error Handler.json`
- **Type**: Error Workflow
- **Trigger**: Error Trigger (automatique sur erreurs)
- **Fonction**: Capture, analyse, log et notifie toutes les erreurs

## 🏗️ Architecture

```
Error Trigger (automatique)
    ↓
Analyze Error Context
    ↓
┌─────────────────────┬─────────────────────┬─────────────────────┐
│                     │                     │                     │
Classify Error    Extract Stack    Calculate Severity
    ↓                 Trace              ↓
Format Log Entry      ↓           Check if Critical
    ↓                 │                   ↓
┌───────────────┐     │          ┌────────────────┐
│               │     │          │                │
Log to Sheets ──┴─────┴──────────┴→ Send Telegram Alert
                                          (if critical)
```

## 📊 Logs Capturés

### Informations d'Erreur
- **Timestamp**: Date et heure précise
- **Workflow ID & Name**: Identification du workflow source
- **Execution ID**: ID d'exécution unique
- **Node Name**: Nom du node en erreur
- **Error Type**: Type d'erreur (API, Timeout, Validation, etc.)
- **Error Message**: Message d'erreur complet
- **Stack Trace**: Trace d'exécution (si disponible)
- **Input Data**: Données d'entrée du node
- **Severity**: Critique, Important, Mineur

### Métriques
- **Execution Duration**: Temps avant échec
- **Retry Count**: Nombre de tentatives
- **Error Frequency**: Compteur d'occurrences similaires
- **User Impact**: Utilisateur affecté (si applicable)

## 🔌 Intégrations

### Google Sheets
- **Feuille**: "n8n Error Logs"
- **Colonnes**: Timestamp, Workflow, Node, Error Type, Message, Severity, Stack Trace, Input, Execution ID
- **Retention**: Tous les logs conservés (archivage manuel)

### Telegram
- **Bot**: Notifications immédiates
- **Critères**: Erreurs critiques seulement
- **Format**: Résumé structuré avec lien vers n8n

## 🎯 Classification des Erreurs

### 🔴 Critique (Notification immédiate)
- Échec authentification API principale
- Erreur base de données
- Workflow business-critical échoue
- Erreur de sécurité
- Data loss potentiel

### 🟡 Important (Log uniquement)
- Timeout API externe
- Rate limit atteint
- Validation de données échouée
- Node optionnel échoue

### 🟢 Mineur (Log uniquement)
- Retry réussi après échec
- Warning non-bloquant
- Fallback activé avec succès

## 🔧 Configuration

### Prérequis
1. **Google Sheets Credential**: Accès au spreadsheet de logs
2. **Telegram Credential**: Bot pour notifications
3. **Spreadsheet ID**: ID du Google Sheet

### Activation
Pour chaque workflow à monitorer:
1. Ouvrir Settings du workflow
2. Sélectionner "Error Workflow"
3. Choisir "Global Error Handler"
4. Sauvegarder

### Variables d'Environnement
```javascript
CRITICAL_WORKFLOWS = [
  "Agent Telegram - Dev Ideas",
  "MCP - Idée Dev Nico (Perso)",
  "Production API"
]

NOTIFICATION_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"
ERROR_LOG_SHEET_ID = "YOUR_GOOGLE_SHEET_ID"
```

## 📈 Dashboard & Analytics

Le Google Sheet inclut des graphiques automatiques:
- **Erreurs par jour**: Tendance temporelle
- **Top 5 workflows avec erreurs**: Identification problèmes récurrents
- **Distribution par type**: API, Timeout, Validation, etc.
- **Taux de criticité**: % erreurs critiques vs. mineures

## 💡 Cas d'Usage

### Exemple 1: API Timeout
```
Workflow: Agent Telegram - Dev Ideas
Node: Download Audio
Error: Request timeout (30s)
Severity: 🟡 Important
Action: Log dans Sheets, pas de notification
```

### Exemple 2: Erreur Critique
```
Workflow: MCP - Idée Dev Nico (Perso)
Node: Create Idea in Notion
Error: 401 Unauthorized - Invalid API key
Severity: 🔴 Critique
Action: Log + Notification Telegram immédiate
```

### Exemple 3: Validation Error
```
Workflow: Agent Telegram - Dev Ideas
Node: Format Text Input
Error: Missing required field 'userMessage'
Severity: 🟢 Mineur
Action: Log uniquement (continue on fail activé)
```

## 🔄 Maintenance

### Nettoyage des Logs
- **Fréquence**: Mensuelle
- **Méthode**: Archiver logs >90 jours dans onglet séparé
- **Script**: `scripts/archive-old-error-logs.js` (à créer si besoin)

### Monitoring
- **Review hebdomadaire**: Analyser patterns d'erreurs
- **Action**: Corriger erreurs récurrentes
- **Optimization**: Ajuster classification si besoin

## 🎓 Bonnes Pratiques

1. **Ne pas désactiver Continue on Fail** pour capturer toutes erreurs
2. **Tester le workflow d'erreur** avec erreur volontaire
3. **Vérifier Sheets régulièrement** pour détecter patterns
4. **Ajuster seuil de criticité** selon vos besoins
5. **Documenter résolutions** dans colonne "Resolution Notes"

## 📚 Références

- [n8n Error Handling Docs](https://docs.n8n.io/workflows/error-handling/)
- [n8n Error Trigger](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.errortrigger/)
- [Best Practices Error Workflows](https://community.n8n.io/t/error-workflow-best-practices/)

---

**Créé**: 2025-11-01
**Maintenu par**: Claude Code + Nicolas Marillot
**Instance**: https://auto.mhms.fr/
