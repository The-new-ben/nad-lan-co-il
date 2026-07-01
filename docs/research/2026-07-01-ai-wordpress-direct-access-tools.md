# Developing nad-lan.co.il with AI, directly — tools, real quotes, honest limits
Research date 2026-07-01 · Author Claude Code · Web-search sourced, quotes verbatim.

The owner's problem, stated plainly: the current workflow (edit repo → PR → merge → UPress
"Pull main" for the theme, and build ZIP → wp-admin "Update" for the plugin) is slow and
indirect. UPress has no SSH/CLI. He wants to know if there's a way for an AI agent to connect
and work on the live site *directly* — code, database, tables, files — without the git dance.

Answer up front: **Yes, there are now real, direct-connect options** (the WordPress MCP
Adapter + application passwords + two browser-admin plugins). They are much better than
git-pull for many tasks. But each has honest limits, and giving an AI agent unlimited
raw access to a live production DB is exactly what security researchers are warning against
in 2026. Details below.

---

## 1. The big one: the official WordPress MCP Adapter (Feb 2026)

WordPress shipped an official Model Context Protocol adapter that lets AI tools connect
straight into a WordPress site. From the WordPress Developer Blog announcement:

> "The adapter implements the Model Context Protocol in the scope of a WordPress site and
> lets AI tools (like Claude Desktop, **Claude Code**, Cursor, and VS Code) discover and
> call WordPress Abilities directly."
> — developer.wordpress.org/news/2026/02/from-abilities-to-ai-agents-introducing-the-wordpress-mcp-adapter/

