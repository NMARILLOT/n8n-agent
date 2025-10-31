# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# n8n Agent - Workflow Automation Repository

Expert n8n developer specialized in creating, modifying, and improving automation workflows with full SuperClaude Framework autonomy.

**Instance n8n**: `https://auto.mhms.fr/`

---

## 🎯 Core Mission

Create and manage n8n workflows via API with full autonomy for:
- Creating new workflows programmatically
- Modifying existing workflows
- Deploying workflows automatically
- Managing workflow lifecycle (create, update, delete, activate)
- Maintaining workflow documentation

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

# Debug mode (environment variable)
DEBUG=1 ./scripts/deploy.sh
```

### Development Workflow

```bash
# 1. Setup environment (first time)
cp .env.example .env
# Edit .env and add N8N_API_KEY from https://auto.mhms.fr/

# 2. List current workflows
./scripts/list.sh

# 3. Make changes to workflow JSON files

# 4. Deploy with dry-run first
./scripts/deploy.sh --dry-run

# 5. Deploy for real (auto-commits to Git before deploying)
./scripts/deploy.sh

# 6. Push to GitHub (after successful deployment)
git push origin main
```

### Git Versioning

Every deployment **automatically creates a Git commit** before deploying:
- Timestamp of deployment
- Target workflows (all or specific system)
- Mode (production or dry-run)

This ensures complete version history and rollback capability.

---

## 📁 Architecture

### Project Structure

```
n8n Agent/
├── CLAUDE.md                    # This file - Claude Code guidance
├── n8n_instructions.md          # French n8n developer instructions
├── README.md                    # Project overview
├── DEPLOYMENT.md                # Deployment guide
├── BUGS_KNOWLEDGE.md            # Bug tracking database
├── WORKFLOW_GUIDELINES.md       # Workflow best practices
├── .env                         # Configuration (API keys)
├── .env.example                 # Configuration template
│
├── scripts/
│   ├── deploy.sh                # Bash deployment wrapper
│   ├── deploy.js                # Node.js deployment logic (380 lines)
│   ├── list.sh                  # List workflows wrapper
│   └── list-workflows.js        # List workflows from n8n API
│
├── claudedocs/                  # Architecture analysis & guides
│   ├── START_HERE.md            # Quick start decision guide
│   ├── UPDATED_SUMMARY.md       # Current state analysis
│   ├── UPDATED_ANALYSIS.md      # Detailed architecture review
│   ├── IMPLEMENTATION_ROADMAP.md
│   ├── ARCHITECTURE_ANALYSIS.md
│   └── README.md
│
├── .claude/
│   └── commands/
│       └── bug.md               # /bug command workflow
│
└── [System Folders]/            # Each system = group of related workflows
    ├── README.md                # System documentation
    └── workflow/
        ├── workflow1.json
        └── workflow2.json
```

### API Integration (scripts/deploy.js)

**Key Functions**:
```javascript
// HTTP client for n8n API
function apiRequest(method, endpoint, body)

// Workflow operations
async function getRemoteWorkflows()      // GET /api/v1/workflows
async function getWorkflow(id)           // GET /api/v1/workflows/:id
async function createWorkflow(data)      // POST /api/v1/workflows
async function updateWorkflow(id, data)  // PUT /api/v1/workflows/:id

// Data preparation
function cleanWorkflowForAPI(workflow)   // Remove unsupported fields
```

**Update Logic**:
- Preserves: `pinData` (test data), `staticData` (workflow state)
- Cleans: `id`, `createdAt`, `updatedAt`, `versionId`
- Excludes: `executionOrder`, `callerPolicy` (unsupported by API)

**Workflow Matching**:
```javascript
// Workflows matched by name field
const existingWorkflow = remoteWorkflows.find(w => w.name === workflowName);

if (existingWorkflow) {
    // Update existing
    await updateWorkflow(existingWorkflow.id, workflowData);
} else {
    // Create new
    await createWorkflow(workflowData);
}
```

---

## 🔧 Development Patterns

### Creating a New Workflow System

1. **Create system folder**:
   ```bash
   mkdir "My New System"
   mkdir "My New System/workflow"
   ```

2. **Add workflows**:
   ```bash
   # Export from n8n or create JSON
   # Place in workflow/ directory
   ```

3. **Create README.md**:
   - Use template from n8n_instructions.md
   - Document objectives, integrations, credentials
   - List all workflows and their roles

4. **Deploy**:
   ```bash
   ./scripts/deploy.sh --dry-run --dir "My New System"
   ./scripts/deploy.sh --dir "My New System"
   ```

### Modifying Existing Workflows

1. **List current state**:
   ```bash
   ./scripts/list.sh
   ```

2. **Edit local JSON**:
   - Modify workflow JSON files directly
   - OR export from n8n editor after manual changes

3. **Update documentation**:
   - Update system README.md if changes affect architecture

4. **Deploy with automatic Git commit**:
   ```bash
   ./scripts/deploy.sh --dry-run --dir "System Name"
   ./scripts/deploy.sh --dir "System Name"  # Auto-commits before deploying
   git push origin main                      # Push to GitHub
   ```

### Git History and Rollback

```bash
# View deployment history
git log --oneline --grep="Pre-deployment"

