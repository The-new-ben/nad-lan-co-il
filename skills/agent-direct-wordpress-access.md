# Agent Direct WordPress Access — what's live, how to use it, what's still gated

> **Read this before assuming you need a git → PR → merge → owner-click cycle for
> everything.** As of 2026-07-01, this session's environment already carries working
> WordPress REST credentials, and four direct-access tools are installed and active on
> the live site. Full narrative + verification commands:
> `docs/research/2026-07-01-ai-wordpress-direct-access-tools.md` (§"SHIPPED 2026-07-01").
> This file is the short operating reference; that one is the research log.

## ⭐ Agent-driven plugin deploy — NO owner "Update" click (proven live 2026-07-01)

The owner's #1 friction was clicking **Update** in wp-admin for every plugin release. That
click is just WordPress running `Plugin_Upgrader` — and an agent with `update_plugins` +
Code Snippets can run the exact same thing. **Proven: v1.69.69 shipped to main and deployed
live with zero owner action.** The repo stays source of truth; only the *deploy trigger*
moves from the owner to the agent. The method (each deploy is create-route → call → delete,
so no permanent privileged route lingers):

1. Ship the release normally: bump version, `python3 scripts/build-plugin-zip.py <ver>`,
   update `plugin-dist/nadlan-config.json`, merge to `main` (so the ZIP is on GitHub raw).
2. Create a **temporary** Code Snippets snippet (`POST /wp-json/code-snippets/v1/snippets`,
   `scope:"global"`, `active:true`) that registers an admin-only REST route running the
   upgrader against the ZIP's raw URL, forcing the `update_plugins` transient first:
   ```php
   add_action('rest_api_init', function () {
     register_rest_route('nadlan-deploy','/run', array('methods'=>'POST',
       'permission_callback'=>function(){return current_user_can('update_plugins');},
       'callback'=>function(){
         require_once ABSPATH.'wp-admin/includes/file.php';
         require_once ABSPATH.'wp-admin/includes/misc.php';
         require_once ABSPATH.'wp-admin/includes/plugin.php';
         require_once ABSPATH.'wp-admin/includes/class-wp-upgrader.php';
         $p='nadlan-config/nadlan-config.php';
         $u='https://raw.githubusercontent.com/The-new-ben/nad-lan-co-il/main/plugin-dist/nadlan-config-<VER>.zip';
         $t=get_site_transient('update_plugins'); if(!is_object($t)){$t=new stdClass();}
         if(empty($t->response)||!is_array($t->response)){$t->response=array();}
         $t->response[$p]=(object)array('slug'=>'nadlan-config','plugin'=>$p,'new_version'=>'<VER>','package'=>$u,'url'=>'https://nad-lan.co.il');
         set_site_transient('update_plugins',$t);
         $s=new WP_Ajax_Upgrader_Skin(); $up=new Plugin_Upgrader($s); $ok=$up->upgrade($p);
         if(!is_plugin_active($p)){activate_plugin($p);}
         return array('result'=>is_wp_error($ok)?('ERR:'.$ok->get_error_message()):var_export($ok,true),'messages'=>$s->get_upgrade_messages());
       }));
   });
   ```
3. `POST /wp-json/nadlan-deploy/run` (basic-auth as the app-password user). Success returns
   `"messages": [... "Plugin updated successfully."]`.
4. Verify: `/wp-json/nadlan/v1/healthcheck` version == new; curl the changed page; homepage 200.
5. **DELETE the snippet** (`DELETE /wp-json/code-snippets/v1/snippets/<id>`) and confirm the
   route is gone (`POST /nadlan-deploy/run` → 404). Never leave the deploy route active.

Notes / gotchas learned:
- **Prefer `install($zipUrl, array('overwrite_package' => true))` over the transient+
  `upgrade()` dance.** The forced `update_plugins` transient can be rewritten by the
  vendored plugin-update-checker's `pre_set_site_transient_update_plugins` filter before
  the upgrader reads it ("The plugin is at the latest version." → nothing deployed —
  observed on the 1.69.70 deploy). `install` with `overwrite_package` is the exact
  "Upload Plugin → Replace current with uploaded" path and skips version comparison
  entirely. Append `?nlcb=<time()>` to the raw URL to dodge the ~5-min GitHub raw cache.
  Used successfully for 1.69.70/71/72/73.
- A `single-use` snippet activated via REST did **not** execute the code — use the
  `scope:"global"` + explicit REST-route call pattern above, which runs in your own
  authenticated request and returns the upgrader messages so you're not deploying blind.
- WordPress enables maintenance mode for ~2-5s during the swap and rolls back on failure;
  the plugin is `function_exists`/`ABSPATH`-guarded, so a partial state is defensive.
- **Rollback** is the same call pointed at the previous good ZIP (e.g. `-1.69.68.zip`).
- Still can't do pixels here (headless Chromium has no egress in the agent sandbox) — verify
  rendered *markup* + health via curl, and have the owner/Codex eyeball the actual look.
- This does not fix the **child theme** (no plugin-update path); for that see the deploy
  pipeline research (`docs/research/`), esp. WP Pusher (GitHub push → auto-install).

## The credential (already in your environment, if inherited correctly)

`WP_BASE_URL`, `WP_USER`, `WP_APP_PASSWORD` — per `skills/agent-onboarding.md`, these are
env vars, not repo files. If your session doesn't have them, see that doc's transfer
process; do not paste the value into chat, a commit, or any file.

