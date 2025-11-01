const https = require('https');
const fs = require('fs');
const path = require('path');

// Read .env file manually
const envPath = path.join(__dirname, '..', '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
const apiKey = envContent.match(/N8N_API_KEY=(.+)/)[1].trim();
const workflowId = '2YHssdr9SHK0iKeP'; // Global Error Handler

// Get workflow to check if active
const options = {
  hostname: 'auto.mhms.fr',
  path: `/api/v1/workflows/${workflowId}`,
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  }
};

console.log('🔍 Vérification du Global Error Handler...\n');

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    try {
      const workflow = JSON.parse(data);
      console.log('📋 Workflow:', workflow.name);
      console.log('🔄 Active:', workflow.active ? '✅ OUI' : '❌ NON');
      console.log('🆔 ID:', workflow.id);

      if (!workflow.active) {
        console.log('\n⚠️  PROBLÈME: Le workflow d\'erreur n\'est PAS activé!');
        console.log('');
        console.log('📝 SOLUTION:');
        console.log('   1. Va sur https://auto.mhms.fr/workflow/2YHssdr9SHK0iKeP');
        console.log('   2. Clique sur le toggle en haut à droite pour l\'activer');
        console.log('   3. Vérifie que l\'indicateur devient vert');
        console.log('');
      } else {
        console.log('\n✅ Le workflow d\'erreur est bien activé');
        console.log('');
        console.log('🔍 Vérifie aussi:');
        console.log('   - Le workflow de test a bien errorWorkflow assigné');
        console.log('   - L\'erreur s\'est bien produite (vérifier les executions)');
      }
    } catch (e) {
      console.error('❌ Erreur:', e.message);
      console.error('Response:', data);
    }
  });
});

req.on('error', (e) => {
  console.error('❌ Erreur requête:', e.message);
});

req.end();
