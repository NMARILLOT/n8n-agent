# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 🧠 Règles Personnelles de Workflow - Nicolas (TDAH-Optimized)

**IMPORTANT**: Ces règles s'appliquent à TOUS mes projets et définissent ma méthode de travail préférée.

### 1. Commande : "PLAN"
**Rôle**: Coach / Architecte
**Comportement**:
- Résumer en **1 phrase claire** l'objectif
- Créer une **TODO LIST numérotée** (3 à 6 points maximum)
- Lister les **fichiers à modifier**
- **STOPPER LÀ** - Ne code RIEN, n'exécute RIEN

**Exemple**:
```
Objectif : Ajouter un système d'authentification JWT au bot Telegram

TODO:
1. Créer le middleware d'authentification (auth.middleware.ts)
2. Ajouter la validation JWT dans le workflow Telegram
3. Mettre à jour le README avec les nouvelles variables d'environnement

Fichiers à toucher:
- Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json
- scripts/add-auth-middleware.py (nouveau)
- Agent Telegram - Dev Nico Perso/README.md
```

### 2. Commande : "CODE"
**Rôle**: Développeur concentré
**Comportement**: Faire **uniquement l'étape demandée** (ex: "Code étape 2")
- Donner les **diffs git exacts** (avant/après)
- Expliquer **brièvement** ce que fait chaque modification
- Ajouter **1 mini test** pour vérifier (commande CLI, test manuel, ou validation)
- **S'ARRÊTER** - Pas d'amélioration spontanée, pas d'optimisation non demandée

**Exemple**:
```
Code étape 2 : Validation JWT dans workflow Telegram

Modifications:
- Agent Telegram - Dev Nico Perso/workflow/Agent Telegram - Dev Ideas.json
  → Ajout du node "Verify JWT Token" entre Telegram Trigger et Agent
  → Configuration de la validation avec variable d'environnement JWT_SECRET

Test de validation:
./scripts/deploy.sh --dry-run --dir "Agent Telegram - Dev Nico Perso"
```

### 3. Commande : "CHECK"
**Rôle**: QA / Coach positif
**Comportement**: Vérifier l'étape complétée
- **Comparer** le résultat à l'objectif initial du PLAN
- Si ✅ **c'est bon** → le dire simplement
- Si ❌ **bug détecté** → donner le **patch minimal** uniquement
- **Pas de blabla**, pas de refactor global, pas de suggestions non demandées

**Exemple**:
```
CHECK étape 2 :

✅ Node "Verify JWT Token" correctement ajouté
✅ Connexions mises à jour (Telegram → JWT → Agent)
✅ Variable JWT_SECRET référencée dans les paramètres

Étape 2 validée. Prêt pour étape 3.
```

### ⚙️ Conventions Techniques Générales
Ces conventions s'appliquent à mes projets web (pas spécifique à n8n) :
- **Stack web**: NestJS + React + Tailwind + shadcn/ui + Postgres/PostGIS
- **Typage strict**: TypeScript obligatoire
- **Forms**: react-hook-form + zod
- **Règles strictes**:
  - ❌ Jamais de nouvelle dépendance sans validation explicite
  - ❌ Jamais de refactor hors ticket
  - ❌ Jamais de modification DB sans demande explicite

---

# n8n Agent - Expert Workflow Automation Repository

Expert n8n developer specialized in creating, modifying, and improving automation workflows with deep technical knowledge and full SuperClaude Framework autonomy.

**Instance n8n**: `https://auto.mhms.fr/`
**Complete Documentation**: `claudedocs/n8n_comprehensive_documentation_2025.md`

---

## 📖 Table of Contents

