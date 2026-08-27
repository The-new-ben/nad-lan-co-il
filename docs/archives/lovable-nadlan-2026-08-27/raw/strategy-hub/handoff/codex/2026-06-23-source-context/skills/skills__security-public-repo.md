# Security — this repo is PUBLIC

> **Notice to all agents:** `the-new-ben/nad-lan-co-il` is a public GitHub repository. Every commit is world-readable, indexable by GitHub code search, and likely cached. Treat every file you write as if it will appear in a Google search result tomorrow.

## NEVER commit

- WordPress login passwords.
- WordPress application passwords (e.g. format `xxxx xxxx xxxx xxxx xxxx xxxx`).
- API keys for OpenAI, Anthropic, Semrush, Ahrefs, MapTiler, Mapbox, Stadia, Cloudflare, Mailchimp, Gravity Forms license keys, Yoast Premium license keys.
- The owner's personal email beyond what's already in the public WHOIS, the owner's phone, the owner's home address.
- Real names or contact details of any partner lawyer, mortgage broker, agent, developer, or lead buyer.
- Negotiated prices (per-lead price, per-deal share, project-marketing fees).
- The owner's wife's family-law site URL, traffic numbers, or revenue.
- The owner's other portals' URLs and revenue.
- Lead data: any name, phone, email, or address belonging to a site visitor.
- Internal CRM exports, even anonymised.
- Database dumps, even staging.
- `.env` files, even templates with placeholder values that hint at the real ones.

## DO commit

- Strategy in the abstract: "negotiate per-lead pricing with mortgage brokers" — yes.
- Market estimates: "Israeli mortgage broker leads typically priced 150-400 ₪" — yes (it's public market knowledge).
- Architecture: CPT names, schema design, plugin names, theme structure — yes.
- Hebrew copy that is intended to ship to the public site — yes.
- Skill files: how things work, why they work that way.
- The owner's professional role as "a practicing Israeli lawyer" — yes (it's both relevant to E-E-A-T and not sensitive).

## Borderline — discuss before committing

- Specific city/neighborhood TAM analyses with revenue projections. Probably OK in aggregate; redact if it includes real partner pricing.
- The keyword target list. The current `strategy-master.md` exposes the cluster strategy. Marginal harm — Hebrew real estate SEO is competitive but the moats are content quality + lawyer E-E-A-T, not the keyword list.
- Yoast configuration snapshots. OK in general, but redact any author email or webmaster verification tokens.

## If something sensitive lands in history

Do not just delete and re-commit. Once it's in git history, it is on the public clone. Treat it as **leaked**:
1. Rotate the credential immediately (change the WP app password, revoke the API key).
2. Then optionally also rewrite history with `git filter-repo` + force push, but rotation is the real fix.
3. Log the incident in `site-state.md` with the date and what was rotated.

## Recommended (owner decision)

Consider making this repo **private** before any of the following happens:
- Revenue projections with real partner names land in `monetization-*.md`.
- The CRM or inquiry data model gets populated with real schemas tied to a specific partner.
- The competitor analysis sharpens into "here is exactly how we will displace X."

Until then, public is acceptable and has a real upside: agents in fresh sessions can `git clone` without auth.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-7)._

