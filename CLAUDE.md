# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

# n8n Agent - Workflow Automation Repository

Expert n8n developer specialized in creating, modifying, and improving automation workflows with full SuperClaude Framework autonomy.

**Instance n8n**: `https://auto.mhms.fr/`

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

# Debug mode
DEBUG=1 ./scripts/deploy.sh
```

### Development Workflow

```bash
# 1. Setup environment (first time)
cp .env.example .env
# Edit .env and add N8N_API_KEY from https://auto.mhms.fr/

# 2. Make changes to workflow JSON files

# 3. Deploy with dry-run first
./scripts/deploy.sh --dry-run

# 4. Deploy for real (auto-commits to Git before deploying)
./scripts/deploy.sh

# 5. Push to GitHub after successful deployment
git push origin main
```

### Fetch Current Layout from n8n

```bash
# Retrieve current workflow layouts to understand user preferences
export N8N_API_KEY="your_key"
python3 scripts/fetch-current-layout.py
```

---

## 📁 Architecture

### Project Structure

```
n8n Agent/
├── CLAUDE.md                    # This file
├── README.md                    # Project overview
├── DEPLOYMENT.md                # Deployment guide
├── BUGS_KNOWLEDGE.md            # Bug tracking database
├── WORKFLOW_GUIDELINES.md       # Visual layout & best practices
├── .env                         # Configuration (API keys)
│
├── scripts/
│   ├── deploy.sh                # Deployment with auto-commit
│   ├── deploy.js                # Node.js deployment logic
│   ├── list-workflows.js        # List workflows from API
│   ├── fetch-current-layout.py  # Retrieve layouts from n8n
│   └── your-style-layout.py     # User's preferred layout style
│
└── [System Folders]/            # Each system = group of related workflows
    ├── README.md                # System documentation
    └── workflow/
        └── *.json               # Workflow files
```

### API Integration (scripts/deploy.js)

**Key Functions**:
```javascript
// HTTP client for n8n API
function apiRequest(method, endpoint, body)

// Workflow operations
async function getRemoteWorkflows()      // GET /api/v1/workflows
async function createWorkflow(data)      // POST /api/v1/workflows
async function updateWorkflow(id, data)  // PUT /api/v1/workflows

// Data preparation
function cleanWorkflowForAPI(workflow)   // Remove unsupported fields
```

**Update Logic**:
- Preserves: `pinData`, `staticData`
- Cleans: `id`, `createdAt`, `updatedAt`, `versionId`
- Excludes: `executionOrder`, `callerPolicy` (unsupported)

**Workflow Matching**: Matched by `name` field (exact match, case-sensitive)

---

## 🎨 Visual Layout Guidelines (CRITICAL)

### User's Preferred Layout Style

Based on analyzed preferences from `scripts/your-style-layout.py`:

**Key Characteristics**:
- ❌ **NO sticky notes** - User prefers clean view without overlays
- ✅ **Horizontal spacing**: ~150-240px (compact)
- ✅ **Vertical spacing**: ~160-200px (generous for readability)
- ✅ **Left-to-right flow**: Natural reading direction
- ✅ **Parallel branches**: Stacked vertically with clear separation
- ✅ **No line crossings**: Clean connections

### Layout Principles

1. **Horizontal Flow** (Left → Right)
   - Trigger/inputs on the left
   - Processing in the middle
   - Outputs on the right

2. **Vertical Branching**
   - Branches stack vertically (200px spacing minimum)
   - Each branch flows horizontally at its Y level
   - No diagonal connections

3. **Column Organization**
   - Column 1: Triggers (X ≈ -600 to -800)
   - Column 2: Routing/Tools (X ≈ -200 to -400)
   - Column 3+: Processing (X increments of 200-300px)

### Example: MCP Workflow Layout

```
MCP Server Trigger     (X: -1008, Y: 256)
    ↓
Tools (vertical column, X: -1264):
    search_projects    (Y: -368)
    get_project_by_id  (Y: -208)
    list_categories    (Y: -48)
    ...                (Y: +160px each)
    ↓
Execute Trigger → Switch → Branches (parallel, 160px vertical spacing)
```

### When Modifying Layouts

**ALWAYS**:
1. Check `scripts/fetch-current-layout.py` to see current state
2. Preserve user's spacing preferences (~150px horizontal, ~200px vertical)
3. Never add sticky notes unless explicitly requested
4. Keep horizontal flow left-to-right
5. Separate parallel branches vertically (200px minimum)

**NEVER**:
- Add sticky notes by default
- Cross connection lines
- Use tight spacing (<150px horizontal)
- Arrange nodes in grid patterns without flow direction

---

## 🔧 Development Patterns

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

```python
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

---

## 🐛 Bug Tracking Workflow

**Before debugging any issue**:
1. Check `BUGS_KNOWLEDGE.md` for known issues
2. Search by node type, error message, or symptom

**After resolving any bug**:
1. Document immediately in `BUGS_KNOWLEDGE.md`
2. Follow standard format: `[BUG-XXX]` with symptoms, root cause, solution

**Automated workflow**:
```bash
/bug [description]  # Use SuperClaude command
```

---

## 🤖 SuperClaude Framework Integration

### Available Commands
- `/sc:implement` - Feature implementation
- `/sc:analyze` - Architecture analysis
- `/sc:design` - System design
- `/sc:troubleshoot` - Debug issues
- `/sc:document` - Generate documentation
- `/bug` - Automated bug tracking

### Specialized Agents
- backend-architect: API and system design
- frontend-architect: UI components
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

### Workflow Patterns
- **Tool Workflows**: Reusable workflow components
- **Agent Loops**: Autonomous agents with planning/execution
- **Memory Management**: Conversation state retention

---

## 🐛 Troubleshooting

### Common Issues

**Deploy fails with 401 Unauthorized**:
- Check `.env` file exists with valid `N8N_API_KEY`
- Verify API key at https://auto.mhms.fr/settings/api

**Workflow not updating**:
- Ensure workflow `name` field matches exactly (case-sensitive)
- Check `DEBUG=1 ./scripts/deploy.sh` for detailed logs

**Layout looks wrong after deployment**:
- Fetch current layout: `python3 scripts/fetch-current-layout.py`
- Check user's preferred spacing in `scripts/your-style-layout.py`
- Remember: NO sticky notes by default

---

## 📚 Documentation Structure

- **CLAUDE.md** (this file): Claude Code guidance
- **WORKFLOW_GUIDELINES.md**: Visual layout best practices
- **README.md**: Project overview
- **DEPLOYMENT.md**: Complete deployment guide
- **BUGS_KNOWLEDGE.md**: Bug tracking database

---

## 🎯 Autonomy Guidelines

As Claude Code working on this project:

1. **Visual layout**: Always check user's style preferences first (`scripts/your-style-layout.py`)
2. **No sticky notes**: Don't add sticky notes unless explicitly requested
3. **Spacing**: Use ~200px horizontal, ~200px vertical
4. **Flow direction**: Always left-to-right horizontal flow
5. **Test with --dry-run** before actual deployment
6. **Git commits automatically** before each deployment
7. **Update documentation** when making changes
8. **Document bugs immediately** in BUGS_KNOWLEDGE.md
9. **Preserve workflow state** (pinData, staticData)
10. **Push to GitHub** after successful deployments

---

**Maintained by**: Claude Code + Nicolas Marillot
**Instance**: https://auto.mhms.fr/
**Framework**: SuperClaude (25+ commands, 15+ agents, 8 MCP servers)