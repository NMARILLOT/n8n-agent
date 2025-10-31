# Agent Telegram - Capture d'Idées de Développement

## 🎯 Objectif

Capturer rapidement des idées de projets et fonctionnalités via Telegram (texte ou vocal) et les organiser automatiquement dans Notion grâce à un agent IA intelligent.

## 📋 Description

Ce système permet de transformer Telegram en un assistant de capture d'idées connecté à Notion. L'utilisateur peut envoyer une idée par message texte ou vocal, et l'agent IA (Claude Sonnet 4.5) analyse automatiquement l'idée, cherche si un projet similaire existe déjà, et crée soit un nouveau projet, soit ajoute l'idée à un projet existant dans Notion.

Le système utilise le protocole MCP (Model Context Protocol) pour exposer les opérations Notion comme des outils que l'agent IA peut utiliser de manière autonome.

## 🔧 Workflows inclus

### Workflow 1: Agent Telegram - Dev Ideas
- **Fichier**: `workflow/Agent Telegram - Dev Ideas.json`
- **Fonction**: Bot Telegram principal avec agent IA pour capturer et organiser les idées
- **Déclencheur**: Webhook Telegram (messages texte ou vocaux)
- **Dépendances**:
  - Workflow MCP "MCP - Idée Dev Nico (Perso)"
  - OpenAI Whisper (transcription)
  - Claude Sonnet 4.5 (agent IA)
  - Telegram Bot API

**Architecture du workflow**:
```
Telegram → Switch (text/vocal) → [vocal: Download + Transcribe] → Merge → Agent IA → Format → Telegram
                                  [text: Format] ──────────────┘
```

### Workflow 2: MCP - Idée Dev Nico (Perso)
- **Fichier**: `workflow/MCP - Idée Dev Nico (Perso) (1).json`
- **Fonction**: Serveur MCP exposant des outils de gestion de projets Notion
- **Déclencheur**: MCP Server Trigger (SSE sur `https://auto.mhms.fr/mcp/projects-mhms/sse`)
- **Dépendances**:
  - Notion API (2 databases)
  - Execute Workflow Trigger (auto-appel)

**Outils MCP exposés**:

*Gestion des projets:*
- `search_projects(query)` - Recherche de projets par mots-clés
- `get_project_by_id(id)` - Récupération des détails d'un projet
- `list_categories()` - Liste des catégories disponibles
- `create_project(...)` - Création d'un nouveau projet
- `create_idea(project_id, title, content, category)` - Ajout d'une idée à un projet

*Gestion des idées (nouveau 🆕):*
- `search_ideas(query)` - 🔍 Recherche d'idées par mot-clé dans titre ou contenu
- `get_idea_by_id(id)` - 📖 Récupération des détails d'une idée spécifique
- `update_idea(idea_id, title?, content?, category?)` - ✏️ Modification d'une idée existante
- `delete_idea(idea_id)` - 🗑️ Suppression définitive d'une idée (irréversible)

## 🔗 Intégrations

### Services externes
- **Telegram**: Bot de capture (@votre_bot_name)
- **Notion**:
  - Database "Projets" (ID: `29b2c1373ccc8042a8e2e096b12ca4e4`)
  - Database "Idées" (ID: `29b2c1373ccc807d9347ce519cabcac4`)
- **OpenAI**: API Whisper pour transcription audio (langue: FR)
- **Anthropic**: Claude Sonnet 4.5 pour l'agent IA

### MCP Server
- **Endpoint SSE**: `https://auto.mhms.fr/mcp/projects-mhms/sse`
- **Authentification**: Bearer Token

## 🔑 Credentials nécessaires

1. **Telegram Bot API** (`telegramApi`)
   - ID: `tecnNETDK9d3pNmM`
   - Nom: "Telegram Nico Dev (perso)"

2. **Notion API** (`notionApi`)
   - ID: `cT2CMYYw9BByHYSg`
   - Nom: "Notion account - nicolas@mhms.fr"

3. **OpenAI API** (`openAiApi`)
   - ID: `6foKVjLxDL95kCfm`
   - Nom: "OpenAi account - Nicolas MARILLOT"

4. **Anthropic API** (`anthropicApi`)
   - ID: `DHjhBnBvG95IQssg`
   - Nom: "Anthropic account"

5. **Bearer Auth MCP** (`httpBearerAuth`)
   - ID: `aCtUA2HFdnNADDGH`
   - Nom: "Notion MCPAuth"

## 📊 Architecture

