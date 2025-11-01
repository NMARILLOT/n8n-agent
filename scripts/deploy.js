#!/usr/bin/env node

/**
 * n8n Workflow Deployment Script
 *
 * Deploy local workflow JSON files to remote n8n instance
 * Usage: node scripts/deploy.js [workflow-folder]
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// Configuration
const config = {
  n8nHost: process.env.N8N_HOST || 'https://auto.mhms.fr',
  apiKey: process.env.N8N_API_KEY,
  workflowsDir: process.argv[2] || '.',
  dryRun: process.env.DRY_RUN === 'true'
};

// Validate configuration
if (!config.apiKey) {
  console.error('❌ Error: N8N_API_KEY environment variable is required');
  console.error('   Set it with: export N8N_API_KEY=your_api_key');
  process.exit(1);
}

/**
 * Make HTTP request to n8n API
 */
function apiRequest(method, endpoint, body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, config.n8nHost);
    const isHttps = url.protocol === 'https:';
    const httpLib = isHttps ? https : http;

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method: method,
      headers: {
        'X-N8N-API-KEY': config.apiKey,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    };

    const req = httpLib.request(options, (res) => {
      let data = '';

      res.on('data', (chunk) => {
        data += chunk;
      });

      res.on('end', () => {
        try {
          const parsed = data ? JSON.parse(data) : {};
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve(parsed);
          } else {
            reject(new Error(`API Error ${res.statusCode}: ${JSON.stringify(parsed)}`));
          }
        } catch (error) {
          reject(new Error(`Failed to parse response: ${error.message}`));
        }
      });
    });

    req.on('error', (error) => {
      reject(new Error(`Request failed: ${error.message}`));
    });

    if (body) {
      req.write(JSON.stringify(body));
    }

    req.end();
  });
}

/**
 * Get all workflows from remote n8n instance
 */
async function getRemoteWorkflows() {
  try {
    const response = await apiRequest('GET', '/api/v1/workflows');
    return response.data || [];
  } catch (error) {
    console.error('❌ Failed to fetch remote workflows:', error.message);
    return [];
  }
}

/**
 * Create a new workflow on remote n8n instance
 */
async function createWorkflow(workflowData) {
  return await apiRequest('POST', '/api/v1/workflows', workflowData);
}

/**
 * Get existing workflow from remote n8n instance
 */
async function getWorkflow(workflowId) {
  return await apiRequest('GET', `/api/v1/workflows/${workflowId}`);
}

/**
 * Update existing workflow on remote n8n instance
 */
async function updateWorkflow(workflowId, workflowData) {
  return await apiRequest('PUT', `/api/v1/workflows/${workflowId}`, workflowData);
}

/**
 * Find local workflow JSON files
 */
function findWorkflowFiles(dir) {
  const workflows = [];

  function scanDirectory(currentDir) {
    const entries = fs.readdirSync(currentDir, { withFileTypes: true });

    for (const entry of entries) {
      const fullPath = path.join(currentDir, entry.name);

      if (entry.isDirectory() && entry.name === 'workflow') {
        // Scan workflow directory
        const workflowFiles = fs.readdirSync(fullPath)
          .filter(file => file.endsWith('.json'))
          .map(file => path.join(fullPath, file));
        workflows.push(...workflowFiles);
      } else if (entry.isDirectory() && !entry.name.startsWith('.')) {
        // Recurse into subdirectories
        scanDirectory(fullPath);
      }
    }
  }

  scanDirectory(dir);
  return workflows;
}

/**
 * Load and validate workflow JSON
 */
function loadWorkflow(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const workflow = JSON.parse(content);

    // Validate required fields
    if (!workflow.name) {
      throw new Error('Workflow missing required field: name');
    }
    if (!workflow.nodes || !Array.isArray(workflow.nodes)) {
      throw new Error('Workflow missing required field: nodes');
    }

    return workflow;
  } catch (error) {
    throw new Error(`Failed to load ${filePath}: ${error.message}`);
  }
}

/**
 * Clean workflow data for API submission
 * Remove fields that are managed by n8n API
 */
function cleanWorkflowForAPI(workflow, isUpdate = false) {
  // Clean settings by removing fields not accepted by API
  const cleanedSettings = {};
  if (workflow.settings) {
    // Copy settings but exclude fields not supported by API
    const excludedSettingsFields = ['executionOrder', 'callerPolicy'];
    for (const [key, value] of Object.entries(workflow.settings)) {
      if (!excludedSettingsFields.includes(key)) {
        cleanedSettings[key] = value;
      }
    }
  }

  // Only keep fields accepted by the API
  const cleanedWorkflow = {
    name: workflow.name,
    nodes: workflow.nodes,
    connections: workflow.connections,
    settings: cleanedSettings
  };

  // Add 'active' field only for updates, not for creation (API rejects it)
  if (isUpdate && workflow.active !== undefined) {
    cleanedWorkflow.active = workflow.active;
  }

  // Add optional fields if they exist
  if (workflow.pinData) {
    cleanedWorkflow.pinData = workflow.pinData;
  }

  // Add staticData only if it exists and is not undefined
  if (workflow.staticData !== undefined) {
    cleanedWorkflow.staticData = workflow.staticData;
  }

  return cleanedWorkflow;
}

/**
 * Deploy a single workflow
 */
