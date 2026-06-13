# v1.61.0 Rainbow Premium Showroom + SEO + WhatsApp Funnel QA

## Goal

Make the Rainbow Tel Aviv page closer to a premium buyer showroom and a repeatable project-page
system:

- interactive model appears before the old static profile card,
- building selector is the default product surface,
- Mapbox view stays user-opened and RTL-safe,
- price/availability language is source-backed and non-binding,
- WhatsApp can enter the same lead funnel instead of leaking out of the system,
- the pattern is documented for the next Sde Dov project.

## Research Evidence Used

### SERP And Project Facts

- Official Rainbow site: `https://rainbow-telaviv.com/`
  - Lesson: official branding exists, but the official page cannot safely serve comparative price
    and buyer-evaluation intent the way NadLan can.
- Israel Canada Rainbow page: `https://www.israel-canada.co.il/projects/tel-aviv/rainbow`
  - Lesson: developer identity and official marketing claims must be cited separately from market
    journalism.
- Sde Dov project page: `https://sdedov.co.il/project/rainbow/`
  - Lesson: compound context matters; Rainbow should be cloned into a Sde Dov map system later.
- Globes, May 2025: `https://www.globes.co.il/news/article.aspx?did=1001511649`
  - Lesson: public market reporting supports a non-binding price narrative and dates the numbers.
- Calcalist, public sales reports: `https://www.calcalist.co.il/market/article/bj9leo2fxx`
  - Lesson: searchers want transaction numbers; use them as citations, not as live inventory.
- Bizportal, June 2026 Sde Dov pricing/sales pace: `https://www.bizportal.co.il/realestates/news/article/20033505`
  - Lesson: price intent should mention both prestige and risk/slowdown honestly.

### Product Interaction Patterns

- Baymard product-page research: `https://baymard.com/research/product-page`
  - Lesson: the product page is the decision center; high-value interaction must sit where users
    expect the product media, not below a long article.
- Baymard on videos/360 views near image gallery: `https://baymard.com/blog/embedding-product-page-videos`
  - Lesson: 360/product views belong at the top product media surface, not hidden in a tab far down
    the page.
- `<model-viewer>`: `https://modelviewer.dev/`
  - Lesson: future real GLB models should use a proven web component, but the current SVG/CSS
    showroom should remain lightweight until official drawings/models are available.

### WhatsApp Funnel Patterns

- Meta WhatsApp webhooks overview: `https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview/`
  - Lesson: official API webhooks can carry WhatsApp messages as JSON, so our first bridge should
    accept JSON and map into the lead CPT.
- Meta messages webhook reference: `https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/`
  - Lesson: inbound message bodies and statuses should be treated as provider events, not as a
    click-only CTA.
- 360dialog coexistence docs: `https://docs.360dialog.com/docs/resources/phone-numbers/coexistence`
  - Lesson: Business App/API coexistence exists, but requires provider setup; v1.61.0 ships a
    secret-gated bridge rather than unofficial personal-number scraping.

## Implementation Summary

### Project 3D

- `inc/project-3d.php`
  - moves the module before the `.nlpf` static profile header,
  - adds `<!-- nlp3d-start -->` / `<!-- nlp3d-end -->`,
  - adds a stage-first showroom CSS layer,
  - keeps building/model as default,
  - keeps Mapbox user-opened,
  - registers Mapbox RTL text plugin before map creation,
  - bumps asset handles to `1.61.0`.

### Raw Script Leak

- `inc/directory.php`
  - removes raw project/professional profile-header `<script>` handlers from the content body,
  - replaces inline `onclick` with data attributes,
  - registers `nadlan-project-profile-quote` and `nadlan-professional-quote` through
    `wp_add_inline_script`.

### SEO Assembly

- `inc/project-page-assembly.php`
  - one-shot seed for Rainbow only, gated by `nadlan_rainbow_seed_v1610`,
  - writes schema meta before render: amenities, official site URLs, price range, min/max and FAQ,
  - prepends a visible `nadlan-guide` SEO block only once,
  - keeps price language non-binding and source-backed.

### WhatsApp Funnel

