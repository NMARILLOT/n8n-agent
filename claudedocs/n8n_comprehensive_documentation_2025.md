# n8n Comprehensive Documentation - Expert Reference Guide

**Research Date**: 2025-01-01
**Purpose**: Complete technical reference for n8n workflow automation platform
**Confidence Level**: High (based on official documentation and community resources)

---

## Table of Contents

1. [Code Node - JavaScript Capabilities](#1-code-node---javascript-capabilities)
2. [Expression System & Built-in Variables](#2-expression-system--built-in-variables)
3. [HTTP Request Node - Authentication](#3-http-request-node---authentication)
4. [Webhook Node Configuration](#4-webhook-node-configuration)
5. [AI Agents & LangChain Integration](#5-ai-agents--langchain-integration)
6. [Tool Workflows & MCP Integration](#6-tool-workflows--mcp-integration)
7. [REST API Endpoints](#7-rest-api-endpoints)
8. [Error Handling Patterns](#8-error-handling-patterns)
9. [Best Practices Summary](#9-best-practices-summary)

---

## 1. Code Node - JavaScript Capabilities

### Overview
The Code node allows custom JavaScript (or Python) execution as workflow steps. It's the most flexible node for data transformation and custom logic.

### Built-in Methods & Variables

**Syntax Pattern**: `_variableName` or `_methodName()`

Type `_` in the Code node to see autocomplete suggestions for all built-in methods and variables.

**Key Built-in Variables**:
- `$input` - Access all incoming items at once
- `$json` - Access current item's JSON data (in "For Each Item" mode)
- `$node()` - Access data from other nodes
- `$execution` - Access workflow and execution metadata
- `$workflow` - Access workflow information

### Available Libraries

**Luxon Library** (built-in for date/time):
```javascript
// Date manipulation examples
.toDateTime()   // Convert to DateTime object
.plus()         // Add time
.minus()        // Subtract time
.format()       // Format date string
.isWeekend()    // Check if weekend
```

**External npm Packages**:
- Available ONLY in self-hosted installations
- Requires configuration in instance settings
- NOT available in n8n Cloud

### Execution Modes

**Run Once for All Items**:
```javascript
// Access all items with $input.all()
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
// Access current item with $json
return {
  city: $json.city,
  processed: true
};
```

### Limitations

❌ **Cannot** access file system
❌ **Cannot** make HTTP requests directly (use HTTP Request node)
✅ **Can** transform data, use built-in JavaScript methods
✅ **Can** access Luxon library for dates
✅ **Can** use complex JavaScript logic

### Best Practices

1. **Use dedicated nodes** for HTTP requests and file operations
2. **Leverage built-in methods** instead of reinventing logic
3. **Test code** in "For Each Item" vs "All Items" modes
4. **Handle errors** with try-catch blocks
5. **Document complex logic** with comments

**Reference**: https://docs.n8n.io/code/code-node/

---

## 2. Expression System & Built-in Variables

### Expression Syntax

**Basic Pattern**: `{{ JavaScript expression here }}`

Expressions work in most node input fields and use the Tournament templating language extended with n8n custom methods.

### Core Variables

#### `$json`
Access incoming JSON data for current item (For Each Item mode).

```javascript
{{ $json.city }}                    // Direct property access
{{ $json['body']['city'] }}         // Nested property access
{{ $json.items[0].name }}           // Array access
```

#### `$input`
Access all items at once (Run Once for All Items mode).

```javascript
$input.all()                        // Get all items
$input.first()                      // Get first item
$input.last()                       // Get last item
```

#### `$node`
Access data from other nodes.

```javascript
{{ $node['Get an order'].json.data }}           // Access specific node output
{{ $node['HTTP Request'].json.body.results }}   // Access nested data
```

**Alternative Syntax** (deprecated but may still work):
```javascript
{{ $('Node Name').json.data }}
```

⚠️ **Note**: Recent updates may have compatibility issues with `$()` syntax. Prefer `$node[]` syntax.

#### `$execution`
Access workflow execution metadata.

```javascript
{{ $execution.id }}                 // Execution ID
{{ $execution.mode }}               // Execution mode (manual, trigger, etc.)
{{ $execution.resumeUrl }}          // Resume URL for paused workflows
```

#### `$workflow`
Access workflow information.

```javascript
{{ $workflow.id }}                  // Workflow ID
{{ $workflow.name }}                // Workflow name
{{ $workflow.active }}              // Is workflow active?
```

### Built-in Functions

Access with `$` prefix and autocomplete in expressions editor.

**Common patterns**:
- Date/time manipulation with Luxon
- String operations
- Array methods
- Math operations
- Object handling

### Best Practices

1. **Use `$node[]` syntax** instead of deprecated `$()`
2. **Type `$` for autocomplete** to discover available methods
3. **Test expressions** in the expressions editor
4. **Handle missing data** with optional chaining or defaults
5. **Keep expressions simple** - use Code node for complex logic

**Reference**: https://docs.n8n.io/code/expressions/

---

## 3. HTTP Request Node - Authentication

### Supported Authentication Methods

n8n supports comprehensive authentication through its credentials system.

#### 1. **Bearer Token Authentication**

**Setup**:
1. Go to **Credentials** → **Create New** → **HTTP Bearer Token Auth**
2. Enter your Bearer Token
3. Save credential
4. In HTTP Request node, select **Bearer Auth**
5. Choose your saved credential

**Under the hood**: Sets `Authorization: Bearer <token>` header

**Use cases**: Modern REST APIs, OAuth 2.0 access tokens

#### 2. **OAuth 1.0**

**Configuration**:
- Use generic OAuth1 authentication
- Requires: Consumer Key, Consumer Secret
- Support for request token URL and authorization URL

**Use cases**: Twitter API v1.1, legacy APIs

#### 3. **OAuth 2.0**

**Configuration Requirements** (vary by Grant Type):
- **Client ID** (required)
- **Client Secret** (required)
- **Authorization URL** (required)
- **Access Token URL** (required)
- **Scope** (optional, space-separated)

**Grant Types Supported**:
- Authorization Code
- Client Credentials
- Resource Owner Password
- Refresh Token

**n8n Advantages**:
- User-friendly OAuth flow interface
- Automatic token refresh handling
- Secure credential storage

**Use cases**: Google APIs, Microsoft Graph, Salesforce, most modern APIs

#### 4. **API Key / Header Auth**

**Setup**:
1. Create **Header Auth** credential
2. Specify header name (e.g., `X-API-Key`, `api-key`)
3. Enter API key value

**Common header names**:
- `X-API-Key`
- `api-key`
- `apikey`
- `Authorization` (for custom schemes)

**Use cases**: Simple REST APIs, webhooks, internal APIs

#### 5. **Basic Authentication**

**Configuration**:
- Username
- Password

**Encoding**: Automatically encodes as `Base64(username:password)` and sets `Authorization: Basic <encoded>` header

**Use cases**: Simple HTTP auth, legacy systems, internal tools

#### 6. **Query Authentication**

**Setup**:
- Add API key/token as query parameter
- Specify parameter name (e.g., `api_key`, `token`)

**Example**: `https://api.example.com/data?api_key=YOUR_KEY`

**Use cases**: Some legacy APIs, simple authentication schemes

#### 7. **Custom Authentication**

**Flexible configuration** for non-standard auth schemes:
- Custom headers
- Multiple authentication parameters
- Complex auth flows

### Authentication Best Practices

1. **Use credential reuse**: Store credentials once, use in multiple nodes
2. **Never hardcode secrets**: Always use credential system
3. **Test auth separately**: Verify credentials work before complex workflows
4. **Handle token expiry**: Use OAuth 2.0 with automatic refresh when possible
5. **Monitor auth failures**: Set up error handling for 401/403 responses

**Reference**: https://docs.n8n.io/integrations/builtin/credentials/httprequest/

---

## 4. Webhook Node Configuration

### Webhook URL Types

n8n provides TWO webhook URLs per Webhook node:

#### **Test URL**
- **Registration**: Created when you click "Listen for Test Event" or execute workflow manually
- **Availability**: Only while workflow is NOT active
- **Display**: Shows incoming data in the workflow UI
- **Use case**: Development, debugging, testing webhook payloads

**Pattern**: `https://<domain>/webhook-test/<path>`

#### **Production URL**
- **Registration**: Created when workflow is ACTIVATED
- **Availability**: Permanent while workflow is active
- **Display**: Does NOT show data in UI (runs silently)
- **Use case**: Production integrations, live webhooks

**Pattern**: `https://<domain>/webhook/<path>`

**Toggle**: Click "Test URL" or "Production URL" at top of node panel to see respective URLs.

### URL Path Configuration

**Default**: Randomly generated path (e.g., `/a1b2c3d4-e5f6-7890-abcd-ef1234567890`)

**Custom Path**:
- Manually specify any path (e.g., `/my-webhook`, `/orders/created`)
- **Supports route parameters**: `/orders/:orderId/update`

**Best practice**: Use descriptive paths for production webhooks.

### HTTP Methods

Supported methods:
- `GET` - Retrieve data (query parameters)
- `POST` - Submit data (body + headers)
- `PUT` - Update data
- `PATCH` - Partial update
- `DELETE` - Remove data
- `HEAD` - Headers only
- `OPTIONS` - CORS preflight

### Authentication Options

#### 1. **None**
- Open webhook, no authentication
- ⚠️ **Security risk** for sensitive data

#### 2. **Basic Auth**
- Username + Password validation
- HTTP Basic Authentication scheme

#### 3. **Header Auth**
- Check for static token in request header
- Example: `X-API-Key: your-secret-token`
- **Best for**: API integrations with custom headers

#### 4. **JWT Auth**
- Validate signed JSON Web Token
- Supports RS256, HS256 algorithms
- **Best for**: OAuth flows, modern auth

### Headers Configuration

**Response Headers**:
Add custom headers to webhook responses (e.g., `Content-Type`, `Cache-Control`, `Access-Control-Allow-Origin`).

**Reference**: [MDN Response Headers](https://developer.mozilla.org/en-US/docs/Glossary/Response_header)

### CORS Configuration

**Allowed Origins**:
- Default: `*` (allow all origins)
- Specify: Comma-separated list of allowed domains
- Example: `https://example.com,https://app.example.com`

**Use case**: Control which web apps can call your webhook from browsers.

### IP Whitelist

**IP(s) Whitelist**:
- Limit webhook invocations to specific IPs
- Comma-separated list: `192.168.1.1,10.0.0.5`
- **Security benefit**: Prevent unauthorized webhook calls

### Response Modes

**Options**:
1. **On Workflow Completion**: Wait for entire workflow to finish
2. **Last Node**: Respond immediately with last node output
3. **Webhook Response Node**: Use dedicated "Respond to Webhook" node for custom response

**Best practice**: Use "Respond to Webhook" node for complex workflows to avoid timeouts.

### Best Practices

1. **Use Production URLs** for live integrations
2. **Enable authentication** (Header Auth or JWT recommended)
3. **Set IP whitelist** when source IPs are known
4. **Configure CORS** appropriately for web apps
5. **Use custom paths** for clarity and organization
6. **Test with Test URL** before activating workflow
7. **Handle errors** - webhook should respond even on failure
8. **Log incoming data** for debugging

**Reference**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/

---

## 5. AI Agents & LangChain Integration

### Overview

n8n provides comprehensive AI Agent capabilities through LangChain integration, enabling autonomous workflows powered by AI that can make decisions, interact with apps, and execute tasks.

### Agent Types

#### 1. **Conversational Agent**

**Purpose**: Optimized for conversation and ongoing dialogue

**Key Features**:
- **Memory support**: Can recall previous prompts and maintain context
- **Chat interface**: Works with Chat Trigger node
- **Use cases**: Chatbots, customer support, interactive assistants

**Configuration**:
- Attach memory sub-node (Simple Memory, MongoDB, Redis, Postgres, Zep)
- Connect to chat model (OpenAI, Anthropic, Google Gemini, etc.)
- Add tools for extended capabilities

**Example workflow**:
```
Chat Trigger → Conversational Agent → Tools → Respond to Chat
                    ↓
               Simple Memory
```

#### 2. **Tools Agent**

**Purpose**: Implements LangChain's tool calling interface

**Key Features**:
- **Tool schema description**: Describes available tools automatically
- **Improved output parsing**: Passes parser to model as formatting tool
- **Flexible tool integration**: Connect any n8n tool or custom code tool

**Use cases**: Task automation, API orchestration, multi-tool workflows

**Configuration**:
- Connect chat model
- Add tools (Calculator, Wikipedia, Wolfram, Custom Code, MCP Client, etc.)
- Configure output parser if needed

#### 3. **ReAct Agent**

**Purpose**: Reasoning and Acting framework

**Key Features**:
- **Automatic tool listing**: LangChain adds tools list automatically
- **No memory support**: Cannot recall previous prompts
- **Single-shot execution**: Best for one-time tasks

**Limitations**:
- ❌ Does NOT support memory sub-nodes
- ❌ Cannot simulate ongoing conversations

**Use cases**: Single-query analysis, fact-checking, one-off automations

**Reference**: [LangChain ReAct Documentation](https://python.langchain.com/docs/modules/agents/agent_types/react)

### Additional Agent Types (Specialized)

#### 4. **OpenAI Functions Agent**
- Leverages OpenAI's function calling capabilities
- Native integration with OpenAI models
- Best for OpenAI-specific workflows

#### 5. **Plan and Execute Agent**
- Strategic task decomposition
- Plans then executes step-by-step
- Best for complex multi-step tasks

#### 6. **SQL Agent**
- Database query generation and execution
- Natural language to SQL conversion
- Best for data analysis and reporting

### LangChain Components Integration

#### **Chat Models** (LLM providers):
- OpenAI (GPT-3.5, GPT-4, GPT-4 Turbo)
- Anthropic (Claude 3 Opus, Sonnet, Haiku)
- Google Gemini
- Azure OpenAI
- Mistral Cloud
- Groq
- Cohere
- DeepSeek
- Ollama (self-hosted)
- OpenRouter

#### **Memory Types**:
- **Simple Memory**: In-workflow memory (session-based)
- **MongoDB Chat Memory**: Persistent, scalable
- **Redis Chat Memory**: Fast, ephemeral
- **Postgres Chat Memory**: Persistent, relational
- **Zep**: Purpose-built for conversational AI
- **Xata**: Cloud-native memory
- **Motorhead**: High-performance memory

#### **Tools** (agent capabilities):
- Calculator
- Wikipedia
- Wolfram|Alpha
- SerpApi (Google search)
- Custom Code Tool
- Call n8n Workflow Tool
- MCP Client Tool (see next section)
- Vector Store QA Tool

#### **Vector Stores** (for RAG):
- Pinecone
- Qdrant
- Weaviate
- Supabase
- PGVector (Postgres)
- MongoDB Atlas
- Redis
- Milvus
- Simple Vector Store (in-memory)
- Zep

#### **Embeddings Models**:
- OpenAI
- Azure OpenAI
- Cohere
- Google Gemini
- Google PaLM
- Google Vertex AI
- HuggingFace Inference
- Mistral Cloud
- Ollama
- AWS Bedrock

#### **Text Processing**:
- Character Text Splitter
- Recursive Character Text Splitter
- Token Splitter

### AI Agent Workflow Patterns

**Pattern 1: Simple Conversational Bot**
```
Chat Trigger → Conversational Agent + Simple Memory → Respond to Chat
```

**Pattern 2: Tools-Augmented Agent**
```
Manual Trigger → Tools Agent → [Wikipedia + Calculator + Custom Code Tool] → Output
```

**Pattern 3: RAG-Powered Agent**
```
Webhook → ReAct Agent → Vector Store Retriever → LLM → Response
```

**Pattern 4: Multi-Agent System**
```
Chat Trigger → Plan and Execute Agent → [SQL Agent + Tools Agent] → Synthesize → Respond
```

### Best Practices

1. **Choose the right agent type**:
   - Conversational → chatbots, ongoing dialogue
   - Tools → multi-tool orchestration
   - ReAct → single-shot reasoning

2. **Memory selection**:
   - Development → Simple Memory
   - Production → Redis/Postgres/Zep

3. **Tool configuration**:
   - Provide clear tool descriptions
   - Limit tools to what's necessary (reduces token usage)
   - Test tools individually before adding to agent

4. **Model selection**:
   - GPT-4 → complex reasoning, best quality
   - GPT-3.5 → fast, cost-effective
   - Claude 3 Sonnet → balance of speed and quality
   - Ollama → privacy, self-hosted

5. **Error handling**:
   - Implement timeout limits
   - Handle LLM API failures gracefully
   - Log agent decisions for debugging

**Reference**: https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/

---

## 6. Tool Workflows & MCP Integration

### Tool Workflows (Call n8n Workflow Tool)

**Purpose**: Create reusable workflows that AI agents can call as tools.

**Key Concept**: Turn ANY n8n workflow into an AI agent tool by using the "Call n8n Workflow Tool" node.

#### Configuration

**Parameters**:
1. **Description**: Define what the tool does (critical - LLM reads this)
2. **Source**: Specify which workflow to call
3. **Workflow Inputs**: Map data passed from agent to workflow

**Example**:
```
AI Agent → Call n8n Workflow Tool
              ↓
          [Separate Workflow: "Get Customer Data"]
              ↓
          Returns customer JSON to agent
```

#### Best Practices

1. **Clear descriptions**: LLM decides when to use tool based on description
2. **Single responsibility**: Each tool workflow does ONE thing well
3. **Input validation**: Validate inputs in the called workflow
4. **Error handling**: Return meaningful errors to agent
5. **Modular design**: Build library of reusable tool workflows

**Use cases**:
- Database queries
- API integrations
- Complex calculations
- Data transformations
- External system interactions

### MCP (Model Context Protocol) Integration

#### Overview

**MCP** = Model Context Protocol - enables seamless integration between LLMs and external tools/data sources in a standardized way.

**n8n's MCP Capabilities**:
1. **MCP Client** (consume external MCP servers)
2. **MCP Server** (expose n8n workflows as MCP tools)

#### MCP Client Tool Node

**Purpose**: Connect AI agents to external MCP servers and use their exposed tools.

**Configuration**:

1. **SSE Endpoint**: URL of the MCP server (Server-Sent Events)
   - Example: `https://mcp-server.example.com/sse`

2. **Authentication**:
   - **Bearer Token**: `Authorization: Bearer <token>`
   - **Header Auth**: Custom header authentication

3. **Tool Selection**:
   - **All**: Expose all tools from MCP server
   - **Selected**: Choose specific tools to make available

**Architecture**:
```
AI Agent → MCP Client Tool → [External MCP Server] → Tools/Resources
```

**Example workflow**:
```
Chat Trigger → Tools Agent → MCP Client Tool (pointing to external MCP server)
                                    ↓
                              [External tools: file_search, code_execution, etc.]
```

#### MCP Server Trigger Node

**Purpose**: Make n8n workflows available to external MCP clients (like Claude Desktop, Claude Code, Cursor, Windsurf).

**Configuration**:
- Exposes n8n workflows as MCP tools
- External MCP clients can discover and call your n8n workflows
- Bidirectional integration: n8n ↔ AI assistants

**Architecture**:
```
External MCP Client (Claude Code) → n8n MCP Server Trigger → n8n Workflow
```

**Use cases**:
- Expose n8n automation to AI coding assistants
- Let Claude Code/Cursor call your workflows
- Create custom AI tools backed by n8n logic

#### Community MCP Node

**GitHub**: [nerding-io/n8n-nodes-mcp](https://github.com/nerding-io/n8n-nodes-mcp)

**Additional capabilities**:
- Interact with MCP servers in workflows
- Access MCP resources
- Execute MCP tools
- Use MCP prompts

**Installation**: Community node (install via n8n community nodes)

### MCP Integration Patterns

**Pattern 1: External Tools via MCP**
```
AI Agent → MCP Client Tool → External MCP Server (Perplexity, file system, etc.)
```

**Pattern 2: n8n as MCP Server**
```
Claude Desktop → n8n MCP Server Trigger → n8n Workflow (database query, API call, etc.)
```

**Pattern 3: Hybrid**
```
Claude Code → n8n MCP Server → Workflow → MCP Client Tool → External MCP
```

### Best Practices

1. **MCP Client**:
   - Test SSE endpoint before workflow execution
   - Use Bearer auth for production
   - Select specific tools (not "All") for clarity

2. **MCP Server**:
   - Provide clear tool descriptions
   - Validate inputs from external clients
   - Handle errors gracefully
   - Log MCP tool calls for debugging

3. **Security**:
   - Use authentication for all MCP endpoints
   - Whitelist allowed clients
   - Validate all inputs from MCP clients

**Reference**: https://docs.n8n.io/integrations/builtin/cluster-nodes/sub-nodes/n8n-nodes-langchain.toolmcp/

---

## 7. REST API Endpoints

### Overview

n8n provides a public REST API for programmatically managing workflows, executions, and credentials.

**Base URL Pattern**: `https://<your-n8n-domain>/api/v1/`

**Authentication**: API Key (Bearer token in Authorization header)

### API Endpoint Categories

#### 1. **Workflows**

**Base endpoint**: `/api/v1/workflows`

**Operations**:

**GET /api/v1/workflows**
- List all workflows
- Returns: Array of workflow objects

**GET /api/v1/workflows/:id**
- Get specific workflow by ID
- Returns: Complete workflow JSON

**POST /api/v1/workflows**
- Create new workflow
- Body: Workflow JSON
- Returns: Created workflow with ID

**PUT /api/v1/workflows/:id**
- Update existing workflow
- Body: Complete workflow JSON
- Returns: Updated workflow

**DELETE /api/v1/workflows/:id**
- Delete workflow
- Returns: Success confirmation

**PUT /api/v1/workflows/:id/activate**
- Activate workflow
- Returns: Activated workflow

**PUT /api/v1/workflows/:id/deactivate**
- Deactivate workflow
- Returns: Deactivated workflow

#### 2. **Executions**

**Base endpoint**: `/api/v1/executions`

**Operations**:

**GET /api/v1/executions**
- List workflow executions
- Query parameters: `workflowId`, `status`, `limit`
- Returns: Array of execution records

**GET /api/v1/executions/:id**
- Get specific execution details
- Returns: Complete execution data, logs, output

**DELETE /api/v1/executions/:id**
- Delete execution record
- Returns: Success confirmation

**Use cases**:
- Custom monitoring dashboards
- Execution analytics
- Debugging and troubleshooting
- Automated reporting

#### 3. **Credentials**

**Base endpoint**: `/api/v1/credentials`

**Operations**:

**GET /api/v1/credentials**
- List all credentials (names only, not values)
- Returns: Array of credential metadata

**Note**: For security, credential VALUES are NOT returned via API.

#### 4. **Tags**

**Base endpoint**: `/api/v1/tags`

**Operations**:
- Manage workflow tags
- Organize workflows programmatically

### Using the n8n Node

**Alternative to direct API calls**: Use the built-in **n8n** node

**Available operations**:
- Workflow management (get, create, update, delete, activate)
- Execution management (list, get)
- Credential listing

**Advantages**:
- No need to manage authentication manually
- Built-in error handling
- Visual workflow integration

**Reference**: https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.n8n/

### Authentication

**API Key Setup**:
1. Go to n8n Settings → API
2. Generate API key
3. Copy key (shown only once!)

**Usage**:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://your-n8n-domain/api/v1/workflows
```

**In n8n HTTP Request node**:
- Authentication: Bearer Token
- Token: Your API key

### Example: Deploy Workflow via API

**HTTP Request (POST)**:
```json
POST https://auto.mhms.fr/api/v1/workflows
Headers: {
  "Authorization": "Bearer YOUR_API_KEY",
  "Content-Type": "application/json"
}
Body: {
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...},
  "active": false
}
```

### Best Practices

1. **Store API keys securely**: Use environment variables or credential system
2. **Use n8n node when possible**: Simpler than direct API calls
3. **Handle errors**: API returns standard HTTP status codes
4. **Paginate results**: Use `limit` parameter for large result sets
5. **Monitor API usage**: Track API calls for rate limiting
6. **Version control**: Export workflow JSON before updates

**Reference**: https://docs.n8n.io/api/api-reference/

---

## 8. Error Handling Patterns

### Core Error Handling Mechanisms

#### 1. **Error Trigger Node**

**Purpose**: Create dedicated error workflows that run when ANY workflow fails.

**Setup**:
1. Create a new workflow starting with **Error Trigger** node
2. In the original workflow: **Settings** → **Error Workflow** → Select error workflow
3. Error workflow runs automatically on any execution failure

**Data Available**:
```javascript
{
  "execution": {
    "id": "execution-id",
    "mode": "manual",
    "error": {
      "message": "Error description",
      "stack": "Error stack trace"
    }
  },
  "workflow": {
    "id": "workflow-id",
    "name": "Workflow Name"
  }
}
```

**Best practice**: ONE centralized error workflow per n8n instance

**Example error workflow**:
```
Error Trigger → Parse Error → Send Slack Notification → Log to Google Sheets
```

#### 2. **Continue on Fail**

**Purpose**: Allow workflow to continue even when a node fails.

**Settings** (per node):
- **Stop on Fail** (default): Workflow halts on error
- **Continue on Fail**: Workflow skips failed node and continues

**When enabled**:
- Node exposes **error output** (red connector)
- Can route failures to different path
- Useful for non-critical operations

**Example**:
```
HTTP Request (Continue on Fail enabled)
    ↓ success (green)          ↓ error (red)
  Process Data            Send Error Alert
```

**Use cases**:
- Optional API calls
- Fallback mechanisms
- Graceful degradation

#### 3. **Retry on Fail**

**Purpose**: Automatically retry failed nodes (especially for flaky APIs).

**Configuration** (per node):
- **Max Retry Attempts**: 1-5 (typically 3)
- **Retry Interval**: Time between retries (seconds)

**Retry behavior**:
- Exponential backoff (recommended)
- Fixed interval
- Stops after max attempts

**Best for**:
- Network requests
- External API calls
- Temporary service outages

**Example settings**:
```
Max Retries: 3
Wait Between Retries: 5 seconds
```

### Error Handling Patterns

#### Pattern 1: Centralized Error Workflow

**Setup**:
```
[System] Error Handler
    ↓
Error Trigger → Parse Error Details → Branch by Error Type
                                           ↓
                    ┌─────────────────────┼──────────────────────┐
                    ↓                     ↓                      ↓
              Critical Error        API Failure         Timeout Error
                    ↓                     ↓                      ↓
            PagerDuty Alert      Retry Queue          Log & Continue
```

**Benefits**:
- Single point of error management
- Consistent error handling across all workflows
- Easy to update error handling logic

#### Pattern 2: Error Output Branching

**Setup**:
```
Gmail Node (Continue on Fail)
    ↓ success               ↓ error
Process Emails      Fallback: Use IMAP
```

**Benefits**:
- Graceful fallback mechanisms
- Service redundancy
- Improved reliability

#### Pattern 3: Retry with Escalation

**Setup**:
```
HTTP Request (Max Retries: 3)
    ↓ success               ↓ error (after 3 retries)
  Process Data          Send Admin Alert
```

**Benefits**:
- Automatic recovery from temporary issues
- Human intervention only when necessary
- Reduced manual monitoring

#### Pattern 4: Logging & Monitoring

**Setup**:
```
Error Trigger → Extract Error Info → Branch
                                       ↓
                    ┌──────────────────┼──────────────────┐
                    ↓                  ↓                  ↓
            Google Sheets          Slack Alert       Update Status Page
            (Error Log)            (Team Notification)
```

**Data to log**:
- Timestamp
- Workflow name & ID
- Execution ID
- Error message
- Error stack trace
- Node name that failed
- Input data (if safe)

**Benefits**:
- Complete error history
- Pattern analysis
- Root cause identification
- Compliance/audit trail

### Best Practices Summary

#### Node-Level Settings

1. **Enable retries** for external API calls (3-5 attempts)
2. **Use Continue on Fail** for optional operations
3. **Set appropriate timeouts** to avoid hanging workflows
4. **Log errors locally** before escalating

#### Workflow-Level Settings

1. **Assign error workflow** to all production workflows
2. **Use descriptive workflow names** for error identification
3. **Tag workflows** for categorization (critical, non-critical)
4. **Test error handling** explicitly (force failures)

#### System-Level Practices

1. **Centralized error workflow**: Single error handler for all workflows
2. **Tiered alerting**:
   - Critical → PagerDuty/SMS
   - Important → Slack/Email
   - Minor → Log only
3. **Error analytics**: Track error rates, patterns, root causes
4. **Regular reviews**: Analyze error logs weekly/monthly
5. **Documentation**: Document common errors and resolutions

### Error Response Patterns

**HTTP Webhook Errors**:
```
Webhook → Try Main Process → On Error: Return 500 with error message
```

**Async Errors**:
```
Error Trigger → Log Error → Send Notification (no blocking)
```

**User-Facing Errors**:
```
Error → Format User-Friendly Message → Respond to Chat/Webhook
```

### Common Issues to Handle

1. **API Rate Limits**: Implement retry with exponential backoff
2. **Network Timeouts**: Set appropriate timeout values + retries
3. **Authentication Failures**: Refresh tokens, re-authenticate
4. **Data Validation**: Validate inputs before processing
5. **Resource Limits**: Handle out-of-memory, quota exceeded

### Monitoring & Alerting

**Key Metrics to Track**:
- Error rate (errors / total executions)
- Error types distribution
- Mean time to resolution (MTTR)
- Workflow-specific error rates
- Node-specific failure rates

**Alerting Triggers**:
- Error rate > threshold (e.g., 5%)
- Consecutive failures (e.g., 3 in a row)
- Critical workflow failures (immediate alert)
- New error types (investigate)

**Reference**: https://docs.n8n.io/flow-logic/error-handling/

---

## 9. Best Practices Summary

### Workflow Design

1. **Modularity**: Break complex workflows into smaller, reusable tool workflows
2. **Error Handling**: Always configure error workflows and retry logic
3. **Testing**: Use test webhooks and manual triggers before production
4. **Documentation**: Use Sticky Notes to document complex logic
5. **Naming**: Use clear, descriptive names for workflows and nodes

### Code & Expressions

1. **Prefer built-in nodes** over custom code when possible
2. **Use expressions for simple logic**, Code node for complex transformations
3. **Handle missing data** with optional chaining and defaults
4. **Test expressions** in the expressions editor before deployment
5. **Comment complex code** for maintainability

### Security

1. **Use credential system** - never hardcode secrets
2. **Enable webhook authentication** for production webhooks
3. **IP whitelist** when source IPs are known
4. **Validate inputs** from external sources
5. **Store API keys securely** in environment variables

### Performance

1. **Batch operations** when possible (process multiple items at once)
2. **Limit retries** to avoid infinite loops
3. **Set timeouts** to prevent hanging workflows
4. **Use pagination** for large datasets
5. **Monitor execution times** and optimize slow workflows

### AI Agent Best Practices

1. **Choose appropriate agent type** for use case
2. **Limit tools** to reduce token usage and improve decision-making
3. **Provide clear tool descriptions** for LLM understanding
4. **Use memory** for conversational agents
5. **Test with different prompts** to ensure robust behavior

### API & Integration

1. **Use n8n node** instead of direct API calls when available
2. **Handle rate limits** with retries and backoff
3. **Log API calls** for debugging and monitoring
4. **Version control workflows** with Git integration
5. **Test integrations** in non-production environment first

### Deployment

1. **Use version control** (Git) for workflow changes
2. **Test in staging** before production deployment
3. **Gradual rollout** for critical workflows
4. **Monitor executions** after deployment
5. **Have rollback plan** for failed deployments

### Maintenance

1. **Regular reviews** of error logs and execution data
2. **Update credentials** before expiry
3. **Archive unused workflows** to reduce clutter
4. **Document changes** in workflow settings or Git commits
5. **Keep n8n updated** to latest stable version

---

## Additional Resources

### Official Documentation
- **Main Docs**: https://docs.n8n.io/
- **API Reference**: https://docs.n8n.io/api/api-reference/
- **Community Forum**: https://community.n8n.io/
- **GitHub**: https://github.com/n8n-io/n8n

### Learning Resources
- **n8n Academy**: Courses and tutorials
- **Workflow Templates**: https://n8n.io/workflows/
- **YouTube Channel**: Official n8n tutorials
- **Blog**: https://blog.n8n.io/

### Community Resources
- **n8n Arena**: Community leaderboard and guides
- **Discord**: Community chat
- **Stack Overflow**: n8n tag

---

## Document Metadata

**Created**: 2025-01-01
**Research Sources**:
- Official n8n documentation (docs.n8n.io)
- n8n Community forums
- n8n Blog articles
- Community tutorials and guides

**Topics Covered**:
- ✅ Code Node JavaScript capabilities
- ✅ Expression system & built-in variables
- ✅ HTTP Request authentication methods
- ✅ Webhook configuration (test/production URLs, auth)
- ✅ AI Agent types (Conversational, Tools, ReAct)
- ✅ LangChain integration (chat models, memory, tools)
- ✅ Tool Workflows & MCP Client/Server
- ✅ REST API endpoints (workflows, executions, credentials)
- ✅ Error handling patterns (Error Trigger, Continue on Fail, Retry)
- ✅ Best practices across all domains

**Confidence Level**: High
**Last Updated**: 2025-01-01

---

**End of Document**