# View changes to a specific workflow
git log --follow -- "System Name/workflow/workflow.json"

# Rollback to previous version
git checkout COMMIT_HASH -- "System Name/workflow/workflow.json"
./scripts/deploy.sh --dir "System Name"  # Redeploy old version
```

### Bug Tracking Workflow

**Before debugging any issue**:
1. Check BUGS_KNOWLEDGE.md for known issues
2. Search by node type, error message, or symptom

**After resolving any bug**:
1. Document immediately in BUGS_KNOWLEDGE.md
2. Follow standard format: [BUG-XXX] with symptoms, root cause, solution
3. Update statistics section

**Automated workflow**:
```bash
# Use /bug command for automated bug handling
/bug [description]
```

---

## 🤖 SuperClaude Framework Integration

This project uses SuperClaude Framework with full autonomy:

### Available Commands
- `/sc:implement` - Feature implementation with API
- `/sc:analyze` - Architecture and code analysis
- `/sc:design` - System architecture design
- `/sc:improve` - Code quality improvements
- `/sc:troubleshoot` - Debug and fix issues
- `/sc:document` - Generate documentation
- `/sc:test` - Run tests and validation
- `/bug` - Automated bug tracking workflow

### Execution Modes
- Task Management: Multi-step coordination
- Brainstorming: Requirements discovery
- Research: Deep investigation
- Orchestration: Tool optimization
- Token Efficiency: Compressed communication

### Specialized Agents
- backend-architect: API and system design
- frontend-architect: UI components
- security-engineer: Security review
- performance-engineer: Optimization
- technical-writer: Documentation

---

## 🔑 Environment Variables

Required in `.env`:
```bash
N8N_API_KEY=your_api_key_here
N8N_HOST=https://auto.mhms.fr
```

Get API key from: `https://auto.mhms.fr/settings/api`

---

## 🛠️ Technical Details

### n8n Nodes Used
- **Langchain**: Agent, LLM Chat, MCP Client, Memory, Tool Workflow
- **Native**: Telegram, HTTP Request, Code, Switch, Merge, Set, IF
- **Integration**: Notion, OpenAI, Anthropic

### MCP Protocol
- **SSE Servers**: Server-Sent Events for real-time communication
- **Tools**: Callable functions exposed by MCP servers
- **Triggers**: Event-based workflow activation
- **Resources**: Structured data access patterns

### Workflow Patterns
- **Tool Workflows**: Reusable workflow components called as functions
- **Agent Loops**: Autonomous agents with planning and execution
- **Memory Management**: Conversation state and context retention
- **Error Handling**: Graceful degradation and retry logic

---

## 🐛 Troubleshooting

### Common Issues

**Deploy fails with 401 Unauthorized**:
- Check `.env` file exists with valid `N8N_API_KEY`
- Verify API key at https://auto.mhms.fr/settings/api

**Workflow not updating**:
- Ensure workflow `name` field matches exactly (case-sensitive)
- Check `DEBUG=1 ./scripts/deploy.sh` for detailed logs

**List shows no workflows**:
- Verify n8n instance is accessible
- Check API key permissions

---

## 📚 Documentation Structure

- **CLAUDE.md** (this file): Claude Code guidance
- **n8n_instructions.md**: README.md template for workflow systems (French)
- **README.md**: Project overview and quick start
- **DEPLOYMENT.md**: Complete deployment documentation
- **GIT_SETUP.md**: Git & GitHub setup and versioning guide
- **BUGS_KNOWLEDGE.md**: Bug tracking database
- **claudedocs/**: Architecture analysis and roadmaps

---

## 🎯 Autonomy Guidelines

As Claude Code working on this project:

1. **Always check documentation first** (BUGS_KNOWLEDGE.md, READMEs)
2. **Test with --dry-run** before actual deployment
3. **Git commits automatically** before each deployment (no manual commits needed)
4. **Update documentation** when making changes (especially system README.md)
5. **Follow n8n_instructions.md** template for new workflow system READMEs
6. **Document bugs immediately** in BUGS_KNOWLEDGE.md when resolved
7. **Use SuperClaude commands** for complex tasks (/sc:implement, /bug, etc.)
8. **Preserve workflow state** (pinData, staticData) during updates
9. **Push to GitHub** after successful deployments (git push origin main)

---

**Maintained by**: Claude Code + Nicolas Marillot
**Instance**: https://auto.mhms.fr/
**Framework**: SuperClaude (25+ commands, 15+ agents, 8 MCP servers)