- `inc/whatsapp-lead-ingestion.php`
  - adds `POST /wp-json/nadlan/v1/wa-lead`,
  - requires `X-Nadlan-WA-Secret`,
  - resolves `card_id` from payload, URL, or text pattern when possible,
  - reuses `nadlan_lead_e2e_capture` when enabled,
  - logs a non-PII event and exposes `whatsapp_funnel` in healthcheck.
- `inc/conversion-cta.php`
  - adds an admin-only secret field under Settings -> NadLan CTA + WhatsApp,
  - never echoes the stored secret,
  - stores the secret with `autoload=false`.

### Floating Contact Controls

- `inc/premium-ui.php`
  - adds safe-area positioning and focus/tap-target polish for `#nlai` and `#nlcta`,
  - prevents the mobile chat panel from covering the entire viewport in a crude way.

## Manual QA Commands

```powershell
git diff --check
```

Result: clean except normal Windows CRLF warnings.

```powershell
node --check "$env:TEMP\nadlan-p3d-1610.js"
```

Result: pass.

```powershell
python - <<'PY'
# Validates plugin-dist/nadlan-config.json + plugin-dist/nadlan-config-1.61.0.zip.
PY
```

Result: manifest version `1.61.0`, download URL points to `nadlan-config-1.61.0.zip`, ZIP has
130 entries, every entry starts with `nadlan-config/`, zero backslash paths, and the archive
contains `inc/project-3d.php`, `inc/project-page-assembly.php`, `inc/whatsapp-lead-ingestion.php`,
`inc/directory.php`, and `nadlan-config.php`.

```powershell
rg -n 'nadlanProQuote|nadlanProjQuote|data-nadlan-professional-quote|data-nadlan-project-quote' plugins\nadlan-config\inc\directory.php
```

Result: only `wp_add_inline_script` handlers and `data-*` buttons remain. No raw
`<script>function nadlanProQuote` / `<script>function nadlanProjQuote` block remains in the profile
body.

```powershell
php -v
```

Result: unavailable in this Windows shell, so `php -l` must run in Claude/deploy gate.

## Post-Deploy Gates

1. `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck`
   - version must be `1.61.0`,
   - `project_page_assembly.loaded = true`,
   - `project_page_assembly.faq_meta = true`,
   - `whatsapp_funnel.loaded = true`.
2. Rainbow page desktop 1440:
   - no visible raw `function nadlanProjQuote`,
   - `.nlp3d` appears before `.nlpf`,
   - building selector is the default visible stage,
   - drag on `.nlp3d-scene` changes `--angle`,
   - selecting a unit updates stage card and detail facts.
3. Rainbow page mobile 390:
   - no horizontal overflow,
   - stage card not clipped,
   - floating buttons do not cover the lead form or footer,
   - controls remain at least 44px.
4. Map view:
   - opens only after user taps `מבט`,
   - contains `.mapboxgl-canvas`,
   - Hebrew labels are not reversed after RTL plugin load.
5. WhatsApp bridge:

```bash
curl -i -X POST "https://nad-lan.co.il/wp-json/nadlan/v1/wa-lead" \
  -H "Content-Type: application/json" \
  -H "X-Nadlan-WA-Secret: <configured-secret>" \
  --data '{"name":"בדיקת וואטסאפ","phone":"0500000000","message":"ראיתי את https://nad-lan.co.il/projects/rainbow-tel-aviv/ ורוצה פרטים","card_id":4464}'
```

Expected: `200`, lead id returned, attributed card id returned. Without secret: `401`; without
configured secret: `503`.

## Known Limits

- This is still not a real GLB/BIM model. It is a premium lightweight showroom over the existing
SVG/CSS contract. Real architecture requires developer drawings or a licensed model.
- Public prices remain estimates, not live inventory.
- WhatsApp Cloud API/coexistence is not configured here; v1.61.0 provides the secure NadLan bridge
that a Shortcut/API relay can call.
- PHP lint is not locally proven because this shell has no PHP binary.

## Deployment Reminder

After merge: pull/sync the uPress/server Git copy, then update/upload the WordPress plugin. A GitHub
merge alone does not update the live site.
