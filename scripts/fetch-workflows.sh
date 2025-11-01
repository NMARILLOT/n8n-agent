#!/bin/bash

# Fetch workflows from n8n before making changes
# Usage: ./scripts/fetch-workflows.sh [workflow_name]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Load environment
if [ -f "$PROJECT_ROOT/.env" ]; then
  export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

if [ -z "$N8N_API_KEY" ]; then
  echo "❌ N8N_API_KEY not found in .env"
  exit 1
fi

WORKFLOW_NAME="$1"

if [ -z "$WORKFLOW_NAME" ]; then
  echo "❌ Usage: ./scripts/fetch-workflows.sh \"Workflow Name\""
  exit 1
fi

echo "🔍 Fetching workflow: $WORKFLOW_NAME"

node "$SCRIPT_DIR/fetch-workflow.js" "$WORKFLOW_NAME"
