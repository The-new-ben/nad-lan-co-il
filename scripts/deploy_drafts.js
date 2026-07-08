const fs = require('fs');
const path = require('path');

// Credentials
const WP_USER = 'nadlvzld_admin';
const WP_APP_PASSWORD = 'A0Fv r6l8 wj1Q syhH NXtG lKE6';
const WP_REST_BASE = 'https://nad-lan.co.il/wp-json/wp/v2';
const authHeader = 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASSWORD}`).toString('base64');

const MOCKUPS_DIR = path.join(__dirname, '..', 'draft-mockups');

async function getPageByTitle(title) {
  const url = `${WP_REST_BASE}/pages?search=${encodeURIComponent(title)}&status=any`;
  const response = await fetch(url, {
    headers: { 'Authorization': authHeader }
  });
  if (!response.ok) return null;
  const pages = await response.json();
  return pages.find(p => p.title.rendered === title);
}

async function deployDraft(title, content) {
  const existingPage = await getPageByTitle(title);
  
  const payload = {
    title: title,
    content: content,
    status: 'draft',
    template: '' // Standard WP Page
  };
  
  let url = `${WP_REST_BASE}/pages`;
  let method = 'POST';
  
  if (existingPage) {
    url = `${WP_REST_BASE}/pages/${existingPage.id}`;
  }

  const response = await fetch(url, {
    method: method,
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorText = await response.text();
    console.error(`Error deploying ${title}: HTTP ${response.status} - ${errorText}`);
  } else {
    const result = await response.json();
    console.log(`Success: ${title} (ID: ${result.id}) -> ${result.link}`);
  }
}

async function main() {
  if (!fs.existsSync(MOCKUPS_DIR)) {
    console.error(`Mockups directory not found: ${MOCKUPS_DIR}`);
    return;
  }

  const files = fs.readdirSync(MOCKUPS_DIR).filter(f => f.endsWith('.html'));
  
  for (const file of files) {
    const content = fs.readFileSync(path.join(MOCKUPS_DIR, file), 'utf8');
    const basename = path.basename(file, '.html');
    const title = "Mockup: " + basename.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    
    console.log(`Deploying ${title}...`);
    await deployDraft(title, content);
  }
}

main();
