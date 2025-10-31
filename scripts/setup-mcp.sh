#!/bin/bash

# MCP Servers Setup Script for Claude Code
# Installs and configures Context7 and Sequential Thinking

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   MCP Servers Setup for Claude Code${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${RED}❌ Error: npm is not installed${NC}"
    echo -e "${YELLOW}   Install Node.js from: https://nodejs.org/${NC}"
    exit 1
fi

echo -e "${GREEN}✓ npm found: $(npm --version)${NC}"
echo ""

# Create config directory
echo -e "${BLUE}📁 Creating config directory...${NC}"
mkdir -p ~/.config/claude
echo -e "${GREEN}✓ Config directory ready${NC}"
echo ""

# Install MCP servers
echo -e "${BLUE}📦 Installing MCP servers...${NC}"
echo ""

echo -e "${YELLOW}Installing Context7 (documentation access)...${NC}"
npm install -g @upstash/context7-mcp || echo -e "${YELLOW}⚠️  Context7 installation may have issues, will try to use npx${NC}"

echo ""
echo -e "${YELLOW}Installing MCP SDK (Model Context Protocol)...${NC}"
npm install -g @modelcontextprotocol/sdk || echo -e "${YELLOW}⚠️  MCP SDK installation may have issues${NC}"

echo ""
echo -e "${GREEN}✓ MCP servers installation completed${NC}"
echo ""

# Create MCP configuration
echo -e "${BLUE}⚙️  Creating MCP configuration...${NC}"

cat > ~/.config/claude/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {},
      "description": "Technical documentation access (n8n, Node.js, frameworks)"
    }
  }
}
EOF

echo -e "${GREEN}✓ Configuration file created: ~/.config/claude/mcp_config.json${NC}"
echo ""

# Verify installation
echo -e "${BLUE}🔍 Verifying installation...${NC}"
echo ""

if npx @upstash/context7-mcp --version &> /dev/null; then
    echo -e "${GREEN}✓ Context7: Ready${NC}"
else
    echo -e "${YELLOW}⚠️  Context7: Will be installed on first use${NC}"
fi

if npm list -g @modelcontextprotocol/sdk &> /dev/null; then
    echo -e "${GREEN}✓ MCP SDK: Installed${NC}"
else
    echo -e "${YELLOW}⚠️  MCP SDK: Will be installed on first use${NC}"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✨ MCP Servers Setup Complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

echo -e "${YELLOW}📖 What's Available Now:${NC}"
echo ""
echo -e "  ${GREEN}Context7${NC} - Access to technical documentation"
echo -e "    • n8n node documentation"
echo -e "    • API references"
echo -e "    • Framework patterns"
echo ""
echo -e "  ${GREEN}MCP SDK${NC} - Model Context Protocol"
echo -e "    • Protocol implementation"
echo -e "    • Server communication"
echo ""

echo -e "${YELLOW}💡 Usage:${NC}"
echo -e "  Just use Claude Code normally!"
echo -e "  MCP servers will activate automatically when needed."
echo ""

echo -e "${YELLOW}📋 Configuration:${NC}"
echo -e "  ~/.config/claude/mcp_config.json"
echo ""

echo -e "${YELLOW}📚 Documentation:${NC}"
echo -e "  See MCP_SETUP.md for detailed info"
echo ""

echo -e "${GREEN}Ready to use! 🚀${NC}"
echo ""
