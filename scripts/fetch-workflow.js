const https = require('https');
const fs = require('fs');
const path = require('path');

const workflowName = process.argv[2];

if (!workflowName) {
  console.error('❌ Usage: node fetch-workflow.js "Workflow Name"');
  process.exit(1);
}

// Load API key from .env
const envPath = path.join(__dirname, '..', '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
const apiKey = envContent.match(/N8N_API_KEY=(.+)/)?.[1]?.trim();

if (!apiKey) {
  console.error('❌ N8N_API_KEY not found in .env');
  process.exit(1);
}

console.log(`🔍 Recherche du workflow: ${workflowName}\n`);

// Get all workflows
const options = {
  hostname: 'auto.mhms.fr',
  path: '/api/v1/workflows',
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }
};

https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    try {
      const result = JSON.parse(data);
      const workflow = result.data.find(w => w.name === workflowName);

      if (!workflow) {
        console.error(`❌ Workflow "${workflowName}" introuvable`);
        console.log('\n📋 Workflows disponibles:');
        result.data.forEach((w, i) => {
          console.log(`   ${i + 1}. ${w.name}`);
        });
        process.exit(1);
      }

      console.log('✅ Workflow trouvé:');
      console.log(`   ID: ${workflow.id}`);
      console.log(`   Active: ${workflow.active}`);
      console.log(`   Nodes: ${workflow.nodes.length}`);

      // Find the directory containing this workflow
      const findWorkflowFile = (dir) => {
        const items = fs.readdirSync(dir, { withFileTypes: true });

        for (const item of items) {
          const fullPath = path.join(dir, item.name);

          if (item.isDirectory() && item.name !== 'node_modules' && item.name !== '.git') {
            const result = findWorkflowFile(fullPath);
            if (result) return result;
          } else if (item.isFile() && item.name.endsWith('.json')) {
            try {
              const content = JSON.parse(fs.readFileSync(fullPath, 'utf8'));
              if (content.name === workflowName) {
                return fullPath;
              }
            } catch (e) {
              // Skip invalid JSON files
            }
          }
        }
        return null;
      };

      const localFile = findWorkflowFile(path.join(__dirname, '..'));

      if (localFile) {
        console.log(`\n📁 Fichier local: ${path.relative(path.join(__dirname, '..'), localFile)}`);

        // Backup local version
        const backupFile = localFile + '.backup';
        fs.copyFileSync(localFile, backupFile);
        console.log(`💾 Backup créé: ${path.basename(backupFile)}`);

        // Save remote version
        const cleanWorkflow = {
          name: workflow.name,
          nodes: workflow.nodes,
          connections: workflow.connections,
          settings: workflow.settings || {},
          staticData: workflow.staticData || null,
          pinData: workflow.pinData || {}
        };

        fs.writeFileSync(localFile, JSON.stringify(cleanWorkflow, null, 2) + '\n');
        console.log(`✅ Version n8n sauvegardée localement`);

        console.log(`\n⚠️  VÉRIFIER LES CHANGEMENTS:`);
        console.log(`   git diff "${path.relative(path.join(__dirname, '..'), localFile)}"`);

      } else {
        console.log('\n⚠️  Fichier local introuvable');
        console.log('   Le workflow existe dans n8n mais pas localement');
      }

    } catch (e) {
      console.error('❌ Erreur:', e.message);
      process.exit(1);
    }
  });
}).end();
