const https = require('https');
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '..', '.env');
const envContent = fs.readFileSync(envPath, 'utf8');
const apiKey = envContent.match(/N8N_API_KEY=(.+)/)?.[1]?.trim();

const testWorkflowId = 'UE65UccwntrhYzKp'; // Test Error Handler
const errorWorkflowId = '2YHssdr9SHK0iKeP'; // Global Error Handler

console.log('🔍 DIAGNOSTIC COMPLET\n');
console.log('═══════════════════════════════════════\n');

// Check test workflow executions
function checkExecutions(workflowId, workflowName, callback) {
  const options = {
    hostname: 'auto.mhms.fr',
    path: `/api/v1/executions?workflowId=${workflowId}&limit=5`,
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
        callback(null, result.data || []);
      } catch (e) {
        callback(e, null);
      }
    });
  }).end();
}

// Step 1: Check test workflow
console.log('📋 ÉTAPE 1: Workflow de test');
console.log('─────────────────────────────────');
checkExecutions(testWorkflowId, 'Test Error Handler', (err, executions) => {
  if (err) {
    console.error('❌ Erreur:', err.message);
    return;
  }

  if (executions.length === 0) {
    console.log('❌ PROBLÈME: Aucune exécution trouvée!');
    console.log('');
    console.log('💡 SOLUTION:');
    console.log('   1. Va sur: https://auto.mhms.fr/workflow/UE65UccwntrhYzKp');
    console.log('   2. Clique sur "Test workflow" (bouton play en haut)');
    console.log('   3. Une erreur devrait apparaître (c\'est normal)');
    console.log('');
    return;
  }

  console.log(`✅ ${executions.length} exécution(s) trouvée(s)\n`);

  const lastExec = executions[0];
  console.log('Dernière exécution:');
  console.log(`   Date: ${new Date(lastExec.startedAt).toLocaleString()}`);
  console.log(`   Status: ${lastExec.finished ? (lastExec.status === 'error' ? '❌ ERROR' : '✅ SUCCESS') : '⏳ RUNNING'}`);
  console.log(`   Mode: ${lastExec.mode}`);

  if (lastExec.status === 'error') {
    console.log('   ✅ L\'erreur s\'est bien produite (attendu)');
  } else {
    console.log('   ⚠️  Pas d\'erreur détectée - le code ne génère peut-être pas d\'erreur');
  }

  console.log('');
  console.log('═══════════════════════════════════════\n');

  // Step 2: Check error workflow
  console.log('📋 ÉTAPE 2: Global Error Handler');
  console.log('─────────────────────────────────');

  checkExecutions(errorWorkflowId, 'Global Error Handler', (err, executions) => {
    if (err) {
      console.error('❌ Erreur:', err.message);
      return;
    }

    if (executions.length === 0) {
      console.log('❌ PROBLÈME: Global Error Handler jamais exécuté!');
      console.log('');
      console.log('💡 CAUSES POSSIBLES:');
      console.log('   1. errorWorkflow non assigné dans Settings');
      console.log('   2. Le workflow de test n\'a pas généré d\'erreur');
      console.log('   3. L\'erreur a été capturée par "Continue on Fail"');
      console.log('');
      console.log('🔧 VÉRIFICATION:');
      console.log('   - Va sur: https://auto.mhms.fr/workflow/UE65UccwntrhYzKp');
      console.log('   - Clique Settings (⚙️) → Error Workflow');
      console.log('   - Vérifie que "Global Error Handler" est sélectionné');
      console.log('');
      return;
    }

    console.log(`✅ ${executions.length} exécution(s) trouvée(s)\n`);

    executions.slice(0, 3).forEach((exec, i) => {
      console.log(`${i + 1}. Exécution du ${new Date(exec.startedAt).toLocaleString()}`);
      console.log(`   Status: ${exec.finished ? (exec.status === 'error' ? '❌ FAILED' : '✅ SUCCESS') : '⏳ RUNNING'}`);
      console.log(`   Mode: ${exec.mode}`);

      if (exec.status === 'error') {
        console.log('   ⚠️  ERROR: Le workflow d\'erreur a lui-même échoué!');
        console.log('   💡 CAUSE: Probablement credentials manquants (Google Sheets ou Telegram)');
      } else if (exec.finished && exec.status === 'success') {
        console.log('   ✅ Exécuté avec succès');
        console.log('   📱 Tu aurais dû recevoir une notification Telegram');
      }
      console.log('');
    });

    console.log('═══════════════════════════════════════\n');
    console.log('🔗 LIENS UTILES:');
    console.log('   Test workflow: https://auto.mhms.fr/workflow/UE65UccwntrhYzKp/executions');
    console.log('   Error Handler: https://auto.mhms.fr/workflow/2YHssdr9SHK0iKeP/executions');
    console.log('');
  });
});
