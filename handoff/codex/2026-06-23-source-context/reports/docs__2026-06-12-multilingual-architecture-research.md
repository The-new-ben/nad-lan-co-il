# Multilingual (EN/FR/RU) Architecture for nad-lan.co.il — Cited Research
**Date:** 2026-06-12 · **Researcher:** Claude (deep-research agent, 17 searches / 8 fetches)
**Trigger:** owner requires project pages (3D picker) fully translatable, countrywide rollout.

## TL;DR decision
- **Polylang Pro** (€99 yr-1, ~€50 renewals — annual license, NOT SaaS) for content languages: CPTs, slug translation, meta sync, automatic hreflang, `/en/ /fr/ /ru/` subdirectories, RTL→LTR.
- **Module strings**: translate in PHP (`__()` + text domain `nadlan-config` + `load_plugin_textdomain`), emit ONE `nadlanI18n` object into the inline JS via `wp_localize_script` — no build tooling, works with our PHP-built inline JS today.
- **Units JSON meta stays language-neutral** (numbers/codes only) and is shared across translations via `pll_copy_post_metas` — one inventory, four languages, zero drift.
- **Machine translation with OUR OpenAI key**: gpt-4o-mini ≈ **$0.001–0.002 per 1,000 words per language** (100 articles × 3 languages < $1 total). Or Polylang Pro's built-in DeepL (free 500k chars/mo). Budget human review, not API cost.
- **Effort**: first fully-translated project page ≈ **22–30 h** (one-time string extraction ~10–14 h dominates); each subsequent project ≈ **2–4 h** (content only).

## Key findings (full citations at bottom)

### A. Plugin string i18n with PHP-heredoc + inline-JS architecture
- Heredoc trap: `__()` cannot run inside a heredoc — strings must be hoisted to variables first.
- Private plugins MUST call `load_plugin_textdomain()` (translate.wordpress.org auto-loading doesn't apply).
- `wp_set_script_translations()` keys its JSON files off the *enqueued file path md5* — our inline JS has no file path, so the automatic machinery doesn't map. **The pragmatic correct choice: translate in PHP, inject a `nadlanI18n` labels object** — exactly what `wp_localize_script` was designed for. Forward-compatible if JS ever moves to real files.

### B. Plugin comparison (2026)
| Plugin | Price | Verdict |
|---|---|---|
| Polylang Pro | €99/yr, 50% renewal | **WINNER** — meta sync filters fit units JSON exactly; Israeli agency Savvy standardizes on it; ~4 extra DB queries vs WPML's ~16 |
| WPML CMS | €99/yr 3 sites | Heavier queries; fine alternative |
| TranslatePress | €99–349/yr | Visual front-end model weak for structured JSON meta |
| Weglot | $17–$769/MONTH | EXCLUDED — subscription |
| MultilingualPress | €128–428/yr + multisite conversion | Overkill |

### C. Machine translation BYOK (no subscriptions)
- PolyTranslate AI / AutoPoly / AI Translate — free WP plugins taking OUR OpenAI key.
- Polylang Pro ships DeepL integration; **DeepL API Free tier = 500,000 chars/month at €0.**
- Unedited MT ranks poorly — human review is the real cost line.

### D. Real-estate practice
- Subdirectory-per-language dominates: Azorim `/en/`, DAMAC EN/AR/RU, Emaar country chooser, IsraelEstates HE/EN/FR/AR/RU.
- hreflang: ~75% of implementations contain errors; one bad tag invalidates the cluster; put it in the XML sitemap on large portals. Polylang emits it automatically — validate once `/en/` is live.
- **Prices/units stay numeric-shared**: facts not prose; per-language duplication guarantees drift (sold in HE, "available" in RU). Localize only labels + `Intl.NumberFormat(locale)` formatting. ₪ stays canonical — converted prices go stale and create legal ambiguity.

## Migration path (the 10 steps)
1. Wrap strings module-by-module starting with project-3d (heredoc → hoisted `__()` variables).
2. Inline JS: one `nadlanI18n` object per module via wp_localize_script.
3. Install Polylang Pro; languages he/en/fr/ru; subdirectory URLs.
4. Units JSON meta → `pll_copy_post_metas` (shared canonical blob).
5. Register module strings via `pll_register_string` (editable in wp-admin, no deploys).
6. MT pass: Polylang+DeepL free tier or PolyTranslate AI with our key.
7. Validate hreflang clusters when /en/ goes live.
8. Clone playbook addition: create 3 linked translation posts, meta auto-shared, MT pass, review, publish.
9. First page ≈ 22–30 h; subsequent projects ≈ 2–4 h.
10. Site-wide: repeat step 1 per module incrementally — pattern scales unchanged.

## Sources
developer.wordpress.org/apis/internationalization · developer.wordpress.org/reference/functions/wp_set_script_translations · /wp_localize_script · /load_plugin_textdomain · make.wordpress.org/core/2018/11/09/new-javascript-i18n-support · roots.io/stop-using-wp_localize_script-to-pass-data · polylang.pro/pricing + /documentation (strings-translation, multilingual-custom-post-types, synchronize-metadatas, deepl) · wpml.org/purchase · translatepress.com/pricing · weglot.com/pricing · multilingualpress.org · blogvault.net/multilingualpress-vs-wpml · oddjar.com/wordpress-translation-plugins-2026-comparison · webhosting.de multilingual performance · simplepotranslate.com polylang-vs-wpml-vs-translatepress-2026 · wordpress.org/plugins/polytranslate-ai · coolplugins.net/autopoly · wordpress.org/plugins/ai-translate · openai.com/api/pricing · searchvolume.io/resources/hreflang-tags-real-estate-seo · linkgraph.com hreflang guide · developers.google.com multi-regional · globalmediainsight.com Dubai real-estate sites · emaar.com choose-country-language · azorim.co.il/en · israel-estates.com · savvy.co.il Polylang guides