async function deployWorkflow(filePath, remoteWorkflows) {
  console.log(`\n📦 Processing: ${path.basename(filePath)}`);

  try {
    const localWorkflow = loadWorkflow(filePath);
    const workflowName = localWorkflow.name;

    // Check if workflow already exists on remote
    const existingWorkflow = remoteWorkflows.find(w => w.name === workflowName);
    const isUpdate = !!existingWorkflow;

    if (config.dryRun) {
      if (existingWorkflow) {
        console.log(`   🔄 Would update: ${workflowName} (ID: ${existingWorkflow.id})`);
      } else {
        console.log(`   ✨ Would create: ${workflowName}`);
      }
      return { success: true, action: 'dry-run' };
    }

    if (existingWorkflow) {
      // Update existing workflow
      console.log(`   🔄 Updating: ${workflowName} (ID: ${existingWorkflow.id})`);

      // Fetch the existing workflow from API to get the correct structure
      const remoteWorkflow = await getWorkflow(existingWorkflow.id);

      // Clean settings (exclude unsupported fields)
      const cleanedSettings = {};
      const excludedSettingsFields = ['executionOrder', 'callerPolicy'];

      // Start with remote settings
      if (remoteWorkflow.settings) {
        for (const [key, value] of Object.entries(remoteWorkflow.settings)) {
          if (!excludedSettingsFields.includes(key)) {
            cleanedSettings[key] = value;
          }
        }
      }

      // Override with local settings
      if (localWorkflow.settings) {
        for (const [key, value] of Object.entries(localWorkflow.settings)) {
          if (!excludedSettingsFields.includes(key)) {
            cleanedSettings[key] = value;
          }
        }
      }

      // Build update payload with ONLY accepted fields
      // Note: 'active' is read-only and managed separately
      const updateData = {
        name: localWorkflow.name,
        nodes: localWorkflow.nodes,
        connections: localWorkflow.connections,
        settings: cleanedSettings
      };

      // Add optional fields only if they exist and have content
      const localPinData = localWorkflow.pinData;
      const remotePinData = remoteWorkflow.pinData;
      const hasPinData = (localPinData && Object.keys(localPinData).length > 0) ||
                         (remotePinData && Object.keys(remotePinData).length > 0);

      if (hasPinData) {
        updateData.pinData = localPinData || remotePinData;
      }

      const localStaticData = localWorkflow.staticData;
      const remoteStaticData = remoteWorkflow.staticData;
      const hasStaticData = localStaticData !== undefined || remoteStaticData !== undefined;

      if (hasStaticData) {
        updateData.staticData = localStaticData !== undefined ? localStaticData : remoteStaticData;
      }

      // Debug: log the payload
      if (process.env.DEBUG) {
        console.log('   🐛 Payload keys:', JSON.stringify(Object.keys(updateData)));
        console.log('   🐛 Settings keys:', JSON.stringify(Object.keys(updateData.settings || {})));
      }

      await updateWorkflow(existingWorkflow.id, updateData);
      console.log(`   ✅ Updated successfully`);
      return { success: true, action: 'update', id: existingWorkflow.id };

    } else {
      // Create new workflow
      console.log(`   ✨ Creating: ${workflowName}`);

      // Clean workflow data for API
      const createData = cleanWorkflowForAPI(localWorkflow);

      const result = await createWorkflow(createData);
      console.log(`   ✅ Created successfully (ID: ${result.id})`);
      return { success: true, action: 'create', id: result.id };
    }

  } catch (error) {
    console.error(`   ❌ Failed: ${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * Main deployment function
 */
async function main() {
  console.log('🚀 n8n Workflow Deployment');
  console.log('═'.repeat(50));
  console.log(`📍 Target: ${config.n8nHost}`);
  console.log(`📁 Source: ${path.resolve(config.workflowsDir)}`);

  if (config.dryRun) {
    console.log('🔍 DRY RUN MODE - No changes will be made');
  }

  console.log('═'.repeat(50));

  // Find all workflow files
  console.log('\n🔍 Scanning for workflows...');
  const workflowFiles = findWorkflowFiles(config.workflowsDir);

  if (workflowFiles.length === 0) {
    console.log('⚠️  No workflow files found');
    return;
  }

  console.log(`   Found ${workflowFiles.length} workflow(s)`);

  // Get remote workflows
  console.log('\n🌐 Fetching remote workflows...');
  const remoteWorkflows = await getRemoteWorkflows();
  console.log(`   Found ${remoteWorkflows.length} remote workflow(s)`);

  // Deploy each workflow
  console.log('\n📤 Deploying workflows...');
  const results = [];

  for (const filePath of workflowFiles) {
    const result = await deployWorkflow(filePath, remoteWorkflows);
    results.push({ file: path.basename(filePath), ...result });
  }

  // Summary
  console.log('\n' + '═'.repeat(50));
  console.log('📊 Deployment Summary');
  console.log('═'.repeat(50));

  const successful = results.filter(r => r.success).length;
  const failed = results.filter(r => !r.success).length;
  const created = results.filter(r => r.action === 'create').length;
  const updated = results.filter(r => r.action === 'update').length;

  console.log(`✅ Successful: ${successful}/${results.length}`);
  console.log(`   📝 Created: ${created}`);
  console.log(`   🔄 Updated: ${updated}`);

  if (failed > 0) {
    console.log(`❌ Failed: ${failed}`);
    process.exit(1);
  }

  console.log('\n✨ Deployment completed successfully!');
}

// Run deployment
main().catch(error => {
  console.error('\n💥 Deployment failed:', error.message);
  process.exit(1);
});
