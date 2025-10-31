# 🔌 Configuration MCP Servers pour Claude Code

Guide pour configurer les MCP servers (Context7, Sequential, etc.) avec Claude Code.

---

## 📦 Context7 - Documentation Technique

Context7 donne accès à la documentation officielle de frameworks et outils.

### Installation

```bash
# Installer Context7 globalement
npm install -g @upstash/context7-mcp

# Vérifier l'installation
npm list -g @upstash/context7-mcp
```

### Configuration pour Claude Code

#### Option 1: Configuration Globale (Recommandé)

Créer/éditer `~/.config/claude/mcp_config.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {}
    }
  }
}
```

#### Option 2: Configuration Projet (Locale)

Créer `.claude/mcp.json` dans le projet:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {}
    }
  }
}
```

### Utilisation avec Claude Code

Une fois configuré, Context7 sera automatiquement disponible:

```bash
# Claude Code utilisera automatiquement Context7 pour:
# - Documentation n8n
# - Patterns de frameworks
# - Références API
# - Exemples de code

# Example: Demander de la doc n8n
"Comment utiliser le node HTTP Request dans n8n?"
# → Claude utilisera Context7 pour accéder à docs.n8n.io
```

### Frameworks Supportés

Context7 donne accès à:
- ✅ **n8n**: Documentation complète des nodes et API
- ✅ **Node.js**: Documentation officielle
- ✅ **React/Vue/Angular**: Guides et patterns
- ✅ **Python**: Documentation standard library
- ✅ Et beaucoup d'autres...

---

## 🧠 Sequential Thinking - Raisonnement Structuré

Sequential aide Claude à raisonner sur des problèmes complexes.

### Installation

```bash
npm install -g @anthropic/mcp-server-sequential-thinking
```

### Configuration

Ajouter à `mcp_config.json`:

```json
{
  "mcpServers": {
    "context7": { ... },
    "sequential": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-sequential-thinking"],
      "env": {}
    }
  }
}
```

### Utilisation

Sequential s'active automatiquement pour:
- Debugging complexe
- Architecture system design
- Résolution de problèmes multi-étapes
- Analyse de workflows n8n

---

## 🔮 Magic - Génération UI Moderne

Magic génère des composants UI from scratch avec 21st.dev patterns.

### Installation

```bash
npm install -g @21st-dev/mcp-magic
```

### Configuration

```json
{
  "mcpServers": {
    "magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/mcp-magic"],
      "env": {}
    }
  }
}
```

### Utilisation

```bash
# Génération de composants
"Créer un dashboard moderne pour afficher les workflows n8n"
# → Magic génère le HTML/CSS/JS avec design moderne
```

---

## 🧪 Playwright - Tests Browser

Playwright permet de tester l'interface n8n dans un vrai navigateur.

### Installation

```bash
npm install -g @executeautomation/playwright-mcp-server
npx playwright install
```

### Configuration

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"],
      "env": {}
    }
  }
}
```

### Utilisation

- Tests E2E des workflows
- Vérification UI n8n
- Captures d'écran automatiques
- Validation accessibilité

---

## 📋 Configuration Complète Recommandée

Fichier `~/.config/claude/mcp_config.json` complet:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {},
      "description": "Technical documentation access"
    },
    "sequential": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-sequential-thinking"],
      "env": {},
      "description": "Complex reasoning and debugging"
    },
    "magic": {
      "command": "npx",
      "args": ["-y", "@21st-dev/mcp-magic"],
      "env": {},
      "description": "Modern UI component generation"
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"],
      "env": {},
      "description": "Browser testing and automation"
    }
  }
}
```

---

## 🚀 Installation Rapide (Tout en Une)

```bash
# Créer le répertoire de config
mkdir -p ~/.config/claude

# Installer tous les MCP servers
npm install -g @context7/mcp-server
npm install -g @anthropic/mcp-server-sequential-thinking
npm install -g @21st-dev/mcp-magic
npm install -g @executeautomation/playwright-mcp-server
npx playwright install

# Créer la configuration
cat > ~/.config/claude/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {}
    },
    "sequential": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-sequential-thinking"],
      "env": {}
    }
  }
}
EOF

echo "✅ MCP Servers configurés!"
```

---

## 🔍 Vérification

```bash
# Vérifier que les packages sont installés
npm list -g --depth=0 | grep mcp

# Tester Context7
npx @context7/mcp-server --help

# Tester Sequential
npx @anthropic/mcp-server-sequential-thinking --help
```

---

## 📖 Utilisation pour n8n Agent

### Cas d'Usage Context7

```bash
# Claude utilisera automatiquement Context7 pour:

1. "Comment configurer un webhook dans n8n?"
   → Context7 charge docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/

2. "Quel est le format JSON d'un workflow n8n?"
   → Context7 charge la référence API n8n

3. "Comment utiliser le MCP Client node?"
   → Context7 accède à la doc MCP de n8n
```

### Cas d'Usage Sequential

```bash
# Sequential s'active automatiquement pour:

1. Debugging workflow complexe (Agent Telegram)
2. Architecture multi-workflow design
3. Résolution d'erreurs MCP
4. Optimisation de performance
```

---

## 🆘 Troubleshooting

### MCP Server ne démarre pas

```bash
# Vérifier les permissions
chmod +x ~/.config/claude/mcp_config.json

# Vérifier npx
which npx
npx --version

# Réinstaller si besoin
npm install -g @context7/mcp-server --force
```

### Context7 ne trouve pas la doc

```bash
# Context7 nécessite une connexion internet
# Vérifier la connexion
curl -I https://docs.n8n.io

# Tester manuellement
npx @context7/mcp-server
```

### Claude Code ne voit pas les MCP servers

```bash
# Redémarrer Claude Code
# Vérifier le fichier de config
cat ~/.config/claude/mcp_config.json

# Vérifier les logs
tail -f ~/Library/Logs/Claude/mcp.log
```

---

## 📚 Ressources

- [Context7 Documentation](https://github.com/context7/mcp-server)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [Anthropic MCP Servers](https://github.com/anthropics/mcp-servers)
- [n8n Documentation](https://docs.n8n.io/)

---

**Créé le**: 2025-10-31
**Maintenu par**: Claude Code + Nicolas Marillot
