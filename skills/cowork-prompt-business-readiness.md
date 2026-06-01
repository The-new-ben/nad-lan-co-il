# Cowork Activation — Business-Readiness Sprint

> Single copy-paste prompt for the owner to hand to a fresh Cowork session. Self-contained, with obstacle handling for every conceivable failure. Cowork never authors Hebrew prose (preserve Anthropic tokens — ChatGPT does long-form writing). Cowork is the OPERATOR: server fixes, file deploys, analytics wiring, plugin work, `/advertise/` page build, hands-on tasks.

---

## COPY EVERYTHING BELOW THIS LINE → PASTE TO COWORK → SEND

```
COWORK ACTIVATION — NADLAN BUSINESS-READINESS SPRINT
=====================================================

You start with no memory. Read this whole brief. Then execute non-stop until §STOP fires. Owner is offline; do not ask for approvals. "Continue" is always the answer for in-scope items.

IRON RULE: You never author Hebrew prose. ChatGPT does that. You are the OPERATOR: server fixes, file deploys, plugin work, analytics wiring, page scaffolding (HTML/CSS/PHP), and verification. Any Hebrew content > 50 words → spawn a single ChatGPT prompt (via owner's Project) or use existing pre-approved snippets in skills/customer-value-spec.md.

YOUR ACCESS (verify; never claim you lack):
- Repo /home/user/nad-lan-co-il, branch claude/charming-meitner-mwVEW
- WordPress REST admin: env WP_BASE_URL / WP_USER / WP_APP_PASSWORD
- Drive MCP (mistabrajustice@gmail.com) for any Doc handoffs
- GitHub MCP scope the-new-ben/nad-lan-co-il
- Browser/computer-use for the WP admin panel when REST is insufficient

MANDATORY READING AT SESSION START (one pass):
1. AGENTS.md, HANDOFF.md
2. skills/README.md
3. skills/site-state.md  ← last 12 blocks
4. skills/monetization-readiness-and-adsales.md  ← THE business playbook
5. skills/customer-value-spec.md                 ← WHAT each customer gets (publish as /advertise/)
6. skills/accessibility-israel-is5568.md
7. skills/article-guide-design-pattern.md + skills-templates/article-guide.css
8. skills/nadlan-config-plugin.md (full plugin history incl. v1.3.0 notes)

==============================================================================
TASK 1 — MAKE PLUGIN v1.3.0 ACTUALLY ACTIVE ON THE SERVER (highest priority)
==============================================================================
The repo is at v1.3.0 (robots.txt filter + wptexturize disable). The live
plugin reports v1.2.0 via /wp-json/nadlan/v1/healthcheck. The owner did
`git pull`, but the active plugin file in wp-content/plugins/nadlan-config/
was not updated.

Steps:
a) Confirm baseline. curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck"
   → if version already "1.3.0" → skip to TASK 2.
b) The wp-content path differs from repo plugins/ path. You cannot SSH/SFTP
   from here, but you CAN:
   - (Recommended) Build a zip of plugins/nadlan-config/ and upload via WP
     Admin → Plugins → Add New → Upload (overwrites with confirmation).
     Open the WP Admin URL the owner provided; if no session, use
     application password to authenticate via REST equivalent.
   - (Alternative) Use the WP Admin Plugins page via browser automation:
     Plugins → "nadlan-config" → Plugin Updates section → Upload zip.
   - (If the Plugin Update Checker / PUC is configured) Build a
     plugin-info.json + zip and publish at the PUC metadata URL; trigger
     "Check Again" in WP Admin → Updates.
c) After upload, healthcheck must return version=1.3.0. Verify, log to
   site-state.md, commit, push.

OBSTACLES:
- Upload fails ("file too large") → check `upload_max_filesize` via WP
  Admin → Tools → Site Health → Info; if low, advise owner to raise in
  php.ini. Don't escalate; just leave a note + try smaller zip (delete
  /lib/plugin-update-checker/ before zipping if you must).
- Plugin won't activate after upload → check Site Health for fatal errors;
  PHP syntax already validated locally. If activation fails, revert via
  WP Admin → Plugins → "Replace" with the previous zip; report to owner.
- WP Admin login fails / no session → use the App Password REST flow for
  what you can; for what you can't, document blocker in site-state.md and
  move to TASK 2 — don't burn time.

==============================================================================
TASK 2 — ROBOTS.TXT (server-level fix; cannot be solved by plugin alone)
==============================================================================
Current state: https://nad-lan.co.il/robots.txt → nginx 404. The plugin's
robots_txt filter only fires if nginx routes /robots.txt → index.php.
Most likely nginx is intercepting before WP.

Steps:
a) Create a physical robots.txt fallback in the repo at the root.
   File content (UTF-8, no BOM, LF line endings):

       User-agent: *
       Allow: /
       Disallow: /wp-admin/
       Allow: /wp-admin/admin-ajax.php
       Disallow: /cart/
       Disallow: /checkout/
       Disallow: /my-account/
       Disallow: /*?s=
       Disallow: /*add-to-cart=

       Sitemap: https://nad-lan.co.il/sitemap_index.xml

b) Commit + push. Tell the owner exactly what to do server-side:
   - Drop the file at the web-root (the same dir as WP's index.php), OR
   - Add this to the nginx site block:
       location = /robots.txt { try_files $uri /index.php?$args; }
   Send them both options + which is simpler for their host. Wait for
   confirmation before continuing — but do TASK 3 in parallel.

==============================================================================
TASK 3 — ANALYTICS WIRING (waits for owner's GA4 Measurement ID)
==============================================================================
Once owner sends G-XXXXXXXXXX:

a) Add to plugins/nadlan-config/nadlan-config.php a v1.4.0 block:
   - constant: define( 'NADLAN_GA4_ID', 'G-XXXXXXXXXX' );
   - hook wp_head with priority 1 to print:
       <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
       <script>
         window.dataLayer=window.dataLayer||[];
         function gtag(){dataLayer.push(arguments);}
         gtag('js', new Date());
         gtag('config','G-XXXXXXXXXX',{ anonymize_ip: true });
       </script>
   - skip on /wp-admin/, /wp-login.php, and when current_user_can('edit_posts')
   - respect a future consent cookie (placeholder: if cookie 'nadlan_no_track'=1
     then skip — easy to wire to a banner later)
   - bump version: 1.3.0 → 1.4.0 (file header + healthcheck)
b) Also add Microsoft Clarity (free heatmaps) IF owner provides the project
   ID later — gate behind a similar constant NADLAN_CLARITY_ID. Don't
   block on it.
c) Update skills/nadlan-config-plugin.md with the v1.4.0 notes.
d) Commit, push. Owner re-uploads/auto-update brings it live; verify by
   loading the homepage and grep'ing for G-XXXXXXXXXX.
e) IN GA4: GA4 Admin → Property → Connected products → Search Console
   → already linked by owner. Verify reports flow (24-48h delay normal).
f) Set up GA4 Conversion events:
   - 'generate_lead' (when /wp-json/nadlan/v1/lead returns 200): add a
     gtag('event','generate_lead',{...}) call to the existing thank-you
     handler (find the JS that POSTs to /wp-json/nadlan/v1/lead and add
     the gtag call on success).
   - 'view_pricing' (when /join-pro/ loads).
   - 'click_advertise_contact' (CTA on /advertise/ when built).

OBSTACLES:
- Owner doesn't have Measurement ID yet → SKIP to TASK 4. Do not invent
  an ID. Do not insert placeholders that ship.
- Plugin upload blocked → write the gtag snippet via a TEMPORARY WP hook
  by editing the theme's functions.php only if absolutely necessary,
  and revert after the plugin update is in.

==============================================================================
TASK 4 — BUILD /advertise/ + /pricing/ PAGES (real, publish-ready)
==============================================================================
Source of truth: skills/customer-value-spec.md (Hebrew-translatable bullet
form already written). DO NOT freely author Hebrew prose; assemble from
existing approved language + ask ChatGPT for any new Hebrew via a single
Project prompt (per owner's runbook). Tight loop, not creative writing.

a) Build /advertise/ as a new WP page (REST POST /wp/v2/pages with
   parent=0, status=publish, slug=advertise, full nadlan-guide design).
   Section structure (8 H2s):
   1. למי האתר מתאים — קונים, מוכרים, יזמים, אנשי מקצוע
   2. הקהל שלנו — current honest audience numbers (auto-pull from GA4
      once wired; until then leave a "📊 בקרוב — נתוני קהל לאחר התקנת מערכת המדידה" placeholder)
   3. מסלולי פרסום למקצוענים — Free/Basic/Pro/Premier table (from
      customer-value-spec.md §A) with prices, deliverables, position,
      duration, reporting, "להירשם" CTA → /join-pro/
   4. עמוד פרויקט ליזמים וקבלנים — from §C
   5. מודעת נכס למוכרים פרטיים — from §B
   6. כתבה ממומנת — from §D (with the תוכן שיווקי disclosure note)
   7. לידים בתשלום לכל ליד — from §F
   8. שאלות נפוצות — pull from internal-linking-hub-spoke.md FAQ block
      patterns; 6 Q&As covering: traffic guarantee?, refund?, how delivered?,
      how reported?, legal compliance?, contact for custom.
   Add /advertise/ to the site-wide footer links bar (already in
   nadlan-revenue//footer template-part).

b) Fix /pricing/ slug: currently redirects to /selling-apartment/pricing-apartment-for-sale/.
   Either (i) free the /pricing/ slug by renaming that article's URL — DO
   NOT do this, SEO risk — or (ii) make /pricing/ a section-anchor of
   /advertise/. Recommended (ii): create a Yoast redirect /pricing/ → /advertise/#מסלולים.

c) Wire the existing /join-pro/ page to link the 4 WooCommerce SKUs
   (475/476/477 + free option). If the page already does — verify the
   add-to-cart buttons work. If not — add the wp_block patterns.

d) Update internal-linking-hub-spoke.md — /advertise/ now links to and
   from /about/, /editorial-policy/, /join-pro/, all pillars (footer).

OBSTACLES:
- /advertise/ slug collision → check first via GET /wp/v2/pages?slug=advertise.
  If exists, UPDATE it. If exists as draft, publish.
- Long Hebrew sections → use the Drive PROMPTS Doc (id 1zBBuran...) approach:
  spawn ONE ChatGPT prompt asking for the H2 section text under §X with the
  customer-value-spec.md bullets attached; harvest from the Drive inbox or
  the chat code block. NEVER write Hebrew yourself.

==============================================================================
TASK 5 — SEED THE EMPTY DIRECTORY (the "empty shelves" fix)
==============================================================================
Catalog has nadlan_professional=0 and nadlan_project=0. We cannot sell paid
profiles when the directory is empty. Seed 6 sample nadlan_professional
posts (placeholder, status=draft) so the layout is real:
- one each for: עורך דין נדל"ן, שמאי מקרקעין, יועץ משכנתאות,
  אדריכל, קבלן שיפוצים, מתווך מורשה
- title = profession in Hebrew, content = 1 sentence "placeholder" + the
  nadlan_city taxonomy = "תל אביב".
Mark them clearly as drafts so they don't go public.
This is so /professionals/ archive has structure to show prospects.

Same approach for 3 nadlan_project sample drafts.

==============================================================================
TASK 6 — LOG + COMMIT (per task)
==============================================================================
Append a one-paragraph block to skills/site-state.md per task completed.
Commit small commits per task (easy rollback). Push to origin claude/charming-meitner-mwVEW.
Push retry: 4x exponential backoff 2/4/8/16s on network error.

==============================================================================
TASK 7 — PHASE 0 SCAFFOLDING (read skills/proptech-adoption-roadmap.md FIRST)
==============================================================================
Owner has approved building the Phase 0 wedge layer. Scaffold these AS EMPTY
PAGES + UI shells (no live calls to external APIs yet — owner adds keys later).
Don't author Hebrew prose; pull labels/CTAs from customer-value-spec.md and
proptech-adoption-roadmap.md.

a) /contract-check/ — page with upload form + Hebrew copy block from
   roadmap §0.1. Form POSTs to /wp-json/nadlan/v1/lead with type=contract.
   Add a "מסלולי בדיקה" tier table: free AI flags / ₪450-750 lawyer review 48h.
b) /avm/ — page with address-input form + result placeholder card. Wire
   to a stub endpoint that returns "מערכת ההערכה בהשקה — תוצאות בקרוב"
   until owner connects a real AVM service.
c) /tax-calculator/ — extend the existing /purchase-tax-calculator/ to
   support the all-in flow per roadmap §0.3 (inputs: price + buyer
   profile + holding period; outputs: combined number). UI shell only;
   keep the existing single-tax calc functional.
d) /sold-prices/ — page that embeds an iframe of nadlan.gov.il for now,
   plus a "בקרוב: מפת חום של עסקאות אחרונות בכתובת" placeholder. Tracks
   intent + sets the SEO marker.
e) /tama-38-checker/ — address input → returns placeholder "מערכת
   בהשקה" while owner decides on the data source.

Each page: green nadlan-guide design, staff byline, schema, footer link
added to nadlan-revenue//footer template-part.

OBSTACLES:
- External API key not yet provided → ship as placeholder, not skipped.
  The pages have SEO value the day they exist even before live data.
- Stub responses must NOT be fake numbers. Always return "בהשקה" until
  real data is wired.

==============================================================================
STOP CONDITIONS
==============================================================================
1. Owner sends explicit stop.
2. WP REST returns persistent 401/403 → cannot proceed; log and stop.
3. Plugin upload fundamentally fails AND TASK 2/4/5 also blocked → log
   everything in site-state.md, push, stop.
4. All in-scope tasks done (TASK 1-6 with TASK 3 deferred if no GA4 ID
   yet) → write final report block in site-state.md, push, stop politely.

NEVER STOP FOR:
- "Should I continue?" → never; continue.
- Owner is away → continue; output channels are live pages + commits +
  /published/ Drive folder.
- One Hebrew section needs writing → send ONE ChatGPT prompt (per owner's
  runbook v3.2 §6A), wait via Drive poll, do other tasks in parallel.

NEVER:
- Author Hebrew prose yourself (token preservation).
- Sell or imply traffic guarantees on /advertise/ (legal + honesty).
- Add overlay-style accessibility widgets (accessiBe etc.) — they're not
  compliance.
- Touch the JSON-LD Person schema (owner-locked: keep as-is).
- Commit any plugin without a php -l clean check.

START NOW: preflight → read the 8 mandatory skills → TASK 1.
```

---

## How to use this prompt

1. Open a new Cowork session.
2. Copy everything inside the `COWORK ACTIVATION` block (the triple-backticks code).
3. Paste, send, walk away.
4. When you have the GA4 Measurement ID, paste this short follow-up into the same Cowork:
   ```
   GA4 Measurement ID: G-XXXXXXXXXX
   Proceed with TASK 3.
   ```
   Cowork resumes from there.

## Boundaries

Cowork does the hands-on operator work above. He does NOT:
- write more Hebrew articles (already done by ChatGPT/Claude for the 22 articles)
- make business-strategy decisions (owner does)
- decide pricing (it's locked in customer-value-spec.md)
- redesign anything

_Created 2026-05-31 by Claude Code. v1: business-readiness sprint covering plugin deploy, robots.txt, GA4 wire, /advertise/ build, directory seed._