**What this credential actually is:** verified 2026-07-01, it authenticates as
**administrator (user id 1, the owner's own WordPress account)** — `install_plugins`,
`manage_options`, `edit_plugins`, `update_plugins` all `true`. It is NOT a scoped
least-privilege agent user. The owner chose to install tools with it as-is rather than
rotate first; that trade-off is still open to revisit (§Open follow-ups).

Never print `$WP_APP_PASSWORD` to output. Verify auth without leaking it:
```bash
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,name,roles" 
```

## What's installed and active right now

| Tool | Slug | What it's for | How to reach it |
|---|---|---|---|
| Code Snippets | `code-snippets` | run PHP/CSS/JS on the live site, no file deploy | REST: `wp-json/code-snippets/v1` (needs wp-admin to author snippets — check its REST surface before assuming write access) |
| Vibe AI | `vibe-ai` | MCP server bridging Claude/Cursor/Windsurf/ChatGPT to this site | REST: `wp-json/wpvibe/v1` (see below — file/CLI routes exist but are gated) |
| Advanced File Manager | `file-manager-advanced` | browse/edit live files, no FTP/SSH | wp-admin page only (Codex-with-Chrome / Cowork / owner) |
| WP Adminer | `pexlechris-adminer` | raw SQL/table access, no DB credentials | wp-admin page only (Codex-with-Chrome / Cowork / owner) |

Confirm the live set before trusting this table (plugins can be deactivated by anyone with
admin, and versions get updated):
```bash
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/plugins?_fields=plugin,status,name"
```

### Vibe AI / MCP — what actually works today

`GET $WP_BASE_URL/wp-json/wpvibe/v1` lists routes for `file/read`, `file/write`,
`file/edit`, `file/delete`, `cli/run`, `cli/run-approved`, `draft-theme` +
`draft-theme/publish`/`preview`. **Do not assume these work** — `GET .../wpvibe/v1/site-info`
self-reports only `"features": ["content_edit", "content_search"]` enabled on this
install, and a `file/list` probe returned a raw nginx 404, not data. The file-write/CLI
tier is very likely gated behind a license or a settings-page toggle that needs a real
wp-admin browser session to check or enable (Codex-with-Chrome, Cowork, or the owner) — a
REST-only agent cannot get past this alone. **If someone does enable it:** `file/write` and
`cli/run` would let an agent push child-theme files directly, bypassing the whole
git → ZIP → manual-upload problem this tooling exists to solve — and `draft-theme` +
`draft-theme/publish`/`preview` looks like it could function as a de facto staging
environment (draft, preview, then publish) on a site that otherwise has none. Worth
someone with wp-admin access checking deliberately, not worth an unattended agent probing
further on a no-staging production site.

### File Manager / Adminer — REST-only agents can't drive these

Both are wp-admin dashboard pages, not REST-exposed by default. A pure-REST session (this
one, most Claude Code sessions) cannot use them directly. Codex (has a Chrome extension +
computer-use) or Cowork (browser tools) can drive them; direct one of those agents when a
task genuinely needs raw SQL or raw file access, rather than trying to force it through REST.

## Safety boundaries — read before using any of this on the live site

1. **There is no staging environment.** Every install/write above landed on production.
   After any mutating call, re-verify health before doing anything else:
   ```bash
   curl -s "$WP_BASE_URL/" -o /dev/null -w "%{http_code}\n"
   curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck" | python3 -c "import sys,json;print(json.load(sys.stdin).get('version'))"
   ```
   If either fails after a change you just made, that change is the suspect — deactivate
   it first (`curl -X POST .../wp-json/wp/v2/plugins/<plugin> -d '{"status":"inactive"}'`),
   don't make a second change hoping to fix the first.
2. **This credential is full-admin, not scoped.** Treat raw-DB (Adminer) and raw-file
   (File Manager) access as deliberate-session tools, not something to wire into an
   always-on loop — this matches the security research in the parent doc (§6 "the honest
   risk") and OWASP/Unit 42 guidance on AI agent least-privilege.
3. **Git is still the source of truth for reviewed code.** These tools are for the gaps
   git can't reach on this host (the child theme's missing deploy path, quick hotfixes,
   live inspection) — they are not a replacement for the branch → PR → merge flow for
   real feature work. Don't use `file/write`/`cli/run` (if it turns out to work) to make
   changes that should have been a commit; at minimum, mirror any live direct-edit back
   into the repo afterward so "if it's not committed, it doesn't exist" still holds
   (`skills/skill-release-discipline-and-mistakes.md` M9).

## Open follow-ups (not done yet, tracked here so the next agent doesn't re-discover them)

- [ ] Rotate `WP_APP_PASSWORD` to a dedicated least-privilege agent user (owner action,
  `skills/agent-onboarding.md` §"Rotate the Application Password" has the exact steps).
- [ ] Someone with wp-admin browser access: check Vibe AI's settings page for a
  file/CLI-access toggle or license requirement.
- [ ] Delete the `nadlan-rescue-showroom` theme from the live server — it's still
  installed (inactive) despite being explicitly rejected in
  `handoff/external-agent-packages/2026-06-28/REVIEW-AND-SOLUTION.md`. Low risk since
  it's inactive, but it's a footgun if anyone ever activates it by mistake.
- [ ] Fold in findings from the in-progress deep-research on IDE-direct-connection /
  CI-deploy pipeline patterns (started 2026-07-01, covers ground beyond REST/MCP — WP
  Pusher, Deployer.org, Bedrock/Trellis, GitHub Actions SFTP deploy, etc.) once it lands.

---
_Created 2026-07-01 by Claude Code, same session that installed the four tools above._
