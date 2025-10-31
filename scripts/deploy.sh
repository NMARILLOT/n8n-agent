#!/bin/bash

# n8n Workflow Deployment Helper Script
# Makes it easier to deploy workflows

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if .env exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
  echo -e "${RED}❌ Error: .env file not found${NC}"
  echo -e "${YELLOW}💡 Copy .env.example to .env and fill in your N8N_API_KEY${NC}"
  echo ""
  echo "  cp .env.example .env"
  echo "  nano .env  # Edit and add your API key"
  echo ""
  exit 1
fi

# Load environment variables
source "$PROJECT_ROOT/.env"

# Export variables for child processes
export N8N_HOST
export N8N_API_KEY
export DRY_RUN

# Validate API key
if [ -z "$N8N_API_KEY" ]; then
  echo -e "${RED}❌ Error: N8N_API_KEY not set in .env file${NC}"
  exit 1
fi

# Display banner
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   n8n Workflow Deployment${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""

# Parse arguments
TARGET_DIR="$PROJECT_ROOT"

while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      export DRY_RUN=true
      echo -e "${YELLOW}🔍 DRY RUN MODE - No changes will be made${NC}"
      echo ""
      shift
      ;;
    --dir)
      TARGET_DIR="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: ./scripts/deploy.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --dry-run       Test deployment without making changes"
      echo "  --dir <path>    Deploy workflows from specific directory"
      echo "  --help, -h      Show this help message"
      echo ""
      echo "Examples:"
      echo "  ./scripts/deploy.sh                    # Deploy all workflows"
      echo "  ./scripts/deploy.sh --dry-run          # Test deployment"
      echo "  ./scripts/deploy.sh --dir \"Agent Telegram - Dev Nico Perso\""
      echo ""
      exit 0
      ;;
    *)
      echo -e "${RED}❌ Unknown option: $1${NC}"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

# Run deployment
echo -e "${GREEN}🚀 Starting deployment...${NC}"
echo ""

cd "$PROJECT_ROOT"
node "$SCRIPT_DIR/deploy.js" "$TARGET_DIR"

# Check exit status
if [ $? -eq 0 ]; then
  echo ""
  echo -e "${GREEN}✨ Deployment completed successfully!${NC}"
  exit 0
else
  echo ""
  echo -e "${RED}💥 Deployment failed${NC}"
  exit 1
fi
