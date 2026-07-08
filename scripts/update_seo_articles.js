const fs = require('fs');
const marked = require('marked');

// Credentials
const WP_USER = 'nadlvzld_admin';
const WP_APP_PASSWORD = 'A0Fv r6l8 wj1Q syhH NXtG lKE6';
const WP_REST_BASE = 'https://nad-lan.co.il/wp-json/wp/v2';
const authHeader = 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASSWORD}`).toString('base64');

// Posts to update
const posts = [
  {
    id: 4945,
    path: 'C:\\Users\\pro\\nad-lan\\content\\guides\\buying-real-estate-israel-foreign-investor-2026.md'
  },
  {
    id: 4946,
    path: 'C:\\Users\\pro\\nad-lan\\docs\\seo-content\\2026-07-foreign-investor-guide.md'
  }
];

async function updatePost(postDef) {
  console.log(`Processing Post ID: ${postDef.id} from ${postDef.path}`);
  
  if (!fs.existsSync(postDef.path)) {
    console.error(`File not found: ${postDef.path}`);
    return;
  }
  
  let content = fs.readFileSync(postDef.path, 'utf8');
  
  // Extract body after frontmatter
  const match = content.match(/^(?:---\r?\n[\s\S]*?\r?\n---\r?\n)([\s\S]*)$/);
  if (!match) {
    console.error(`Could not parse frontmatter in ${postDef.path}`);
    return;
  }
  
  let markdownBody = match[1];

  // 1. Strip the leading H1 to avoid duplication
  markdownBody = markdownBody.replace(/^#\s+.*?[\r\n]+/m, '');
  
  // 2. Apply Copywriting rules: Remove em-dashes
  markdownBody = markdownBody
    .replace(/ — /g, ' - ')
    .replace(/—/g, ' - ')
    .replace(/  -  /g, ' - ');
    
  // 3. Ensure legal byline is a blockquote
  markdownBody = markdownBody.replace(/^\*(Written by the NadLan editorial team.*?)\*$/gm, '> *$1*');

  // Convert to HTML
  let htmlContent = marked.parse(markdownBody);
  
  // 4. Inject CSS classes for tables (Luxury Tables)
  htmlContent = htmlContent.replace(/<table>/g, '<table class="nadlan-luxury-table">');

  // 5. Wrap everything in the LTR and English language container
  htmlContent = `<div class="article-en-ltr" dir="ltr" lang="en">\n${htmlContent}\n</div>`;
  
  // Update via REST API
  const url = `${WP_REST_BASE}/posts/${postDef.id}`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': authHeader,
        'Content-Type': 'application/json; charset=utf-8'
      },
      body: JSON.stringify({
        content: htmlContent
      })
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorText}`);
    }
    
    const result = await response.json();
    console.log(`Successfully updated Post ID ${result.id}`);
  } catch (err) {
    console.error(`Failed to update Post ID ${postDef.id}:`, err.message);
  }
}

async function main() {
  for (const post of posts) {
    await updatePost(post);
  }
}

main();
