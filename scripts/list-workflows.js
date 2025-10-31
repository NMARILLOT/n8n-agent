#!/usr/bin/env node

/**
 * List all workflows from n8n instance
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Load .env file
const envPath = path.join(__dirname, '..', '.env');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  envContent.split('\n').forEach(line => {
    const match = line.match(/^([^=:#]+)=(.*)$/);
    if (match) {
      const key = match[1].trim();
      const value = match[2].trim();
      process.env[key] = value;
    }
  });
}

const apiKey = process.env.N8N_API_KEY;
const host = process.env.N8N_HOST || 'https://auto.mhms.fr';
const hostname = new URL(host).hostname;

if (!apiKey) {
  console.error('❌ Error: N8N_API_KEY not found in .env file');
  process.exit(1);
}

const options = {
  hostname: hostname,
  port: 443,
  path: '/api/v1/workflows',
  method: 'GET',
  headers: {
    'X-N8N-API-KEY': apiKey,
    'Accept': 'application/json'
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => { data += chunk; });
  res.on('end', () => {
    try {
      const result = JSON.parse(data);

      console.log('═══════════════════════════════════════════════════');
      console.log(`📋 Workflows on ${host}`);
      console.log('═══════════════════════════════════════════════════');
      console.log('');
      console.log(`Total workflows: ${result.data.length}`);
      console.log('');

      // Group by active status
      const active = result.data.filter(w => w.active);
      const paused = result.data.filter(w => !w.active);

      if (active.length > 0) {
        console.log('✅ ACTIVE WORKFLOWS (' + active.length + ')');
        console.log('─'.repeat(50));
        active
          .sort((a, b) => a.name.localeCompare(b.name))
          .forEach((w, i) => {
            console.log(`${String(i + 1).padStart(2, ' ')}. ${w.name}`);
            console.log(`    ID: ${w.id}`);
            if (w.tags && w.tags.length > 0) {
              console.log(`    Tags: ${w.tags.map(t => t.name).join(', ')}`);
            }
            console.log('');
          });
      }

      if (paused.length > 0) {
        console.log('⏸️  PAUSED WORKFLOWS (' + paused.length + ')');
        console.log('─'.repeat(50));
        paused
          .sort((a, b) => a.name.localeCompare(b.name))
          .forEach((w, i) => {
            console.log(`${String(i + 1).padStart(2, ' ')}. ${w.name}`);
            console.log(`    ID: ${w.id}`);
            if (w.tags && w.tags.length > 0) {
              console.log(`    Tags: ${w.tags.map(t => t.name).join(', ')}`);
            }
            console.log('');
          });
      }

      console.log('═══════════════════════════════════════════════════');

    } catch (error) {
      console.error('❌ Failed to parse response:', error.message);
      console.error('Response:', data);
      process.exit(1);
    }
  });
});

req.on('error', (error) => {
  console.error('❌ Request failed:', error.message);
  process.exit(1);
});

req.end();