```
┌─────────────┐
│  Telegram   │
│   (User)    │
└──────┬──────┘
       │ Message (text/vocal)
       ▼
┌──────────────────────────────────────┐
│  Workflow: Agent Telegram Dev Ideas  │
│                                      │
│  ┌─────────┐    ┌──────────────┐   │
│  │ Switch  │───▶│ Transcribe   │   │
│  │ Type    │    │ (si vocal)   │   │
│  └────┬────┘    └──────┬───────┘   │
│       │                 │           │
│       └────────┬────────┘           │
│                ▼                    │
│      ┌──────────────────┐          │
│      │  Agent IA        │          │
│      │  (Claude 4.5)    │          │
│      │  + Memory        │          │
│      └────────┬─────────┘          │
│               │ Appels MCP         │
└───────────────┼────────────────────┘
                │
                ▼
┌───────────────────────────────────────┐
│  Workflow: MCP Server                 │
│                                       │
│  ┌──────────────┐   ┌──────────────┐ │
│  │ MCP Trigger  │───│    Switch    │ │
│  │    (SSE)     │   │  Operation   │ │
│  └──────────────┘   └──────┬───────┘ │
│                             │         │
│    ┌────────────────────────┼─────┐  │
│    │   search_projects      │     │  │
│    │   get_project_by_id    │     │  │
│    │   list_categories      │     │  │
│    │   create_project       │     │  │
│    │   create_idea          │     │  │
│    │   search_ideas     🆕  │     │  │
│    │   get_idea_by_id   🆕  │     │  │
│    │   update_idea      🆕  │     │  │
│    │   delete_idea      🆕  │     │  │
│    └────────────────────────┼─────┘  │
│                             ▼         │
│                      ┌──────────────┐ │
│                      │    Notion    │ │
│                      │   Database   │ │
│                      └──────────────┘ │
└───────────────────────────────────────┘
```

## 💡 Cas d'usage

### Exemple 1: Nouvelle idée de projet (texte)
```
User: "App mobile de suivi d'habitudes quotidiennes"

Agent:
1. Appelle search_projects("habitudes tracking")
2. Aucun résultat trouvé
3. Appelle create_project(
     name="Habit Tracker App",
     category="UX/UI",
     type="App",
     description="Application mobile pour suivre les habitudes...",
     priority="Moyenne",
     status="💡 Idée",
     tech_stack="React Native, Expo, SQLite"
   )
4. Répond: "✅ Projet créé ! ID: PROJ-ABC123..."
```

### Exemple 2: Ajout à projet existant (vocal)
```
User: 🎤 "Ajouter un dark mode à mon blog"

Agent:
1. Transcrit: "Ajouter un dark mode à mon blog"
2. Appelle search_projects("blog")
3. Trouve [PROJ-BLOG-456] Personal Tech Blog
4. Appelle create_idea(
     project_id="PROJ-BLOG-456",
     title="Dark mode",
     content="Toggle dark/light mode avec sauvegarde...",
     category="Amélioration"
   )
5. Répond: "✅ Idée ajoutée ! ID: IDEA-XYZ789..."
```

### Exemple 3: Recherche d'idées existantes 🆕
```
User: "Montre-moi toutes mes idées sur le dark mode"

Agent:
1. Appelle search_ideas("dark mode")
2. Trouve 2 résultats:
   - [IDEA-456] Dark mode pour Personal Tech Blog
   - [IDEA-789] Dark mode préférences utilisateur
3. Répond: "J'ai trouvé 2 idées sur le dark mode:\n1. Dark mode pour blog (IDEA-456)\n2. Dark mode préférences utilisateur (IDEA-789)"
```

### Exemple 4: Modification d'une idée 🆕
```
User: "Change le titre de IDEA-456 en 'Thème sombre complet'"

Agent:
1. Appelle get_idea_by_id("IDEA-456")
2. Vérifie que l'idée existe
3. Appelle update_idea(
     idea_id="IDEA-456",
     title="Thème sombre complet"
   )
4. Répond: "✅ Idée modifiée ! IDEA-456 : Thème sombre complet"
```

### Exemple 5: Suppression d'une idée 🆕
```
User: "Supprime l'idée IDEA-789, elle n'est plus pertinente"

Agent:
1. Appelle get_idea_by_id("IDEA-789")
2. Vérifie que l'idée existe
3. Appelle delete_idea("IDEA-789")
4. Répond: "✅ Idée supprimée\n\n⚠️ IDEA-789 a été supprimée définitivement"
```

## 🛠️ Maintenance

### Comportement de l'agent

Le prompt de l'agent est configuré pour:
- **Toujours rechercher** avant de créer un nouveau projet
- **Ne jamais demander confirmation** à l'utilisateur
- **Agir de manière autonome** et directe
- **Être concis** dans les réponses

### Mémoire conversationnelle
- **Type**: Buffer Window Memory
- **Capacité**: 60 messages
- **Session Key**: `MEMORY_DEV`

### Formatage Markdown
Le workflow convertit automatiquement le markdown de Claude vers la syntaxe Telegram:
- `**gras**` → `*gras*`
- `__italique__` → `_italique_`
- `~~barré~~` → `~barré~`

### Évolutions possibles
- [ ] Ajouter support des images/photos
- [x] ✅ **Permettre la modification et suppression d'idées** (Déployé le 2025-10-31)
- [ ] Ajouter la modification/suppression de projets
- [ ] Ajouter des commandes Telegram (/list, /search, etc.)
- [ ] Statistiques d'utilisation
- [ ] Multi-utilisateurs avec permissions
- [ ] Export de projets en différents formats