How Claude Code connects (from Daniel Kossmann's setup guide): you create a WordPress
**Application Password** for an admin user (Users → Profile → Application Passwords), install
the MCP Adapter plugin, point Claude Code at the site URL + username + app password, then
`/mcp` shows the connected `wordpress-mcp-server`. One command form:
`claude mcp add --transport http mymcp <mcp_url>`.

Reception (InstaWP / smartwp / adalike coverage):

> "WordPress now has an official Claude connector built on the Model Context Protocol (MCP)
> — and reviewers believe most people are seriously underestimating how big this is."

> "the possibilities are 'mind-blowing' once connected to a live website … Claude can create
> posts, manage plugins, clean up taxonomies, and audit your site through natural language."

**The honest limit** (this matters for the owner's "reach the database and tables" ask):

> "No database-level operations are supported. Direct SQL queries, table modifications, or
> raw data access are outside MCP scope. The MCP Adapter works through the WordPress REST
> API, which does not expose file system operations by default."
> — search synthesis across WordPress/mcp-adapter docs + smackcoders guide

> "the core WordPress abilities currently available via MCP are read-only … By design,
> nothing in the WordPress Abilities API is exposed via MCP unless it is explicitly marked
> as MCP-public."

So the official adapter = clean, safe, structured access to **posts / pages / media / meta /
taxonomies / settings / WooCommerce** — NOT raw SQL or files. WordPress.com's hosted MCP has
full write since March 2026, but that's their hosting, not UPress.

## 2. Raw database / tables — WP Adminer plugin

For the "reach the tables and run SQL" need, the real tool is an **Adminer-in-wp-admin**
plugin (`pexlechris-adminer` / `janzikmund/wp-adminer`). From its own description:

> "Allows quick, direct database access during development. Uses wp-config values to login
> user automatically. Handy for doing database changes when admin only has WP admin access
> but **no server or database credentials**." — github.com/janzikmund/wp-adminer

> "Adminer … allows viewing and editing of databases tables, routines, triggers, etc., and
> allows running SQL statements to import data, make bulk changes, or perform other complex
> operations … access is granted only to logged-in accounts that possess the edit_plugins
> capability (normally admins)."

This is the answer to raw DB access on a host with no SSH/CLI: it runs SQL through the browser
using the site's own wp-config credentials. An agent with Chrome (Codex, Cowork) can drive it;
it is not directly MCP-scriptable, but it removes the "I can't reach the tables" wall.

## 3. Raw files / code — File Manager + Code Snippets

- **Advanced File Manager** (`file-manager-advanced`): a file browser + code editor inside
  wp-admin. Its own listing: "includes an AI-powered coding assistant in the code editor
  where you can write functions, generate CSS or PHP, debug safely, and get instant
  explanations." This gives file access without SFTP/SSH.
- **Code Snippets** / **FluentSnippets**: run arbitrary PHP on the live site from wp-admin,
  stored in the DB (`wp_snippets`), toggled like plugins — no file editing, no deploy. Good
  for hotfixes and functions.php-type additions without a theme pull.

## 4. UPress reality

UPress is a managed Israeli WordPress host "focused on developers, offering support for
version management, plugins, migrations, and DNS operations" (upress.io). Public docs did NOT
surface an SSH/WP-CLI offering — consistent with the owner's experience. The distinction that
matters (from seresa.io): **"you can have WP-CLI without SSH (via web interfaces), and SSH
without WP-CLI."** So the path on UPress is not "get a CLI"; it's app-password + REST/MCP +
the browser-admin plugins above. The existing UPress "Pull main" git panel stays as the
deploy path for theme *files*; MCP/REST handles *data and content* directly.

## 5. The three agents (real, current)

- **Claude Code** (me): terminal agent, connects to WordPress via the MCP Adapter (§1) using
  an app password. Best for: code, releases, review, orchestrating Codex/Cowork, and — once
  MCP is wired — direct content/meta operations without git.
- **Codex** (OpenAI): now has a **Chrome extension + background computer-use** (May 2026), so
  it can drive wp-admin, Adminer, and File Manager in a real browser — the raw-DB/file lane.
- **Google Antigravity** (agentic IDE, public preview, free): a real developer's verbatim
  account of building a WordPress site with it —
  > "I didn't write a single line of PHP code. I didn't touch a SQL query. I just managed a
  > team of expert AI agents." … "In 3 hours, I had a fully working WordPress website exactly
  > as per my requirements." … "Antigravity's built-in browser agent loaded the actual page,
  > clicked on the buttons, and navigated through the actual flows to validate its generated
  > code." — Pratik Machchar, Medium
  > Honest caveat from the same author: "The AI had injected a test string into a template and
  > forgot to remove it … This shows that AI is smart, but it can still hallucinate."

## 6. The honest risk (the owner should hear this before granting full access)

The 2026 security literature is blunt about handing AI agents WordPress admin power:

> "WordPress Was Already a Security Nightmare. AI Agents Are About to Make It Unlivable."
> — charlesjones.dev (headline)

> "WordPress 7.0 Ships AI Agent Infrastructure: API Key Theft Risk Surfaces on Launch Day"
> — techtimes.com

> "Any user-generated content — comment sections, contact forms, community forums — becomes a
> potential prompt-injection surface for any agent that scans it."

> "AI agents should operate with the minimum permissions necessary … if an agent is browsing
> the web for pricing data, it shouldn't also have write access to a production database."
> — synthesis, OWASP / Palo Alto Unit 42 / MindStudio

Translation for nad-lan.co.il: a full-admin app password given to an always-on agent, on a
public site with lead forms and (soon) buyer LOI submissions, is a real attack surface. The
mitigation is scoping — a dedicated agent user with only the capabilities it needs, app
passwords that can be revoked instantly, and keeping raw DB/file plugins gated to deliberate
sessions rather than always-on automation.

## 7. Recommendation for THIS site (practical, not hype)

1. **Install the WordPress MCP Adapter + create an app password for a dedicated agent user.**
   This lets Claude Code (me) read/write content, meta, media, settings directly — killing the
   git-pull dance for everything that is *data* (project fields, prices, LOI leads, SEO meta,
   posts/news, listings). Theme *file* changes still deploy via the git pull; but far less of
   the day-to-day work is file changes than it looks.
2. **Install WP Adminer + Advanced File Manager** for the times we genuinely need raw tables
   or files. Codex (Chrome) or Cowork drives them; I direct.
3. **Keep git for what git is good at** — versioned theme/plugin code, review, rollback. Stop
   using it for content/data operations that MCP/REST can do live.
4. **Scope the credential** — dedicated user, least privilege, revocable app password, and do
   NOT wire raw-DB access into the always-on loop. Deliberate sessions only.

Net: the owner's instinct is right and the tooling now exists to work far more directly than
git-pull. The realistic version is "direct via MCP + REST for data, browser-plugins for
raw DB/files, git only for code" — not "one agent with unlimited root on the live database,"
which the security research specifically warns against.

## SHIPPED 2026-07-01 — four tools installed live, verified

The owner authorized installing directly against production (no staging site exists — see
`docs/rebuild-nadlan-2026-06-28/no-staging-platform-rollout.md`). Discovered first: the
`WP_BASE_URL`/`WP_USER`/`WP_APP_PASSWORD` env vars already present in this Claude Code
session authenticate as **administrator (user id 1, the owner's own account)** with
`install_plugins`, `manage_options`, `edit_plugins`, `update_plugins` all `true` — meaning
a REST-only agent session can install and activate wordpress.org plugins directly via
`POST /wp/v2/plugins {"slug": "...", "status": "active"}`, no wp-admin browser/login needed.
This is a materially different capability than "agents have NO WordPress admin access,"
which most of `skills/` was written assuming.

**The "official" WordPress MCP Adapter (`github.com/WordPress/mcp-adapter`) is NOT on the
wordpress.org plugin directory** (confirmed 404 on both `wordpress-mcp` and `mcp-adapter`
slugs via `api.wordpress.org/plugins/info/1.2/`) — it cannot be installed through this REST
path; only wp-admin's manual "Upload Plugin" (a ZIP from GitHub) would work, which needs a
real wp-admin login (Application Passwords authenticate REST/XML-RPC only, not the
`wp-login.php` cookie session). Used **Vibe AI (`vibe-ai`, wordpress.org, 2,000 installs)**
instead — a plugin built specifically to "connect your self-hosted site to any AI assistant
that speaks MCP: Claude, ChatGPT, Cursor, Windsurf, OpenCode" — confirmed to exist and
install cleanly.

Installed one at a time via REST, site-health-checked (`curl` homepage HTTP 200 +
`/wp-json/nadlan/v1/healthcheck` version unchanged) after each before proceeding to the next:

| Plugin | Slug | Version | Installs | Purpose |
|---|---|---|---|---|
| Code Snippets | `code-snippets` | 3.9.6 | 1M+ | run PHP/CSS/JS on the live site from wp-admin, no file deploy |
| Vibe AI | `vibe-ai` | 1.5.1 | 2K | MCP server — connects Claude/Cursor/Windsurf/ChatGPT directly |
| Advanced File Manager | `file-manager-advanced` | 5.4.12 | 100K+ | browse/edit files in wp-admin, no FTP/SSH |
| WP Adminer | `pexlechris-adminer` | 4.3.4.1 | 20K+ | raw SQL/table access in wp-admin, no DB credentials needed |

All four active; site stayed healthy (HTTP 200, unchanged plugin version) through every step.

**Vibe AI's real capability is narrower than its route list suggests.** `GET /wp-json/wpvibe/v1`
lists an ambitious route set — `file/read`, `file/write`, `file/edit`, `file/delete`,
`cli/run`, `cli/run-approved`, `draft-theme` + `draft-theme/publish`/`preview` (a staged
theme-editing workflow that could double as a poor-man's staging environment) — but
`GET /wp-json/wpvibe/v1/site-info` (authenticated, verified working) self-reports only
`"features": ["content_edit", "content_search"]` as actually enabled on this install, and
a probe of `GET /wp-json/wpvibe/v1/file/list?path=.` returned a raw nginx 404 (not a
WordPress JSON error), not file data. **Conclusion: the file/CLI superpowers are gated**
(free-tier limit, license key, or a settings-page opt-in) — did not attempt `file/write` or
`cli/run` given the ambiguity and no-staging risk. Checking/enabling those needs wp-admin
browser access (Codex with Chrome, Cowork, or the owner), not a REST-only session.

**Side finding, not yet acted on:** `site-info`'s `themes` list still includes
`nadlan-rescue-showroom` — the theme `handoff/external-agent-packages/2026-06-28/REVIEW-AND-SOLUTION.md`
explicitly rejected ("DO NOT ACTIVATE... would erase the calculator hub, the
2,711-professional directory, billing/monetization, and all SEO machinery"). It's installed
but inactive; recommend deleting it from the live server to remove the footgun, pending
owner confirmation since deleting is a live mutating action.

**Credential model note:** because `WP_USER`/`WP_APP_PASSWORD` are shared across agent
sessions per `skills/agent-onboarding.md`'s "same platform environment → inherited
automatically" model, every agent that inherits this environment now has these same four
tools available with no per-agent setup — but it also means all four now sit behind one
un-rotated, full-admin credential rather than a scoped least-privilege agent user (the
owner explicitly chose "install now" over "rotate first" on 2026-07-01, aware of the
trade-off). The rotation recommendation from the original research below still stands as
a follow-up, not a blocker.

## Sources
- WordPress Developer Blog — MCP Adapter announcement (Feb 2026)
- github.com/WordPress/mcp-adapter ; github.com/Automattic/wordpress-mcp
- developer.wordpress.com/docs/mcp/ ; wordpress.com/support/model-context-protocol-mcp-settings/
- danielkossmann.com — Claude Code + WordPress MCP setup
- instawp.com/connect-claude-with-wordpress/ ; smartwp.com/wordpress-mcp/ ; adalike.com/claude-mcp-and-wordpress-7/
- wordpress.org/plugins/vibe-ai/ (Vibe AI MCP plugin)
- github.com/janzikmund/wp-adminer ; wordpress.org/plugins/pexlechris-adminer/ (Adminer)
- wordpress.org/plugins/file-manager-advanced/ ; wordpress.org/plugins/code-snippets/ ; wordpress.org/plugins/easy-code-manager/ (FluentSnippets)
- upress.io ; seresa.io (WP-CLI vs SSH)
- Medium — Pratik Machchar, "Built a Production-Ready WordPress Site in 3 Hours Using Google Antigravity"
- developers.googleblog.com — Google Antigravity ; antigravity.google
- charlesjones.dev ; techtimes.com ; owasp.org PromptInjection ; unit42.paloaltonetworks.com (AI agent security)
