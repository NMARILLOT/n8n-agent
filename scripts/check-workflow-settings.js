const https = require('https');
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '..', '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
const apiKey = envContent.match(/N8N_API_KEY=(.+)/)?.[1]?.trim();

const workflowId = process.argv[2] || 'UE65UccwntrhYzKp';

console.log(`🔍 Vérification du workflow ${workflowId}\n`);

const options = {
  hostname: 'auto.mhms.fr',
  path: `/api/v1/workflows/${workflowId}`,
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
      const wf = JSON.parse(data);

      console.log('📋 Workflow:', wf.name);
      console.log('🆔 ID:', wf.id);
      console.log('🔄 Active:', wf.active);
      console.log('');
      console.log('⚙️  SETTINGS:');
      console.log(JSON.stringify(wf.settings, null, 2));
      console.log('');

      if (wf.settings?.errorWorkflow) {
        console.log('✅ errorWorkflow assigné:', wf.settings.errorWorkflow);
      } else {
        console.log('❌ PAS de errorWorkflow assigné!');
        console.log('');
        console.log('💡 SOLUTION:');
        console.log(`   1. Va sur: https://auto.mhms.fr/workflow/${workflowId}`);
        console.log('   2. Settings (⚙️) → Error Workflow');
        console.log('   3. Sélectionne "Global Error Handler"');
        console.log('   4. Save');
      }

    } catch (e) {
      console.error('❌ Erreur:', e.message);
      console.error('Response:', data.substring(0, 200));
    }
  });
}).end();