0. **[Règles Personnelles de Workflow (PLAN/CODE/CHECK)](#-règles-personnelles-de-workflow---nicolas-tdah-optimized)** ⭐
1. [Quick Start](#-quick-start)
2. [Essential Commands](#-essential-commands)
3. [Critical Architecture Patterns](#-critical-architecture-patterns)
4. [n8n Technical Knowledge](#-n8n-technical-knowledge)
5. [Visual Layout Guidelines](#-visual-layout-guidelines)
6. [Development Workflows](#-development-workflows)
7. [Bug Tracking](#-bug-tracking)
8. [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### First Time Setup

```bash
# 1. Environment configuration (copy template and add your API key)
cp .env.example .env
nano .env  # Edit and add N8N_API_KEY from https://auto.mhms.fr/settings/api
# See .env.example for all available configuration options

# 2. MCP servers (Context7 for documentation)
./scripts/setup-mcp.sh

# 3. Verify connection
./scripts/list.sh

# 4. Test deployment (dry-run = no changes)
./scripts/deploy.sh --dry-run
```

### Common Development Cycle

```bash
# 1. Fetch current layout (understand user preferences)
python3 scripts/fetch-current-layout.py

# 2. Make changes to workflow JSON files

# 3. Deploy with auto-commit (Git commits happen BEFORE deployment)
./scripts/deploy.sh --dir "System Name"

# 4. Push to GitHub
git push origin main
```

### Debug Mode

```bash
# Enable detailed logs for troubleshooting
DEBUG=1 ./scripts/deploy.sh --dir "System Name"
```

---

## 🚀 Essential Commands

### Deployment & Management

```bash
# List all workflows from n8n instance
./scripts/list.sh

# Deploy workflows (with dry-run first)
./scripts/deploy.sh --dry-run              # Test without changes
./scripts/deploy.sh                        # Deploy all workflows
./scripts/deploy.sh --dir "System Name"    # Deploy specific system

# Debug mode - detailed logs
DEBUG=1 ./scripts/deploy.sh
```

### MCP Servers (Context7)

**Automatically configured** - provides real-time access to:
- n8n documentation (docs.n8n.io)
- Node.js documentation
- Framework patterns and examples

**Usage**: Context7 auto-activates when you ask about n8n nodes, API, or technical documentation.

**Configuration**: `~/.config/claude/mcp_config.json` (created by setup-mcp.sh)

---

## 🏗️ Critical Architecture Patterns

### 1. Git Versioning System (Automated)

**IMPORTANT**: Every deployment automatically commits to Git BEFORE deploying.

**Flow**:
```bash
./scripts/deploy.sh --dir "System Name"

# Internally executes:
# 1. Git add all changes
# 2. Git commit with deployment metadata
# 3. Deploy to n8n
# 4. Prompt to push to GitHub

# Output:
# 📦 Git Versioning...
# ✅ Committed changes: a1b3cbc
# 💡 Push to GitHub: git push origin main
# 🚀 Starting deployment...
```

**Benefits**:
- Every deployment is versioned
- Easy rollback if needed
- Complete audit trail
- Timestamp tracking

**Script**: `scripts/deploy.sh` (lines 89-133)

### 2. API Data Cleaning Pipeline

**Critical Function**: `cleanWorkflowForAPI()` in `scripts/deploy.js`

**Problem**: n8n API rejects certain fields that exist in exported workflows.

**Fields Excluded**:
- `id`, `createdAt`, `updatedAt`, `versionId` - API manages these
- `settings.executionOrder` - Not supported by API
- `settings.callerPolicy` - Not supported by API

**Fields Preserved**:
- `pinData` - Test data locked to nodes
- `staticData` - Persistent node-specific data

**Update Logic**:
```javascript
// For updates (PUT): Fetch remote workflow first
// Merge remote settings + local settings
// Exclude unsupported fields
// Send cleaned payload to API

// For creates (POST): Clean local workflow
// Send only API-accepted fields
```

**Why This Matters**: Deployment fails if unsupported fields are sent.

**Script**: `scripts/deploy.js` (lines 169-206, 235-291)

### 3. Workflow Matching by Name

**CRITICAL**: Workflows are matched by **exact name** (case-sensitive).

**Matching Logic**:
```javascript
// Remote workflow lookup
const existingWorkflow = remoteWorkflows.find(w => w.name === workflowName);

// If found → UPDATE (PUT /api/v1/workflows/:id)
// If not found → CREATE (POST /api/v1/workflows)
```

**Implication**: Renaming a workflow locally creates a NEW workflow remotely (doesn't update).

**Script**: `scripts/deploy.js` (line 219)

### 4. Project Structure Convention

**Required Structure**:
```
System Name/
├── README.md          # REQUIRED - System documentation
└── workflow/          # REQUIRED - Workflow files directory
    ├── workflow1.json
    └── workflow2.json
```

**Scanning Logic**: `scripts/deploy.js` looks for directories named `workflow/` (line 130)

**Why**: Separates workflows from other files (scripts, docs, etc.)

### 5. Environment Variable Precedence

**Order of Loading**:
1. `.env` file (primary source)
2. Command-line exports (override .env)
3. Script defaults (fallback)

**Required Variables**:
- `N8N_API_KEY` - REQUIRED for all operations
- `N8N_HOST` - Defaults to `https://auto.mhms.fr`
- `DRY_RUN` - Set via `--dry-run` flag

**Script**: `scripts/deploy.sh` (lines 19-42)

---

## 🧠 n8n Technical Knowledge

### Code Node - JavaScript Capabilities

#### Built-in Variables & Methods

**Core Variables**:
```javascript
// Input access patterns
$input.all()      // Get all items at once (Run Once for All Items)
$input.first()    // Get first item
$input.last()     // Get last item

$json            // Current item's JSON data (For Each Item mode)
$json.field      // Direct property access
$json['nested']['field']  // Nested access

// Access other nodes
$node['Node Name'].json.data
$node['HTTP Request'].json.body.results

// Execution & Workflow metadata
$execution.id           // Current execution ID
$execution.mode         // manual, trigger, etc.
$workflow.id           // Workflow ID
$workflow.name         // Workflow name
$workflow.active       // Is active?
```

**Syntax Pattern**: Type `_` (underscore) in Code node for autocomplete

#### Execution Modes

**Run Once for All Items**:
```javascript
const items = $input.all();
return items.map(item => ({
  json: {
    ...item.json,
    processed: true
  }
}));
```

**Run Once for Each Item**:
```javascript
return {
  city: $json.city,
  processed: true
};
```

#### Limitations

❌ **Cannot** access file system
❌ **Cannot** make HTTP requests (use HTTP Request node)
✅ **Can** transform data with JavaScript
✅ **Can** use Luxon library (built-in)
✅ **Can** access built-in n8n methods

### Expression System

#### Syntax

**Pattern**: `{{ JavaScript expression }}`

**Examples**:
```javascript
{{ $json.city }}                           // Property access
{{ $json['body']['city'] }}                // Nested access
{{ $node['Get Order'].json.data }}         // Other node data
{{ $execution.id }}                        // Execution ID
{{ $workflow.name }}                       // Workflow name
```

⚠️ **Important**: Use `$node['Name']` syntax, NOT deprecated `$('Name')`

#### Common Patterns

```javascript
// Date/time with Luxon
{{ $now.toISO() }}
{{ $now.plus({days: 7}).format('yyyy-MM-dd') }}

// String operations
{{ $json.email.toLowerCase() }}
{{ $json.name.split(' ')[0] }}

// Array operations
{{ $json.items.length }}
{{ $json.items.map(i => i.name) }}

// Conditional
{{ $json.status === 'active' ? 'yes' : 'no' }}
```

### HTTP Request Node - Authentication

#### Supported Methods

| Method | Configuration | Best For |
|--------|--------------|----------|
| **Bearer Token** | `Authorization: Bearer <token>` | Modern REST APIs, OAuth 2.0 |
| **OAuth 2.0** | Client ID/Secret, auto-refresh | Google, Microsoft, Salesforce |
| **OAuth 1.0** | Consumer Key/Secret | Twitter API, legacy APIs |
| **Header Auth** | Custom header (X-API-Key) | Simple APIs, webhooks |
| **Basic Auth** | Username/Password (Base64) | Legacy systems |
| **Query Auth** | API key in URL params | Simple auth schemes |
| **Custom Auth** | Flexible multi-param | Non-standard schemes |

#### OAuth 2.0 Configuration

**n8n Advantages**:
- Automatic token refresh
- Secure credential storage
- User-friendly OAuth flow

**Grant Types**: Authorization Code, Client Credentials, Resource Owner Password, Refresh Token

### AI Agents & LangChain Integration

#### Agent Types

| Agent | Memory | Use Case |
|-------|--------|----------|
| **Conversational** | ✅ Yes | Chatbots, customer support, ongoing dialogue |
| **Tools Agent** | ✅ Yes | Multi-tool orchestration, API automation |
| **ReAct** | ❌ No | Single-shot reasoning, fact-checking |
| **OpenAI Functions** | ✅ Yes | OpenAI-specific function calling |
| **Plan & Execute** | ✅ Yes | Complex multi-step tasks |
| **SQL Agent** | ✅ Yes | Natural language to SQL |

#### Agent Workflow Patterns

**Pattern 1: Conversational Bot**:
```
Chat Trigger → Conversational Agent + Simple Memory → Respond to Chat
```

**Pattern 2: Tools-Augmented Agent**:
```
Manual Trigger → Tools Agent → [Wikipedia + Calculator + Custom Code] → Output
```

**Pattern 3: RAG-Powered Agent**:
```
Webhook → ReAct Agent → Vector Store Retriever → LLM → Response
```

### MCP (Model Context Protocol) Integration

#### MCP Client Tool Node

**Purpose**: Connect AI agents to external MCP servers

**Configuration**:
1. **SSE Endpoint**: `https://mcp-server.example.com/sse`
2. **Authentication**: Bearer Token or Header Auth
3. **Tool Selection**: All or Selected

**Architecture**:
```
AI Agent → MCP Client Tool → External MCP Server → [Tools/Resources]
```

#### MCP Server Trigger Node

**Purpose**: Expose n8n workflows as MCP tools to external clients

**Architecture**:
```
External MCP Client (Claude Code/Desktop) → n8n MCP Server → n8n Workflow
```

**Use Cases**:
- Expose n8n automation to AI assistants
- Let Claude Code/Cursor call your workflows
- Create custom AI tools backed by n8n

#### Tool Workflows (Call n8n Workflow Tool)

**Purpose**: Create reusable workflows that AI agents can call as tools

**Best Practices**:
1. Clear descriptions for LLM decision-making
2. Single responsibility per tool
3. Input validation
4. Meaningful error messages
5. Modular design

### Error Handling Patterns

#### 1. Error Trigger Node

**Setup**:
1. Create error workflow starting with Error Trigger
2. In main workflow: Settings → Error Workflow → Select error workflow
3. Runs automatically on execution failure

**Best Practice**: One centralized error workflow per n8n instance

#### 2. Continue on Fail

**Per-node setting**:
- ✅ **Continue**: Skip failed node, continue workflow
- ❌ **Stop**: Halt workflow on error (default)

**When enabled**: Exposes error output (red connector) for routing failures

#### 3. Retry on Fail

**Configuration**:
- Max Retry Attempts: 1-5 (typically 3)
- Retry Interval: Time between retries
- Exponential backoff (recommended)

**Best for**: Network requests, external APIs, temporary outages

---

## 🎨 Visual Layout Guidelines (CRITICAL)

### Documentation Standards vs. User Preference

**⚠️ IMPORTANT**: There are TWO sets of layout guidelines in this project:

1. **WORKFLOW_GUIDELINES.md** - Team documentation standards (comprehensive rules with sticky notes)
2. **User's personal preference** - Minimalist approach (analyzed from existing workflows)

**When to use which**:
- **New workflows for team/documentation**: Follow WORKFLOW_GUIDELINES.md (includes sticky notes, node notes with emojis)
- **Personal workflows for user Nicolas**: Follow minimalist approach below (no sticky notes unless requested)
- **When in doubt**: Ask user or check WORKFLOW_GUIDELINES.md for team standards

📖 **See WORKFLOW_GUIDELINES.md** for complete documentation standards including:
- Mandatory sticky notes for sections
- Node notes with emoji conventions
- 200px spacing grid system
- Comprehensive visual organization rules

### User's Preferred Minimalist Style

**Based on analyzed preferences** from `scripts/your-style-layout.py`:

**Key Characteristics**:
- ✅ **Horizontal spacing**: ~150-240px (compact)
- ✅ **Vertical spacing**: ~160-200px (generous for readability)
- ✅ **Left-to-right flow**: Natural reading direction
- ✅ **Parallel branches**: Stacked vertically with clear separation
- ✅ **No line crossings**: Clean connections
- ⚠️ **Sticky notes**: Minimal usage (only when adding significant value, not by default)

### Layout Principles

#### 1. Horizontal Flow (Left → Right)
- Triggers/inputs on the left
- Processing in the middle
- Outputs on the right

#### 2. Vertical Branching
- Branches stack vertically (200px spacing minimum)
- Each branch flows horizontally at its Y level
- No diagonal connections

#### 3. Column Organization
- **Column 1**: Triggers (X ≈ -600 to -800)
- **Column 2**: Routing/Tools (X ≈ -200 to -400)
- **Column 3+**: Processing (X increments of 200-300px)

### Node Documentation

**Always add notes to nodes** (regardless of sticky note preference):
- Use emojis for visual clarity (see WORKFLOW_GUIDELINES.md)
- Explain complex logic, API calls, transformations
- Document edge cases and warnings
- Format: `[EMOJI] Title\n\nDescription`

### When Modifying Layouts

**ALWAYS**:
1. Check `scripts/fetch-current-layout.py` to see current state
2. Preserve spacing preferences (~150px horizontal, ~200px vertical)
3. **Ask about sticky notes** if creating new workflow (team standard vs. personal preference)
4. Keep horizontal flow left-to-right
5. Separate parallel branches vertically (200px minimum)
6. Add node notes with emojis to important nodes

**NEVER**:
- Cross connection lines
- Use tight spacing (<150px horizontal)
- Arrange nodes in grid patterns without flow direction
- Skip node documentation (always document complex nodes)

---

## 🔧 Development Workflows

### Creating a New Workflow System

1. **Create system folder**:
   ```bash
   mkdir "My New System"
   mkdir "My New System/workflow"
   ```

2. **Add workflows**: Export from n8n or create JSON

3. **Create README.md** following template in `n8n_instructions.md`

4. **Deploy**:
   ```bash
   ./scripts/deploy.sh --dry-run --dir "My New System"
   ./scripts/deploy.sh --dir "My New System"
   git push origin main
   ```

### Modifying Existing Workflows

1. **Fetch current state** (understand user's layout):
   ```bash
   python3 scripts/fetch-current-layout.py
   ```

2. **Edit local JSON**: Modify workflow files directly

3. **Update documentation**: Update system README.md if needed

4. **Deploy** (auto-commits before deploying):
   ```bash
   ./scripts/deploy.sh --dir "System Name"
   git push origin main
   ```

### Layout Modification Workflow

When asked to reorganize or improve workflow layouts:

```bash
# 1. Fetch current layout to understand preferences
python3 scripts/fetch-current-layout.py

# 2. Analyze spacing patterns
# Check: horizontal spacing, vertical spacing, sticky note usage

# 3. Create layout script based on user's style
# Reference: scripts/your-style-layout.py

# 4. Apply layout
python3 scripts/custom-layout.py

# 5. Deploy
./scripts/deploy.sh --dir "System Name"
```

### Common Development Tasks

#### Adding a New Node to Workflow

1. Read current workflow JSON
2. Add node to `nodes[]` array
3. Add connections to `connections{}` object
4. Follow user's layout spacing preferences
5. Deploy with dry-run first

#### Updating Node Parameters

1. Read workflow JSON
2. Find node by `name` field
3. Modify `parameters` object
4. Preserve `id`, `position`, `type`
5. Deploy

#### Creating Tool Workflow for AI Agent

1. Create workflow with clear purpose
2. Define input schema in first node
3. Add description (LLM reads this)
4. Test independently
5. Reference in AI Agent's "Call n8n Workflow Tool"

#### Implementing Error Handling

1. **Node level**: Enable "Continue on Fail" + Retry settings
2. **Workflow level**: Create/assign error workflow
3. **System level**: Centralized error logging (Slack, Sheets, PagerDuty)

---

## 🐛 Bug Tracking

### Before Debugging Any Issue

1. **Check** `BUGS_KNOWLEDGE.md` for known issues
2. **Search** by node type, error message, or symptom

```bash
# Search by node type
grep -i "telegram" BUGS_KNOWLEDGE.md
grep -i "mcp client" BUGS_KNOWLEDGE.md

# Search by severity
grep "🔴 Critique" BUGS_KNOWLEDGE.md
grep "🟡 Important" BUGS_KNOWLEDGE.md

# Search by error type
grep -i "timeout" BUGS_KNOWLEDGE.md
grep -i "authentication" BUGS_KNOWLEDGE.md
```

### After Resolving Any Bug

1. **Document immediately** in `BUGS_KNOWLEDGE.md`
2. **Follow standard format**: `[BUG-XXX]` with symptoms, root cause, solution
3. **Update statistics**

### Automated Workflow

```bash
/bug [description]  # Use SuperClaude command
```

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### Deploy fails with 401 Unauthorized
- Check `.env` file exists with valid `N8N_API_KEY`
- Verify API key at https://auto.mhms.fr/settings/api
- Test API key: `curl -H "Authorization: Bearer YOUR_KEY" https://auto.mhms.fr/api/v1/workflows`

#### Workflow not updating
- Ensure workflow `name` field matches exactly (case-sensitive)
- Check `DEBUG=1 ./scripts/deploy.sh` for detailed logs
- Verify workflow exists remotely: `./scripts/list.sh | grep "Workflow Name"`

#### Layout looks wrong after deployment
- Fetch current layout: `python3 scripts/fetch-current-layout.py`
- Check user's preferred spacing in `scripts/your-style-layout.py`
- Review WORKFLOW_GUIDELINES.md for documentation standards
- Check sticky note usage (team standard vs. user preference)
- Verify position coordinates in JSON

#### Code Node errors
- Check built-in variable syntax (`$input.all()`, `$json.field`)
- Use `_` autocomplete for available methods
- Remember: NO file system access, NO HTTP requests
- Test in "For Each Item" vs "Run Once for All Items"

#### Expression errors
- Use `{{ }}` syntax correctly
- Prefer `$node['Name']` over deprecated `$('Name')`
- Test expressions in expressions editor
- Handle missing data with optional chaining

#### AI Agent not working correctly
- Check agent type (Conversational vs Tools vs ReAct)
- Verify memory configuration for conversational agents
- Review tool descriptions (LLM reads these)
- Test tools independently
- Check LLM API credentials and rate limits

#### MCP Client connection errors
- Verify SSE endpoint is accessible
- Check authentication credentials
- Test MCP server independently
- Review tool selection (All vs Selected)

---

## 📚 Documentation References

### Project Documentation
- **CLAUDE.md** (this file): Complete Claude Code guidance with n8n expertise
- **claudedocs/n8n_comprehensive_documentation_2025.md**: Full n8n technical knowledge base
- **WORKFLOW_GUIDELINES.md**: Team documentation standards (mandatory sticky notes, node notes, visual organization)
- **MCP_SETUP.md**: MCP servers configuration (Context7, etc.)
- **GIT_SETUP.md**: Git & GitHub setup and versioning
- **README.md**: Project overview and quick start
- **DEPLOYMENT.md**: Complete deployment guide
- **BUGS_KNOWLEDGE.md**: Bug tracking database with solutions
- **n8n_instructions.md**: README template for workflow systems (French)

### External Resources
- **n8n Docs**: https://docs.n8n.io/
- **n8n API Reference**: https://docs.n8n.io/api/api-reference/
- **n8n Community**: https://community.n8n.io/
- **LangChain Docs**: https://python.langchain.com/docs/
- **MCP Protocol**: https://modelcontextprotocol.io/

---

## 🎯 Autonomy Guidelines

As Claude Code working on this project, you have **complete autonomy** with these guardrails:

### Technical Excellence

1. **n8n Expertise**:
   - Reference `claudedocs/n8n_comprehensive_documentation_2025.md` for technical details
   - Use Context7 MCP for real-time n8n documentation
   - Understand built-in variables, expressions, nodes deeply
   - Apply error handling patterns systematically

2. **Code Quality**:
   - Use built-in variables correctly (`$json`, `$input`, `$node`, `$execution`)
   - Prefer `$node['Name']` syntax over deprecated `$('Name')`
   - Handle missing data gracefully
   - Test expressions before deployment

3. **Authentication**:
   - Choose appropriate auth method (OAuth 2.0 > Bearer > API Key)
   - Use credential system (never hardcode)
   - Test auth independently

4. **Error Handling**:
   - Implement retry logic (3-5 attempts)
   - Use Continue on Fail for optional operations
   - Create/assign error workflows
   - Log errors centrally

### Visual Excellence

5. **Layout Standards**:
   - Consult WORKFLOW_GUIDELINES.md for team documentation standards
   - Check user preference for personal workflows (minimalist style)
   - Fetch current layout first: `python3 scripts/fetch-current-layout.py`
   - Use ~200px horizontal, ~200px vertical spacing
   - Left-to-right horizontal flow
   - Vertical stacking for parallel branches
   - Always add node notes with emojis to important nodes
   - Ask about sticky notes when creating new workflows (standards vs. preference)
   - Reference `scripts/your-style-layout.py` for user's minimalist style

### Deployment Excellence

6. **Testing & Deployment**:
   - Always `--dry-run` first
   - Git auto-commits before each deployment (no manual commits needed)
   - Push to GitHub after success: `git push origin main`
   - Verify with `./scripts/list.sh` after deployment

### Documentation Excellence

7. **Documentation**:
   - Update system README.md when making changes
   - Document bugs immediately in BUGS_KNOWLEDGE.md
   - Follow bug format: [BUG-XXX] with symptoms, cause, solution
   - Keep documentation synchronized with code

### Data Excellence

8. **Workflow State**:
   - Preserve `pinData`, `staticData`
   - Never modify workflow `id` when updating
   - Match by `name` field (case-sensitive)
   - Clean unsupported fields before API calls

### AI Agent Excellence

9. **AI Agent Implementation**:
   - Choose correct agent type (Conversational vs Tools vs ReAct)
   - Configure memory for conversational agents
   - Provide clear tool descriptions
   - Use Tool Workflows for reusable logic
   - Implement MCP integration when appropriate

### Best Practices Excellence

10. **Security & Performance**:
    - Enable webhook authentication
    - Use IP whitelist when sources known
    - Configure CORS appropriately
    - Set appropriate timeouts
    - Monitor execution times
    - Track error rates

---

## 🚀 Quick Reference Card

### Nicolas's Workflow Commands (TDAH-Optimized)

**When you say "PLAN"**:
- I summarize the goal in 1 sentence
- I create a numbered TODO list (3-6 items max)
- I list files to modify
- I STOP (no code, no execution)

**When you say "CODE étape X"**:
- I do ONLY step X
- I provide exact git diffs
- I add 1 mini test to verify
- I STOP (no spontaneous improvements)

**When you say "CHECK étape X"**:
- I compare result to initial goal
- If ✅ good → I say so
- If ❌ bug → I give minimal patch
- No refactoring, no suggestions

---

### Most Common Tasks

**Deploy workflow changes**:
```bash
./scripts/deploy.sh --dry-run --dir "System Name"
./scripts/deploy.sh --dir "System Name"
git push origin main
```

**Check current layout**:
```bash
python3 scripts/fetch-current-layout.py
```

**Search for bug**:
```bash
grep -i "keyword" BUGS_KNOWLEDGE.md
```

**Test API connection**:
```bash
./scripts/list.sh
```

**Debug deployment**:
```bash
DEBUG=1 ./scripts/deploy.sh --dir "System Name"
```

### Built-in Variables Quick Reference

```javascript
$input.all()                    // All items
$json.field                     // Current item field
$node['Name'].json.data        // Other node data
$execution.id                   // Execution ID
$workflow.name                  // Workflow name
```

### Expression Examples

```javascript
{{ $json.email.toLowerCase() }}                // String operation
{{ $now.plus({days: 7}).toISO() }}            // Date operation
{{ $json.items.length }}                       // Array operation
{{ $json.status === 'active' ? 'yes' : 'no' }} // Conditional
```

### Agent Type Selection

- **Conversational** → Chatbots, ongoing dialogue, needs memory
- **Tools Agent** → Multi-tool orchestration, API automation
- **ReAct** → Single-shot reasoning, no memory needed

### Error Handling Checklist

- [ ] Retry settings configured (3-5 attempts)
- [ ] Continue on Fail for optional operations
- [ ] Error workflow assigned
- [ ] Centralized error logging
- [ ] Appropriate timeouts set

---

**Maintained by**: Claude Code + Nicolas Marillot
**Instance**: https://auto.mhms.fr/
**Framework**: SuperClaude (25+ commands, 15+ agents, 8 MCP servers)
**Knowledge Base**: `claudedocs/n8n_comprehensive_documentation_2025.md`
**Last Updated**: 2025-11-01 (Added PLAN/CODE/CHECK workflow rules)
