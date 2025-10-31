# CLAUDE.md

This file provides comprehensive guidance to Claude Code (claude.ai/code) when working with n8n workflows in this repository.

---

# n8n Agent - Expert Workflow Automation Repository

Expert n8n developer specialized in creating, modifying, and improving automation workflows with deep technical knowledge and full SuperClaude Framework autonomy.

**Instance n8n**: `https://auto.mhms.fr/`
**Documentation**: Complete n8n knowledge base in `claudedocs/n8n_comprehensive_documentation_2025.md`

---

## 📖 Table of Contents

1. [Essential Commands](#-essential-commands)
2. [n8n Technical Knowledge](#-n8n-technical-knowledge)
3. [Architecture](#-architecture)
4. [Visual Layout Guidelines](#-visual-layout-guidelines)
5. [Development Patterns](#-development-patterns)
6. [Bug Tracking](#-bug-tracking-workflow)
7. [SuperClaude Integration](#-superclaude-framework-integration)
8. [Troubleshooting](#-troubleshooting)

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

# 2. Setup MCP servers (Context7 for documentation access)
./scripts/setup-mcp.sh

# 3. Make changes to workflow JSON files

# 4. Deploy with dry-run first
./scripts/deploy.sh --dry-run

# 5. Deploy for real (auto-commits to Git before deploying)
./scripts/deploy.sh

# 6. Push to GitHub after successful deployment
git push origin main
```

### MCP Servers (Context7)

**Context7 is configured** and provides real-time access to:
- n8n documentation (docs.n8n.io)
- Node.js documentation
- Framework patterns and examples

**How it works**: Automatically activated when you ask about n8n nodes, API, or technical documentation. No manual invocation needed.

**Configuration**: `~/.config/claude/mcp_config.json` (created by setup-mcp.sh)

### Fetch Current Layout from n8n

```bash
# Retrieve current workflow layouts to understand user preferences
export N8N_API_KEY="your_key"
python3 scripts/fetch-current-layout.py
```

---

## 🧠 n8n Technical Knowledge

### Code Node - JavaScript Capabilities

#### Built-in Variables & Methods

**Syntax Pattern**: Type `_` in Code node for autocomplete

**Core Variables**:
```javascript
// Access patterns
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

#### Available Libraries

**Luxon (built-in for date/time)**:
```javascript
.toDateTime()   // Convert to DateTime
.plus()        // Add time
.minus()       // Subtract time
.format()      // Format string
.isWeekend()   // Check weekend
```

**External npm Packages**:
- ✅ Available in self-hosted installations ONLY
- ❌ NOT available in n8n Cloud
- Requires configuration in instance settings

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
✅ **Can** use Luxon library
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

⚠️ **Important**: Use `$node[]` syntax, NOT deprecated `$()`

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

**Required**:
- Client ID
- Client Secret
- Authorization URL
- Access Token URL
- Scope (optional)

**Grant Types**:
- Authorization Code
- Client Credentials
- Resource Owner Password
- Refresh Token

**n8n Advantages**:
- Automatic token refresh
- Secure credential storage
- User-friendly OAuth flow

### Webhook Node Configuration

#### URL Types

**Test URL** (`/webhook-test/<path>`):
- Active when workflow is NOT active
- Shows incoming data in UI
- For development/debugging

**Production URL** (`/webhook/<path>`):
- Active when workflow IS active
- Runs silently (no UI display)
- For live integrations

**Toggle**: Click "Test URL" or "Production URL" at top of node

#### Authentication Options

1. **None**: Open webhook (⚠️ security risk)
2. **Basic Auth**: Username + Password
3. **Header Auth**: Static token in header (e.g., `X-API-Key`)
4. **JWT Auth**: Signed JSON Web Token validation

#### CORS & Security

**Allowed Origins**:
- Default: `*` (all origins)
- Specify: `https://example.com,https://app.example.com`

**IP Whitelist**:
- Comma-separated IPs: `192.168.1.1,10.0.0.5`
- Prevents unauthorized calls

#### Response Modes

1. **On Workflow Completion**: Wait for entire workflow
2. **Last Node**: Respond immediately with last output
3. **Webhook Response Node**: Custom response control

**Best practice**: Use "Respond to Webhook" node for complex workflows to avoid timeouts

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

#### LangChain Components

**Chat Models (LLM Providers)**:
- OpenAI (GPT-3.5, GPT-4, GPT-4 Turbo)
- Anthropic (Claude 3 Opus, Sonnet, Haiku)
- Google Gemini
- Azure OpenAI
- Mistral Cloud
- Groq, Cohere, DeepSeek
- Ollama (self-hosted)

**Memory Types**:
- Simple Memory (session-based)
- MongoDB Chat Memory (persistent)
- Redis Chat Memory (fast, ephemeral)
- Postgres Chat Memory (persistent)
- Zep (conversational AI optimized)

**Tools**:
- Calculator
- Wikipedia
- Wolfram|Alpha
- SerpApi (Google search)
- Custom Code Tool
- Call n8n Workflow Tool
- MCP Client Tool
- Vector Store QA Tool

**Vector Stores (for RAG)**:
- Pinecone, Qdrant, Weaviate
- Supabase, PGVector
- MongoDB Atlas, Redis
- Milvus, Zep

**Embeddings**:
- OpenAI, Azure OpenAI
- Cohere, Google Gemini
- HuggingFace, Mistral
- Ollama, AWS Bedrock

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

**Use Cases**:
- File system access
- Code execution
- Database queries
- External APIs

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

**Configuration**:
- **Description**: What the tool does (LLM reads this)
- **Source**: Which workflow to call
- **Workflow Inputs**: Data mapping

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

**Example**:
```
Error Trigger → Parse Error → Slack Alert → Log to Google Sheets
```

#### 2. Continue on Fail

**Per-node setting**:
- ✅ **Continue**: Skip failed node, continue workflow
- ❌ **Stop**: Halt workflow on error (default)

**When enabled**:
- Exposes error output (red connector)
- Route failures to different path

**Example**:
```
HTTP Request (Continue on Fail enabled)
    ↓ success              ↓ error
Process Data      Send Error Alert
```

#### 3. Retry on Fail

**Configuration**:
- Max Retry Attempts: 1-5 (typically 3)
- Retry Interval: Time between retries
- Exponential backoff (recommended)

**Best for**: Network requests, external APIs, temporary outages

#### Error Handling Best Practices

**Node-Level**:
- Enable retries for external API calls (3-5 attempts)
- Use Continue on Fail for optional operations
- Set appropriate timeouts

**Workflow-Level**:
- Assign error workflow to all production workflows
- Use descriptive workflow names
- Tag workflows (critical, non-critical)
- Test error handling explicitly

**System-Level**:
- Centralized error workflow
- Tiered alerting (Critical → PagerDuty, Important → Slack, Minor → Log)
- Error analytics and pattern tracking
- Regular error log reviews

### REST API Endpoints

**Base URL**: `https://auto.mhms.fr/api/v1/`

#### Workflows

```bash
GET    /workflows          # List all
GET    /workflows/:id      # Get specific
POST   /workflows          # Create new
PUT    /workflows/:id      # Update existing
DELETE /workflows/:id      # Delete
PUT    /workflows/:id/activate    # Activate
PUT    /workflows/:id/deactivate  # Deactivate
```

#### Executions

```bash
GET    /executions         # List executions
GET    /executions/:id     # Get execution details
DELETE /executions/:id     # Delete execution
```

**Query Parameters**:
- `workflowId`: Filter by workflow
- `status`: Filter by status
- `limit`: Pagination

#### Credentials

```bash
GET    /credentials        # List (names only, not values)
```

**Security**: Credential VALUES are NOT returned via API

#### Authentication

**API Key Setup**:
1. Go to n8n Settings → API
2. Generate API key
3. Use in Authorization header

**Usage**:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://auto.mhms.fr/api/v1/workflows
```

#### Using n8n Node (Alternative)

**Advantages**:
- No manual auth management
- Built-in error handling
- Visual workflow integration

**Operations**: Workflow management, execution listing, credential listing

---

## 📁 Architecture

### Project Structure

```
n8n Agent/
├── CLAUDE.md                    # This file - Complete guidance
├── README.md                    # Project overview
├── DEPLOYMENT.md                # Deployment guide
├── BUGS_KNOWLEDGE.md            # Bug tracking database
├── WORKFLOW_GUIDELINES.md       # Visual layout best practices
├── GIT_SETUP.md                 # Git & GitHub guide
├── MCP_SETUP.md                 # MCP servers setup
├── n8n_instructions.md          # README template (French)
├── .env                         # Configuration (API keys)
│
├── claudedocs/
│   └── n8n_comprehensive_documentation_2025.md  # Complete n8n knowledge base
│
├── scripts/
│   ├── deploy.sh                # Deployment with auto-commit
│   ├── deploy.js                # Node.js deployment logic
│   ├── list-workflows.js        # List workflows from API
│   ├── setup-mcp.sh             # MCP servers installation
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
- **Preserves**: `pinData`, `staticData`
- **Cleans**: `id`, `createdAt`, `updatedAt`, `versionId`
- **Excludes**: `executionOrder`, `callerPolicy` (unsupported by API)

**Workflow Matching**: By `name` field (exact match, case-sensitive)

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

## 🐛 Bug Tracking Workflow

**Before debugging any issue**:
1. Check `BUGS_KNOWLEDGE.md` for known issues
2. Search by node type, error message, or symptom

**After resolving any bug**:
1. Document immediately in `BUGS_KNOWLEDGE.md`
2. Follow standard format: `[BUG-XXX]` with symptoms, root cause, solution
3. Update statistics

**Automated workflow**:
```bash
/bug [description]  # Use SuperClaude command
```

**Search patterns**:
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

---

## 🤖 SuperClaude Framework Integration

### Available Commands

- `/sc:implement` - Feature implementation with intelligent persona
- `/sc:analyze` - Architecture and code analysis
- `/sc:design` - System design and planning
- `/sc:troubleshoot` - Debug and fix issues
- `/sc:document` - Generate comprehensive documentation
- `/sc:research` - Deep research with web search
- `/sc:test` - Execute tests with coverage analysis
- `/sc:improve` - Code quality improvements
- `/sc:git` - Git operations with smart commits
- `/bug` - Automated bug tracking workflow

### Specialized Agents

- **backend-architect**: API and system design
- **frontend-architect**: UI components and user experience
- **performance-engineer**: Optimization and bottleneck elimination
- **security-engineer**: Security vulnerabilities and compliance
- **technical-writer**: Documentation creation
- **deep-research-agent**: Comprehensive research with Tavily
- **python-expert**: Production-ready Python code

### MCP Server Integration

**Context7**: Real-time access to n8n, Node.js, framework documentation
**Sequential**: Complex reasoning and multi-step analysis
**Serena**: Session persistence and project memory
**Tavily**: Web search for current information

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

### n8n Nodes Expertise

**Core Nodes**:
- Code (JavaScript/Python)
- HTTP Request (all auth types)
- Webhook (test/production)
- Switch, IF, Merge
- Set, Filter, Split Out
- Error Trigger
- Respond to Webhook

**Langchain/AI Nodes**:
- AI Agent (Conversational, Tools, ReAct)
- LLM Chat (OpenAI, Anthropic, Gemini)
- MCP Client Tool
- MCP Server Trigger
- Call n8n Workflow Tool
- Simple Memory, MongoDB Memory, Redis Memory
- Vector Store (Pinecone, Qdrant, etc.)
- Embeddings (OpenAI, Cohere, etc.)

**Integration Nodes**:
- Telegram Bot
- Notion
- OpenAI
- Anthropic
- Google Sheets
- Slack

### Workflow Patterns

**Tool Workflows**: Reusable components called by AI agents
**Agent Loops**: Autonomous agents with planning/execution
**Memory Management**: Conversation state retention
**Error Workflows**: Centralized error handling
**RAG Patterns**: Vector stores + retrieval + LLM

### Data Flow Concepts

**Items**: Data units flowing between nodes
**Execution Order**: Sequential unless parallel branches
**Pinned Data**: Test data locked to nodes
**Static Data**: Persistent node-specific data
**Expressions**: Dynamic value generation with `{{ }}`

---

## 🐛 Troubleshooting

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
- Remember: NO sticky notes by default
- Verify position coordinates in JSON

#### Code Node errors
- Check built-in variable syntax (`$input.all()`, `$json.field`)
- Use `_` autocomplete for available methods
- Remember: NO file system access, NO HTTP requests
- Test in "For Each Item" vs "Run Once for All Items"

#### Expression errors
- Use `{{ }}` syntax correctly
- Prefer `$node[]` over deprecated `$()`
- Test expressions in expressions editor
- Handle missing data with optional chaining

#### Authentication failures (HTTP Request)
- Verify credential type matches API requirements
- Check OAuth 2.0 token refresh settings
- Test credentials independently
- Review API documentation for auth requirements

#### Webhook not receiving data
- Check webhook URL type (test vs production)
- Verify workflow is active for production URL
- Test authentication settings
- Check IP whitelist if configured
- Verify CORS configuration for browser calls

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
- **WORKFLOW_GUIDELINES.md**: Visual layout best practices
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
   - Prefer `$node[]` syntax over deprecated `$()`
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

5. **Layout Preferences**:
   - **NO sticky notes** unless explicitly requested
   - Fetch current layout first: `python3 scripts/fetch-current-layout.py`
   - Use ~200px horizontal, ~200px vertical spacing
   - Left-to-right horizontal flow
   - Vertical stacking for parallel branches
   - Reference `scripts/your-style-layout.py` for user's style

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
**Last Updated**: 2025-01-01
