#!/usr/bin/env node
const https = require('https');

const workflowId = process.argv[2] || '6eWT5tM5D4dhaeK1';
const apiKey = process.env.N8N_API_KEY;

const options = {
  hostname: 'auto.mhms.fr',
  path: `/api/v1/workflows/${workflowId}`,
  method: 'GET',
  headers: {
    'X-N8N-API-KEY': apiKey
  }
};

const req = https.request(options, (res) => {
  let data = '';
  res.on('data', (chunk) => data += chunk);
  res.on('end', () => {
    const workflow = JSON.parse(data);
    console.log(JSON.stringify(workflow, null, 2));
  });
});

req.on('error', (error) => {
  console.error('Error:', error);
});

req.end();
