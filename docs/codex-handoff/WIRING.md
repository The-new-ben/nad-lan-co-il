# Wiring - NadLan

## Architecture

The repo contains two deployable surfaces:

1. WordPress block theme at repo root.
2. Custom WordPress plugin at `plugins/nadlan-config/`.

Theme is presentation. Plugin is infrastructure/data/runtime.

### Theme responsibilities

- Layout and block templates.
- Public trust cleanup on non-commerce pages.
- Header/footer/patterns/styles.
- Floating action rail and other public presentation logic when implemented in theme.
- Deployment path: UPress server Git pull of `main`, then cache clear.

### Plugin responsibilities

- CPTs and taxonomies.
- REST endpoints.
- Lead capture/routing/WhatsApp bridge.
- AI/concierge settings and routing.
- Project 3D/showroom runtime and CMS fields.
- Healthcheck.
- Schema.
- Deployment path: version bump, build ZIP, commit manifest/ZIP, merge, WordPress plugin update, cache clear.

## Build System

### Theme CSS

`package.json` defines:

```powershell
npm run build
npm run watch
```

Build command:

```powershell
postcss style.css --use cssnano -o style.min.css --no-map
```

Only run this if changing theme CSS that requires minification. Do not commit `node_modules/`.

### Plugin ZIP

Canonical build command:

```powershell
python scripts\build-plugin-zip.py
```

This detects the `Version:` header in `plugins/nadlan-config/nadlan-config.php` and writes `plugin-dist/nadlan-config-<version>.zip`. It verifies:

- entries are rooted under `nadlan-config/`,
- no backslash archive paths,
- CRC is clean.

Never hand-build plugin ZIPs on Windows.

## Test And QA Commands

Safe local checks:

```powershell
php -l functions.php
node --check scripts\qa-stage1-public-trust.mjs
git diff --check
```

Plugin checks when plugin touched:

```powershell
php -l plugins\nadlan-config\nadlan-config.php
php -l plugins\nadlan-config\inc\project-3d.php
php -l plugins\nadlan-config\inc\health.php
python scripts\build-plugin-zip.py
```

Public trust visual QA:

```powershell
node scripts\qa-stage1-public-trust.mjs --phase final --out docs/qa/screenshots/stage1-public-trust-final
```

The QA script launches Chrome/Edge through the DevTools protocol. If Chrome is not auto-detected, set `CHROME_PATH` to the browser executable.

## Runtime Commands

This is a WordPress site on UPress, not a local Node server. There is no repo-local `npm start`.

Live checks:

```powershell
Invoke-RestMethod -Uri https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
Invoke-WebRequest -Uri https://nad-lan.co.il/projects/dimri-yama-sde-dov/
```

## Deployment Flow

### Theme deploy

Use for changes to `functions.php`, templates, patterns, theme CSS, root JS/assets:

1. Merge PR to `main`.
2. Pull/sync Git on the UPress server for the active theme.
3. Clear UPress/site cache.
4. Hard refresh target pages.
5. Run screenshot QA against live site.

### Plugin deploy

Use for changes under `plugins/nadlan-config/` or `plugin-dist/`:

1. Branch from current `origin/main`.
2. Bump all version surfaces:
   - plugin header in `plugins/nadlan-config/nadlan-config.php`,
   - plugin version array/healthcheck values,
   - `inc/health.php`,
   - `project-3d.php` style/script cache-busters if project 3D assets changed,
   - `plugin-dist/nadlan-config.json`,
   - ZIP filename.
3. Build ZIP with `python scripts\build-plugin-zip.py`.
4. Run lint/JS/ZIP guards.
5. Commit and open PR.
6. After merge, update the plugin in WP Admin or upload the ZIP.
7. Clear cache.
8. Verify `/wp-json/nadlan/v1/healthcheck` shows the new version.
9. Run visual QA if any public UI changed.

## Environment Variables And Secrets

Do not put values in the repo. Only names are documented.

Possible environment/config names:

- `CHROME_PATH` - local path for QA harness browser.
- `OPENAI_API_KEY` - actual key is stored outside repo or in WP settings.
- `MAPBOX_TOKEN` / Mapbox public token - configured in WordPress/plugin settings.
- `NADLAN_LLM_API_KEY` - legacy/pluggable LLM key name referenced by old skills.
- WhatsApp ingest secret - stored in WordPress settings; healthcheck currently reports whether present.
- GreenInvoice/Morning credentials - stored in WordPress/Woo settings.
- Stripe/WooCommerce credentials - stored in WordPress/Woo settings.
- WordPress application password - never commit.
- GitHub token/CLI auth - local credential store only.

## External Integrations

- WordPress / UPress hosting.
- GitHub repo: `The-new-ben/nad-lan-co-il`.
- WooCommerce.
- Green Invoice / Morning payment gateway.
- OpenAI for AI concierge/lead qualification.
- Mapbox for map/view-from-apartment.
- Google Site Kit / GA4.
- Yoast SEO.
- IndexNow.
- WhatsApp lead bridge.
- data.gov.il imports.

## Branch Strategy

- Work from current `origin/main`.
- Use short-lived `codex/...` branches.
- Do not work from `.codex-tmp` or old repair folders.
- Keep theme-only and plugin releases separate.
- For plugin releases, version must be strictly greater than current `origin/main`.
- Use ready-for-review PRs when possible; do not self-merge if two-key review is active.

## Local Setup For A New PC

1. Clone:
   ```powershell
   git clone https://github.com/The-new-ben/nad-lan-co-il.git
   cd nad-lan-co-il
   ```

2. Confirm tools:
   ```powershell
   git --version
   gh --version
   php -v
   node -v
   npm -v
   python --version
   ```

3. Install Node dependencies only if you need build/QA scripts:
   ```powershell
   npm ci
   ```

4. Do not commit `node_modules/`.

5. Verify live state:
   ```powershell
   Invoke-RestMethod -Uri https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck
   ```
