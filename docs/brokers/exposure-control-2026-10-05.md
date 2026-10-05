# HAD-436: broker exposure control, Gili's mini-site, Gili on Kikar Hamedina (spec and build plan, 5.10.2026)

Prepared by an Opus 5.5 sub-agent for main. **Design only.** Nothing was deployed, pushed, committed or written to the live
site; no secret was read. Live reads were anonymous (curl, raw HTML, 5.10.2026 ~18:50-19:10 UTC, live `nadlan-config`
**1.72.429** per `/wp-json/nadlan/v1/health`). Evidence classes below: **code** = repo file:line, **live** = anonymous raw
HTML or public REST, **unverified** = said so.

Drafts for main's review (not in `plugins/`):
- `docs/brokers/exposure-draft/broker-exposure.php`: the module (store, read API, admin screen, preview, renderers,
  status flips, audit, purge). `php -l` clean (PHP 8.3).
- `docs/brokers/exposure-draft/smoke-test.php`: the module's logic with WordPress stubbed: `php smoke-test.php` gives
  `ok=32 bad=0` (legacy parity, the licence gate, the admin preview, the five languages, raising and lowering Gili,
  the status flips, the purge). It is a logic test only. It is not a live proof.

---

## 0. בקצרה, לבן

- **מה יש היום:** האתר של מיטל בנוי ביד, והאתרים של מתווכים שמצטרפים לבד נבנים על ידי המנוע. יש ריבוע מתווך ליד הבמה בעמודי
  הפרויקט, אבל רק בעברית. מיטל מופיעה רק בריינבו. בכיכר המדינה יש היום רק הריבוע הריק "רוצה להופיע כאן?". אין היום מסך אחד
  שקובע איפה מתווך מופיע: חלק נקבע בקוד, חלק לפי מסלול, וחלק לפי נעיצה.
- **מה מוצע:** מסך אחד בניהול האתר בשם "חשיפת מתווכים". לכל מתווך בוחרים רמה אחת מחמש: מוסתר, אתר בקישור ישיר בלבד, במדריך
  המתווכים, גם בעמודי פרויקט שסימנת, ומומלץ. לכל פרויקט יש תיבה, ולידה תיבה לכל אחת מחמש השפות. כל רמה כוללת את מה שמתחתיה.
  כל שמירה נרשמת ביומן, ומנקה מהמטמון את העמודים שהשתנו.
- **גילי:** מתחיל במצב "מוסתר", כלומר רק מנהלים רואים. כיכר המדינה כבר מסומנת לו בחמש השפות, ולכן ברגע שתעלה אותו הוא יופיע
  שם. אי אפשר להעלות אותו לרמה ציבורית לפני שיש מספר רישיון בכרטיס ולפני שסימנת "בדקתי את הרישיון". את האתר שלו בונים רק מהאתר
  שלו: שם המשרד, הכתובת, הטלפון והוואטסאפ, האזורים והשותפים. אין בו נכסים, מחירים, ציטוטים או תמונות שלו.
- **בעמוד כיכר המדינה:** הריבוע שלו יופיע ליד הבמה, אחרי הכותרת, הפסקה, הכפתורים והבמה. שורה קצרה תופיע גם בפרק "למכירה ולהשכרה",
  המקום שאליו מוביל הכפתור "דירות למכירה במגדלים". לחיצה פותחת את האתר שלו. באתר שלו יש רק קישור לעמוד הפרויקט, בלי להעתיק ממנו
  טקסט.
- **מה מחכה רק לך:** הרשימה בסוף המסמך.

---

## 1. MAP: what exists today

### 1.1 Where each piece lives (plugin file vs live snippet only)

The plugin loads its modules from one list, `plugins/nadlan-config/nadlan-config.php:33-38` (**code**). The three broker
platform modules are **not** in that list: they run on the live site only as Code Snippets, and their source files sit in
`inc/` for the runner `scripts/broker-drop/deploydrop.py:7-9,31-32` (**code**).

| Piece | Source | How it reaches the live site |
|---|---|---|
| Brokers list on `/brokers/`, the menu link for the old header, the broker-site CSS | `inc/brokers-list.php` | plugin module |
| Placements (a broker's ad card on chosen page paths, with dates) | `inc/placements.php` (CPT `nadlan_placement`) | plugin module |
| BrokerSquare, BrokerSlot, the project rail | `inc/project-stage.php:603-644, 761-763, 837, 1154-1157` | plugin module |
| Owned-listing rule (no portal layers on a broker's listing) | `inc/property-owner.php:44, 86, 180` | plugin module |
| Network card, `/professionals/`, register-verified badge | `inc/directory.php:130, 211` | plugin module |
| Profile page, WA digits, person name, calendar | `inc/professional-profile.php:65, 145, 153` | plugin module |
| Endorsements ("המלצות") | `inc/pro-network.php:234` | plugin module |
| Admin control (pin, boost, reserved slot, promo date) + audit log | `inc/admin-control.php:36-38, 189-216, 875-878` | plugin module (flag `nadlan_feature_admin_control`, on live per health) |
| Header mega-menu (Hebrew) | `inc/home-v3.php:104-200` (brokers link at `:176`) | plugin module |
| Home pros band paid slot | `inc/home-v2.php:238-246` (`sponsored_until`) | plugin module |
| REST privacy (hides `nl_tier`, `is_pinned`, `nl_drop_on`, ...) | `inc/rest-privacy.php:21-23` | plugin module |
| **Drop box engine + engine-built broker sites** (`x-broker-drop`, id 687) | `inc/broker-drop.php` (v1.1.3, `:33`) | **live snippet only** |
| **Self-serve join** (`x-broker-join`, id 699) | `inc/broker-join.php` | **live snippet only**; live copy `docs/qa/live-read/20261003T205056Z/snippet-699.php` is identical to the repo file (diff empty, **code**) |
| **Owners' wizard** `/post-listing/` (`x-owner-wizard`, id 707) | `inc/owner-wizard.php` | **live snippet only**; live copy `.../20261003T205055Z/snippet-707.php` identical |
| hreflang meta to REST (684) and the hreflang printer for listing pairs (685) | `snippets/nl-i18n-hreflang-print.php` (685) | **live snippets only** (skill `broker-minisite` lines 48-52) |
| Meital's handcrafted site and listing pages | `handoff/meital-2026-09-17/runners/meital_site.py` (`--site/--listings/--hreflang/--journey/--verify`, `:581-681`) | REST writes of post content, no plugin code |

Note: no live-read copy of 687 exists under `docs/qa/live-read/`; main should read 687 through the bridge before
assuming `inc/broker-drop.php` is its exact text.

The repo's `nadlan-config.php:19` still says 1.72.372 while live is 1.72.429. The release runners bump the version
"on the live text" (`scripts/project-stage/deploy429.py:1-8`), and `inc/project-stage.php` in the working tree is newer
than the last live-read copy (`docs/qa/live-read/20261003T000310Z/inc/project-stage.php`, 1,635 lines, against 1,708
locally). **Every hunk below must be applied to the live text, read through the bridge and pinned by MD5.** The local file
is not the live text.

### 1.2 Broker mini-sites: two kinds, one set of classes

- **The record:** a `nadlan_professional` post with `profession=metavech`. The card meta are registered for REST at
  `inc/broker-drop.php:40-58`: `nl_drop_on, nl_name_he/en/ru, nl_brand_en, nl_gender, nl_site_he/en/ru/fr, nl_auto_publish,
  nl_langs, nl_tier, nl_slug, nl_hero, nl_areas_en/ru/fr, nl_bio_en`. The page and property meta are `nl_broker_id,
  nl_card_key, nl_twin, nl_twins, nl_status, nl_broker_site, nl_broker_auto, nl_lang, nl_drop_id`. The secret upload token
  is `_nl_drop_token` (protected, stripped from REST at `:64-76`). The broker model is built at `nl_drop_broker()`
  `:91-136`.
- **Handcrafted site** (Meital): a page with `nl_broker_site=<professional id>`. The x-broker-drop filter injects new drop
  listings into `<ul class="nlb-grid">` and fixes the counters (`:3090-3121`). The page itself is never rewritten.
- **Engine-built site** (self-serve joiners): a page with `nl_broker_auto=<id>`, created under `/brokers/` or
  `/<lang>/brokers/` by `nl_drop_site_ensure()` `:2531-2563`. It is rewritten after every listing, sale or price change by
  `nl_drop_site_sync()` `:2565-2593` through `nl_drop_site_html()` `:2957-3084`. The rewrite covers the nav, hero, about,
  listings or the empty state, contact, licence line, RealEstateAgent JSON-LD, and the mobile bar. The licence line is
  `nl_drop_licence_line()` `:1670-1676`. The words in four languages are `nl_drop_t()` from `:227`.
- **Drop box**: `/drop/<token>/` (`:3145-3151`). Admin metabox "תיבת נכסים" on the card (`:3421-3479`): on/off, rotate,
  languages, tier (free/pro/studio), names, site ids, gender, auto-publish.
- **Join** (699): `nl_join_registry()` checks the licence against data.gov.il (`inc/broker-join.php:145-174`).
  `nl_join_create()` (`:461-532`) creates a **published** card with `source=broker_join`, `claim_status=verified`,
  `verified_at=time()`, `nl_tier=free`, `nl_langs=he,en`, and a **published** Hebrew engine site. Joiners are public at
  once today.
- **Owners' wizard** (707) runs on the same engine, with no licence and no site. It is not a broker surface.
- **Cache discipline already in the engine**: `nl_drop_purge()` `:1923-1930` (`clean_post_cache`, `litespeed_purge_post`,
  `litespeed_purge_url`).

### 1.3 Meital's site and listings (live + public REST)

| What | Value |
|---|---|
| Card | `nadlan_professional` **7833**, slug `meital-katzir`, `source=broker_minisite`, licence 3131540, `verified_at=1790245052` (24.9), `nl_site_he=7644`, `nl_site_en=7804`, `nl_langs=he,en,ru,fr`, `nl_hero=7798` (**live**, public REST) |
| Hebrew site | page **7644** `/brokers/meital-katzir/` (child of 7645 `/brokers/`), H1 "מיטל קציר", nav "הנכסים · למכירה · להשכרה · האזורים · עליי · יצירת קשר · English", 11 `nlb-lcard`, hreflang he/en/x-default (**live**) |
| English site | page **7804** `/en/brokers/meital-katzir/` (child of 7803 `/en/brokers/`) (**live**) |
| Listings | Hebrew on `nadlan_property` with `nl_broker_id` (counted by `nadlan_bl_active_listings()` `inc/brokers-list.php:59-66`); English as pages under `/en/brokers/meital-katzir/<slug>/` (7 found by `tools/gsc/url_word_audit.py --token brokers`) |
| Owned rule | `inc/property-owner.php:44-86`: a property with `nl_broker_id` / `nl_broker_site` gets no portal layers; "similar" = her other listings (`:205-206`) |
| On a project page | Rainbow Hebrew only: `nadlan_ps_config()['rainbow-tel-aviv']['rail'] = array( 7833 )` (`inc/project-stage.php:52`). Live Rainbow he rail = her square + the empty slot; live Rainbow en rail is empty (**live**) |
| On /brokers/ | top BrokerFeatureCard (portrait, "מתווכת · נדל״ן על הים · תל אביב יפו", licence ✓ "מאומת בפנקס", areas, "11 נכסים", "תיאום סיור", "לעמוד המתווכת") (**live**) |
| Footer legal line | "האתר של מיטל קציר ב-nad-lan.co.il. המידע אינו הצעה מחייבת, שמאות או ייעוץ. צילומים: ..." (**live**) |

### 1.4 The directory and the menu

- `/brokers/` = page **7645**. `inc/brokers-list.php:184-189` puts the list above the page's own offer and turns the
  offer's H1 into an H2. Option off-switch `nadlan_brokers_list`. `nadlan_bl_brokers()` `:27-56` decides who shows:
  published `metavech` cards, not demos. **Featured** = `is_pinned` or `nl_tier` in pro/studio (`:33-35`). Everyone else is
  grouped by city. Featured uses BrokerFeatureCard `:74-118`, and the rest use the network card (`nadlan_dir_card`,
  `inc/directory.php:211`) since release 364 (`scripts/project-stage/deploy364.py:1-6`, "BrokersNetwork v99").
- `/en/brokers/` (7803), `/ru/brokers/`, `/fr/brokers/` are offer pages only, with no list (**live**: no `nlds-bfeat` on
  `/en/brokers/`).
- **Menu (Hebrew header)**: "אנשי מקצוע" > column "המאגר" > "כל המאגר · מתווכים (/brokers/) · הצטרפות למאגר"
  (`inc/home-v3.php:173-177`). No broker is named in the menu today. The old header (`nlpc-primary-nav`) gets "מתווכים" from
  `inc/brokers-list.php:192-197`. It skips `/en|ru|fr|ar/` paths but not `/projects/<slug>-en/`. As a result, the
  English Kikar page's header "Brokers" points to the **Hebrew** `/brokers/` (**live**, `projects/hamedina-en`). This is a
  gap, filed in section 1.8.
- `/professionals/` lists every published card, brokers included (`inc/directory.php`). A private card is absent
  everywhere and its profile returns 404 for visitors (WordPress private status).

### 1.5 Brokers on project pages today

- **BrokerSquare** `nadlan_ps_square()` (`inc/project-stage.php:603-632`): a published card's photo or monogram, the
  "פרסומת" tag, the name linked to the Hebrew site (`nl_site_he` when published, else the card), role and up to 3 areas,
  "רישיון תיווך N", the recommendations count, and **"התייעצות בוואטסאפ" straight to the broker** (`wa.me/<broker>`). The
  square is Hebrew-only text. It has no site button; the name is the link.
- **BrokerSlot** `nadlan_ps_slot()` (`:634-644`): "רוצה להופיע כאן?" → `/brokers/#join`. It is printed on Hebrew pages only
  (`:763`, `:1156`).
- **The rail's source** is the stage config's `'rail'` per project: Rainbow `array(7833)` (`:52`); DUO, Dimri, Ashira and
  Kikar `array()` (`:134, 219, 270, 345`). On every language twin the rail is emptied: `$memo['rail'] = array()` in
  `nadlan_ps_current()` (`:577-580`).
- **Where the rail sits:**
  - On the four classic stage pages the grid is "hero stage rail / lead stage rail / cta stage rail" on desktop. On a phone
    the rail comes after deals (`:1517`, `:1563-1564`).
  - On the Kikar **world** pages the rail is always last in the top block: "hero stage / lead stage / cta stage / below /
    facts / deals / rail" (`:1286`, `:1294`). That is after H1, answer, CTAs, stage, map and facts, so it is content-first
    by construction.
- **Click tracking:** `assets/project-stage/bridge.js:33-39` sends `pro_click` / `whatsapp_click` for `[data-nlps-ev=rail]`.
  World pages load **no bridge.js** (`inc/project-stage.php:1012-1014`), so a rail click on Kikar is not measured today.
- **Placements** (`inc/placements.php`): a managed "ad card on chosen page paths" (who, where, when, position after an H2).
  Labelled "פרסומת". Hebrew only (`:160-161`). One placement per page. Views and clicks go to the private insights table
  (`place_view`, `place_click`, `inc/insights.php:128`). It is another place a broker can show, outside any exposure
  control.
- **Home pros band paid slot** (`inc/home-v2.php:238-246`, `sponsored_until`). It is a third independent switch.

### 1.6 Existing on/off and level settings (none of them is "one source of truth")

| Setting | Where | Effect |
|---|---|---|
| `nadlan_brokers_list` option | `inc/brokers-list.php:185,193` | the list on /brokers/ and the old header link |
| `nl_tier` free/pro/studio (drop metabox) | `inc/broker-drop.php:3441-3443, 3477-3478` | featured on /brokers/ when pro/studio |
| `is_pinned` (admin control) | `inc/admin-control.php:36-38, 757-759` | featured on /brokers/ |
| `boost_multiplier`, `reserved_slot`, `promo_until`, `priority_weight` | `inc/admin-control.php:30-38, 654-690` | directory ordering, with expiry by cron |
| stage config `'rail'` | `inc/project-stage.php:52...345` | which professional is on which project page (code, Hebrew only) |
| `nadlan_placement` posts (`pl_active`, dates, paths) | `inc/placements.php` | ad cards on content pages |
| `sponsored_until` | `inc/home-v2.php:242` | the home band's paid slot |
| post status of the card / site | WordPress | private = nowhere public |
| `nl_drop_on` | drop metabox | the upload link works or not |

### 1.7 Kikar Hamedina today (live, 5.10)

- `/projects/hamedina/`: rail = **the empty BrokerSlot only** (no square). The rail is not printed on `-en/-fr/-ru/-ar`.
- The hero's second button "דירות למכירה במגדלים" jumps to `#nlws-sale` (`inc/project-stage.php:1143`). That is
  `<section class="nlws" id="nlws-sale">` in the article, in all five languages. It says there is no sales office and that
  owners resell, usually through brokers, then links to the brokers directory in the page's language (`/brokers/`,
  `/en/brokers/`, `/ru/brokers/` ...) (**live**). **It is the page's own broker-intent spot.**
- Outline (he): H1, then H2 virtual tour (sr-only), map, deals, film, prices, facts, which tower, apartments, facilities,
  prices, costs, how to buy, **"מגדלי כיכר המדינה למכירה ולהשכרה"** (#nlws-sale), occupancy, history, park, around, map,
  FAQ (**live**).
- Demand (`docs/research/2026-10-05-kikar-press-facts.md`): "מגדלי כיכר המדינה" 260/month is the hub's head term. Broker
  variants have no measurable volume.

### 1.8 Gaps found while mapping (each one should get a Linear child per the no-silent-gaps law)

1. The English Kikar header "Brokers" link goes to the Hebrew `/brokers/` (`inc/brokers-list.php:194-196` skips only
   `/en/...` paths).
2. Kikar rail clicks are not measured (no bridge.js on world pages). The draft fixes this for broker squares.
3. Rainbow's broker is hard-coded in the stage config (`:52`). The exposure store replaces it.
4. The private preview (`minisite-preview.html`) repeats the hub's facts: towers, 453 apartments, the deals at 9.58-10.63
   million ₪, 65,000 ₪/m². That copy would cannibalise `/projects/hamedina/` and **must not** go into Gili's real site
   (section 3).
5. Brokers can appear through four independent switches (tier, pin, stage config, placements, plus the home slot). After
   this release the placements and the home slot are still outside the store. See open question 7.

---

## 2. DESIGN: the exposure control

### 2.1 The ladder (each level includes the ones under it)

| Rank | Key | Admin label | What the public sees |
|---|---|---|---|
| 0 | `hidden` | מוסתר: רק מנהלים רואים | nothing. The card and every site page are **private** (404 for visitors, out of the sitemap). Admins see everything, and `?nlbx_preview=<id>` shows the placements |
| 1 | `link` | אתר בקישור ישיר בלבד | the site pages are public by URL. nad-lan links to them from nowhere: no directory, no menu, no project page. The card stays private. Indexing is unchanged: **no noindex is added** (the owner's indexing law). |
| 2 | `listed` | במדריך המתווכים | + the card is public: a city row on `/brokers/`, `/professionals/`, the profile page |
| 3 | `projects` | גם בעמודי הפרויקטים שסומנו | + the BrokerSquare in the rail and the line in `#nlws-sale` on the ticked projects, in the ticked languages |
| 4 | `featured` | מומלץ: ראשון בכל מקום | + the BrokerFeatureCard at the top of `/brokers/`, first in every rail; + a named header-menu link when "בתפריט" is ticked |

### 2.2 Data model: one autoloaded option

```php
// option nadlan_broker_exposure (autoload yes; one get_option per request, memoised in nadlan_bx_store())
array(
  'v' => 1,
  'brokers' => array(
    7833 => array( 'level' => 'featured', 'projects' => array( 'rainbow-tel-aviv' => array( 'he' ) ),
                   'licence_ok' => 1, 'licence_note' => 'register record 15569, verified_at 24.9.2026',
                   'menu' => 0, 'order' => 10, 'updated' => 1791230000, 'by' => 1, 'log' => array( /* last 20 changes */ ) ),
    <gili> => array( 'level' => 'hidden', 'projects' => array( 'hamedina' => array( 'he','en','fr','ru','ar' ) ),
                   'licence_ok' => 0, 'licence_note' => 'not in the active register, 3.10.2026 (HAD-394)',
                   'menu' => 1, 'order' => 20, ... ),
  ),
)
// plus: nadlan_bx_on ('1'; '0' = every surface back to today's code path), nadlan_bx_since (release time),
//       nadlan_bx_join_level ('listed'), nadlan_bx_strip ('1': the line in #nlws-sale)
```

Why one option and not post meta:
- It is one read per request.
- It is one value to back up and restore (the rollback).
- The question "who is on project X" needs no meta query over serialized arrays.
- The screen is its only writer.

Project keys are the stage config slugs without the language suffix: `rainbow-tel-aviv, duo-tel-aviv,
dimri-yama-sde-dov, ashira-sde-dov, hamedina` (`inc/project-stage.php:42,125,210,262,321`). These are the pages that print
the rail. Each project carries its own languages, so ticking Kikar covers `/projects/hamedina/` and `-en/-fr/-ru/-ar`.
Meital's Rainbow stays Hebrew-only until Ben ticks more. Nothing changes on Rainbow's language pages by surprise.

### 2.3 The licence gate (fail closed)

A public level (rank ≥ 1) needs **both**:
- a `license_number` on the card;
- **either** the screen's "בדקתי את הרישיון" tick (with a note on how and when it was checked) **or** a register
  verification (`verified_at`, or a register source: `nadlan_dir_registry_verified()`, `inc/directory.php:130-133`).

The save refuses anything else (`nadlan_bx_save()` returns `licence`). The radios above "מוסתר" are disabled while the
licence number is empty. The screen can offer "בדיקה בפנקס" through `nl_join_registry()` when 699 is active.

This is the rule for Gili: not found in the active register (`docs/brokers/biyar-2026-10/biyar-review.md:85-90`), so he
stays hidden until Ben confirms the licence and enters it. Reg. 19(a) needs the licence on every publication. The gate
does not apply to **legacy** brokers (no entry, card older than the release), so `/brokers/` keeps every card it shows
today.

### 2.4 Defaults: new brokers start hidden, old ones keep today

- **No entry and the card is older than `nadlan_bx_since`:** today's behaviour, exactly. Published = listed. Pinned or
  pro/studio = featured. The stage config rail applies on Hebrew pages.
- **No entry and the card is newer than the release:** `hidden`. Exception: a self-serve joiner (`source=broker_join`)
  starts at `nadlan_bx_join_level`, `listed` by default. The join screen tells the broker "האתר שלכם באוויר"
  (`inc/broker-join.php:45`), so hiding joiners silently would break that promise. **Ben decides** (open question 3).
- **Adding a broker on the screen** starts from his current effective level. Adding never demotes.

### 2.5 The read API (every surface calls it; nothing else decides)

Draft: `docs/brokers/exposure-draft/broker-exposure.php`.

| Function (draft line) | Answers | Used by |
|---|---|---|
| `nadlan_bx_can( $pro, $surface, $project, $lang )` (`:186`) | `site / card / directory / project / featured / menu`, with the licence gate and the preview | everything below |
| `nadlan_bx_project_brokers( $slug, $lang )` (`:210`) | ordered ids for a project page (featured first, then `order`, at most 3, nobody without a name in that language) | `nadlan_ps_current()` hunk |
| `nadlan_bx_square_html( $pro, $ps )` (`:327`) | BrokerSquare in 5 languages. The Hebrew output keeps today's content (role, areas, licence, recommendations, WA) and **adds** the office name and a "לאתר של <first name>" button | `nadlan_ps_square()` hunk |
| `nadlan_bx_strip_insert( $html, $ps )` (`:399`) | the line inside `#nlws-sale` | `nadlan_ps_compose()` hunk |
| `nadlan_bx_site_url( $pro, $lang )` (`:282`) | the site in the reader's language → English → Hebrew (Arabic → English). A private page only in the preview | square, line, menu, `/brokers/` |
| `nadlan_bx_menu_links( 'he' )` (`:424`) | featured + "בתפריט" + licence → (name, site) | `home-v3.php:176` hunk |
| `nadlan_bx_rank`, `nadlan_bx_publishable`, `nadlan_bx_preview`, `nadlan_bx_projects_of` | building blocks | |
| `nadlan_bx_save( $pro, $in )` (`:536`) | the **only writer**: validate, gate, store, flip statuses, audit, purge | the screen |
| `nadlan_bx_seed( $entries )` (`:600`) | one-time seed, called by the release runner through its bridge, never on load | runner |

### 2.6 The wp-admin screen: NadLan Ops › "חשיפת מתווכים"

`add_submenu_page( 'nadlan-ops', ... 'manage_options', 'nadlan-broker-exposure' )`. The parent menu is at
`inc/ops-dashboard.php:16-19`. Draft `:617-726`. One row per broker, one save button per row, so a slip never changes
two brokers.

```
חשיפת מתווכים                                    [הוספת מתווך: שם או מספר רישיון] [חיפוש]
┌───────────────┬──────────────┬───────────────────────────┬──────────────────────────┬─────────────┬────────────────┬────────┐
│ מתווך          │ רישיון        │ רמה                        │ עמודי פרויקט              │ תפריט וסדר   │ תצוגה למנהל     │        │
├───────────────┼──────────────┼───────────────────────────┼──────────────────────────┼─────────────┼────────────────┼────────┤
│ מיטל קציר      │ 3131540      │ ○ מוסתר                    │ ☑ ריינבו  ☑he ☐en ☐fr ☐ru ☐ar │ ☐ בתפריט    │ הכרטיס          │ [שמירה] │
│ נדל״ן על הים   │ מאומת בפנקס  │ ○ אתר בקישור ישיר בלבד      │ ☐ DUO                     │ סדר [10]    │ האתר / באנגלית  │ שונה... │
│ #7833 publish │ ☑ בדקתי       │ ○ במדריך                    │ ☐ דימרי ים  ☐ אשירה         │             │ /brokers/      │        │
│               │ [הערה]        │ ○ גם בעמודי הפרויקטים        │ ☐ כיכר המדינה              │             │ ריינבו (תצוגה)  │        │
│               │              │ ● מומלץ                     │                          │             │                │        │
├───────────────┼──────────────┼───────────────────────────┼──────────────────────────┼─────────────┼────────────────┼────────┤
│ גיל נסים       │ חסר           │ ● מוסתר                    │ ☑ כיכר המדינה ☑he ☑en ☑fr ☑ru ☑ar │ ☑ בתפריט   │ האתר (פרטי)     │ [שמירה] │
│ ה׳ באייר נדל״ן │ ☐ בדקתי       │ (רמות ציבוריות נעולות:      │                          │ סדר [20]    │ כיכר המדינה    │        │
│ #<id> private │ [לא בפנקס 3.10]│  "רמה ציבורית נפתחת רק אחרי בדיקת רישיון") │                │             │ (תצוגה)        │        │
└───────────────┴──────────────┴───────────────────────────┴──────────────────────────┴─────────────┴────────────────┴────────┘
```

- **The rows:**
  - every broker with an entry;
  - every broker with a site, a `broker_minisite`/`broker_join` source, a pro/studio tier or a pin;
  - the search results (name, or a licence number).
- **"תצוגה למנהל":** the card and the site pages open as themselves (WordPress shows private pages to admins). `/brokers/`
  and every ticked project open with `?nlbx_preview=<id>`. The page shows exactly what the entry asks for. A red badge
  "תצוגה למנהל בלבד" sits on any square shown only because of the preview. The page is never cached
  (`litespeed_control_set_nocache` + `nocache_headers`).
- **The screen's header text says it plainly:** lowering to "מוסתר" makes the site and the card private, which also takes
  them out of the sitemap. That is Ben's own action, never an agent's.
- The **design-first law** applies: the screen, the localized square and the line go into the design system artifact
  first (section 5.0).

### 2.7 What a save does (draft `nadlan_bx_save()` `:536-597`)

1. **Gate:** the licence (2.3). Refuse with a notice and write nothing.
2. **Store:** write the option, and push a log row: from, to, projects, time, user (the last 20 rows per broker).
3. **Statuses:**
   - the card: `publish` from rank 2, else `private`;
   - the site pages (`nl_site_he/en/ru/fr`): `publish` from rank 1, else `private`;
   - only publish ↔ private, never a draft or the trash.
   - The flip is a direct `posts.post_status` update plus `clean_post_cache` and `wp_transition_post_status`. It does
     **not** re-save the content: a broker page holds `<style>` and JSON-LD that a kses re-save could strip. The previous
     statuses are stored in the log row, for an exact rollback.
   - Side effects checked:
     - IndexNow does **not** fire. It hooks `save_post` (`nadlan-config.php:370-380`), and the flip does not save.
     - The generic sitemap ping does fire on a page's first publish (`inc/sitemap-ping.php:45-49`). It is throttled hourly,
       and Google retired that ping endpoint in 2023, so it is effectively a no-op. It is still listed in open question 6,
       because indexing is Ben's call.
4. **Audit:** `nadlan_admin_control_audit()` (`inc/admin-control.php:189-216`) with action `broker_exposure`, the old and
   new level, projects and menu. It lands in the same journal Ben already has under "בקרת לקוחות".
5. **Purge:**
   - Always, targeted: the card, the site pages, the old ∪ new project pages × 5 language twins, `/brokers/` (4
     languages), `/professionals/`. Each gets `clean_post_cache`, `litespeed_purge_post` and `litespeed_purge_url`, the same
     calls as `nl_drop_purge()`.
   - Plus `litespeed_purge_all` when the change crosses the directory line (rank 2), the featured line (rank 4) or the menu
     box. The header menu is on every page, and `/professionals/?profession=...` has query-string variants. These changes
     are rare.
   - Release runners already purge the same way (`deploy429.py:471-474`).

### 2.8 Five languages

- **Names:** Hebrew uses `nl_name_he`. Russian uses `nl_name_ru`, else `nl_name_en`. English, French and Arabic use
  `nl_name_en`. A broker with no `nl_name_en` is **skipped** on every language page. Hebrew never reaches a language page,
  which keeps `tools/lang_pages_check.py` green.
- **Office:** `company_name` (he) / `nl_brand_en` (others).
- **Areas:** `areas_served` / `nl_areas_<lang>` (Arabic uses English). Any Hebrew item is filtered off non-he pages.
- **Site link:** the reader's language → English → Hebrew. Arabic always goes to English: the engine has no Arabic site
  (`nl_drop_langs()` = he, en, ru, fr).
- **Words** (`nadlan_bx_t()`, draft `:235-257`, DRAFT strings: the language gate and a native read come before release):

| key | he | en | fr | ru | ar |
|---|---|---|---|---|---|
| ad label | פרסומת | Advertisement | Publicité | Реклама | إعلان |
| role | מתווך / מתווכת (today's label) | Licensed real estate broker | Agent immobilier agréé / Agente immobilière agréée | Лицензированный риелтор | وسيط عقاري مرخّص / وسيطة عقارية مرخّصة |
| licence | רישיון תיווך N | Licence no. N | Licence n° N | Лицензия № N | رخصة رقم N |
| WA button | התייעצות בוואטסאפ (today's) | Chat on WhatsApp | Écrire sur WhatsApp | Написать в WhatsApp | تواصل عبر واتساب |
| site button | לאתר של <שם פרטי> | <First>’s site | Le site de <Prénom> | Сайт: <Имя> | موقع <الاسم> |
| line heading | מתווכים שפעילים ב<פרויקט> | Brokers active in <project> | Agents immobiliers actifs : <projet> | Риелторы проекта «<проект>» | وسطاء عقاريون يعملون في <المشروع> |
| WA text | today's Hebrew sentence | Hello <first>, I saw your card on the <project> page on nad-lan.co.il and would like to talk | (fr) | (ru) | (ar) |

- The rail's aria-label per language already exists (`inc/project-stage.php:1028-1073`, key `rail`).
- **WhatsApp wording law:** "ייעוץ חינם" stays on the floating bar only (`tools/wa_wording_check.py:1-4`). The broker
  buttons never use it.

### 2.9 Caching

- Anonymous HTML is decided on the server. A hidden broker is never in it, so no cached page can leak him.
- The admin preview is a query string and is marked no-cache. LiteSpeed does not serve cached pages to logged-in users by
  default (**unverified** for this host's settings; the runner check "anonymous fetch has no Gili" covers it).
- On save: 2.7 step 5. On release: the runner's usual `purge` op.
- The Hebrew header's counts are a one-hour transient (`inc/home-v3.php:58-73`). The menu links are built per request and
  live inside the cached page, hence `purge_all` on a menu change.

### 2.10 "Never present as a broker" (Brokers Law s.2(c), reg. 19(a))

- **Every broker surface carries the broker's own name, the broker status and the licence number** (square:
  role + "רישיון תיווך N"; line: `nadlan_bx_licence_line()`; site footer: the licence line). No licence means no public
  surface (2.3).
- **Every placement says it is the broker's:** the "פרסומת" / "Advertisement" tag on the square and on the line.
- **WhatsApp and calls go straight to the broker** (`wa.me/<broker phone>`). nad-lan never relays, screens, quotes prices or
  books viewings for him. The lead belongs to him (`docs/brokers/biyar-2026-10/call-prep-he.md:51-54`). Leads from
  nad-lan's own forms are never forwarded without consent given in the form itself.
- **The BrokerSlot stays next to him** ("רוצה להופיע כאן?" → `/brokers/#join`). This keeps the page fair: any broker can
  join on the same terms, so it does not read as nad-lan recommending one office.
- **Words never printed** on the square, the line, the menu or his site:
  - Hebrew: עמלה, דמי תיווך, הנחה בעמלה, אחוז, המתווך שלנו, המתווך של nad-lan, נציג nad-lan, בלעדי ל-nad-lan;
  - English: commission, our broker, our agent, exclusive to nad-lan.
- **Payment, if any, is a fixed fee only** (`.claude/skills/broker-minisite/SKILL.md:79`). Nothing in the build mentions
  money. No payment model is decided with Gili (open question 8).
- **Gili's site footer** keeps the engine's legal line ("האתר של <שם> ב-nad-lan.co.il. המידע אינו הצעה מחייבת, שמאות או
  ייעוץ.") and adds the preview's line: "nad-lan היא פלטפורמת פרסום ואינה משרד תיווך, והפניות מגיעות ישירות למשרד."

### 2.11 Migration at release (byte parity for every broker shown today)

The seed (through the bridge, `nadlan_bx_seed()`) sets:
- `nadlan_bx_since = now`;
- **Meital 7833:** `featured`, projects `rainbow-tel-aviv: [he]`, `licence_ok=1` (note "verified_at 24.9.2026, register
  15569"), `menu=0`, `order=10`.

No other entries are seeded: every other broker stays on the legacy path. Gili's entry is written by the build step, after
his card exists.

Intended visible change on Rainbow (he), declared in the receipt: Meital's square **gains** her office name on the role
line and a "לאתר של מיטל" button. Nothing is removed (the additive law).

---

## 3. DESIGN: Gili's mini-site (from biyar.co.il only)

Read anonymously on 5.10.2026: `/`, `?page_id=60` (about), `?page_id=62` (projects), `?page_id=64` (contact), `?p=1`
(Kikar), `?page_id=926/932/937` (sale/rent/commercial, all empty), and `?page_id=2033&lang=en` (English home). Only
published business details are used.

### 3.1 Addresses and records (URL word law checked)

`tools/gsc/url_word_audit.py --token` on the live sitemap: `heh` 0, `biyar` 0, `gil` 0, `nissim` 0. `hamedina` is owned by
the 5 Kikar pages, so **no broker URL may carry `hamedina` or `kikar`**.

| Record | Address | Status at build |
|---|---|---|
| Card (`nadlan_professional`) | `/professionals/heh-biyar/` | **private** |
| Hebrew site (page, parent 7645) | `/brokers/heh-biyar/` | **private** |
| English site (page, parent 7803) | `/en/brokers/heh-biyar/` | **private** |

The pattern is the same as Meital's (card slug = site slug). The slug assumes the office is the brand; if Ben says the
site goes in the licence holder's name, the slug follows (open question 2).

### 3.2 Fields: source or placeholder

| Field | Hebrew | English | Source (S) / Placeholder (P) |
|---|---|---|---|
| Office (brand, H1) | ה׳ באייר נדל״ן | Heh B’iyar Real Estate | S: site title and logo; English from `?page_id=2033&lang=en` |
| People | גיל נסים, עובד זנגי | Gil Nissim, Oved Zangi | S: about page (he) / English home |
| Whose site it is (name on the licence line) | — | — | **P: the licence holder's name and licence number, from Ben** (Gil not found in the register; "זנגי עובדיה חי" exists, unconfirmed) |
| Address | ה׳ באייר 4, תל אביב | 4 Heh B’iyar St, Tel Aviv | S: contact page |
| Office phone | 03-5333307 | +972 3-533-3307 | S: contact page |
| WhatsApp | 054-2442555 (`wa.me/972542442555`) | same | S: the floating WhatsApp button on every biyar.co.il page. **P: whose phone it is**, to confirm (it becomes the card's `phone`, which drives every WA button) |
| Eyebrow | תיווך נדל״ן · תל אביב | Real estate · Tel Aviv | our wording on S facts |
| Lede | שיווק, מכירה וניהול של נדל״ן יוקרה בצפון הישן ובצפון החדש של תל אביב. | Marketing, sales and management of high-end homes in Tel Aviv’s Old North and New North. | S: about/home (paraphrased). P: Gili's OK on the wording |
| Areas (text tiles, no photos) | כיכר המדינה · הצפון הישן · הצפון החדש · נווה שאנן | Kikar Hamedina · Old North · New North · Neve Sha’anan | S: about (Old North/New North), projects list (Kikar, APEX Neve Sha'anan). Tile photos = **P** (his material, written approval) |
| Kikar block | see 3.3 | see 3.3 | S: address; link to our hub |
| Listings | the engine's empty-state line: "כרגע אין נכסים פעילים באתר. לפרטים על נכסים נוספים אפשר לפנות ישירות." + an empty `<ul class="nlb-grid">` (hidden when empty) | "No homes are listed right now. For other homes, get in touch directly." | S: biyar.co.il shows no listings (sale/rent/commercial pages empty). **No invented listings.** The empty grid lets the drop box inject his first listing (`inc/broker-drop.php:3093`) |
| About (people) | ה׳ באייר נדל״ן בבעלות גיל נסים ועובד זנגי. גיל נולד בתל אביב וגדל בצפון העיר. עובד עוסק בנדל״ן כ-30 שנה, ומשווק לקהילות יהודיות בחו״ל, בהן צרפת, גרמניה וארצות הברית. | (same, English) | S: about page. First-person bio lines = **P** (his words, approval) |
| Services line (optional) | אדריכלות ועיצוב פנים מישראל ומאיטליה, ליווי משפטי ומימון בשיתוף משרדים ובנקים | (same) | S: about page. Optional, with approval |
| Licence line | `<!--nlbx:licence-->` → "מתווך במקרקעין · רישיון N" read live from the card (draft `:440-452`) | same | **P until Ben**: admins see "רישיון: ממתין לאישור של בן"; the public never sees the page without it (gate) |
| Hero picture | none: the `.nlb-hero-media:empty` gradient (`inc/broker-drop.php:3080`) | same | **P**: only his own material with written approval. **No photo of him, no portrait.** The tower renders on his site are probably the developer's (call-prep), so they are not used |
| JSON-LD | RealEstateAgent: name, telephone, address (ה׳ באייר 4), areaServed, parentOrganization | same | from the fields above |
| Yoast title | ה׳ באייר נדל״ן \| תיווך נדל״ן יוקרה בצפון תל אביב | Heh B’iyar Real Estate \| High-end Homes in North Tel Aviv | our wording ("יוקרה" is in the broker DNA's title set, `docs/dna/luxury-broker-copy-dna-2026-09.md:67`) |
| Meta description | ה׳ באייר נדל״ן, משרד תיווך ברחוב ה׳ באייר 4 בתל אביב: נדל״ן בצפון הישן, בצפון החדש ובכיכר המדינה. פנייה ישירה בוואטסאפ ובטלפון. | (same, English) | our wording on S facts |

**Left out on purpose** (claims we cannot check, or the rules):
- "מעל 1,700 נכסים", "30 שנות ותק" as a stat, "3,570 לקוחות מרוצים";
- "שיווקה אלפי יח' דיור";
- the ₪80M penthouse and the celebrity client;
- the 11-project list (projects he marketed are not listings; add only with his written list and approval);
- his logo and every image (approval first);
- the "_EN" duplicated English Kikar pages.

### 3.3 The Kikar block on his site (broker intent, no hub text)

- **H2:** "ה׳ באייר נדל״ן בכיכר המדינה" / "Heh B’iyar Real Estate at Kikar Hamedina". It never uses the hub's head term
  "מגדלי כיכר המדינה" as its heading.
- **Body (2 sentences):**
  - he: "המשרד ברחוב ה׳ באייר 4, על טבעת הכיכר. לדירות במגדלים, פנייה ישירה למשרד."
  - en: "The office is at 4 Heh B’iyar St, on the square’s ring road. For homes in the towers, contact the office directly."
  - The ring-road fact is also in our facts (`inc/project-stage.php:350`).
- **One link to the hub:** "כל המידע על הפרויקט: הסיור, הקומות והעסקאות שפורסמו ←" → `/projects/hamedina/`; in English
  "Everything about the project: the tour, the floors and the published deals →" → `/projects/hamedina-en/`.
- **Not on his site:** facts tables, deal prices, unit counts, the 3D picker, the film, the 360 tour. They are the hub's.
  The private preview's "המגדלים" block and its picker do **not** ship (gap 4).
- When he uploads a real listing in the towers, it becomes a listing page through the drop box. Its title carries the
  apartment (rooms, tower, floor), never the project's head term alone.

### 3.4 Order (Meital's contract, `.claude/skills/broker-minisite/SKILL.md:12`)

nav (הנכסים · כיכר המדינה · האזורים · עלינו · יצירת קשר · English) → hero (eyebrow, H1 office, lede, WA + office phone) →
the Kikar block → areas tiles → listings (empty state) → about (people) → contact (address, phones, licence line,
legal lines) → the mobile bar (WA + call).

**Gates before any public level:**
- Gili's written approval of the wording;
- the licence holder and number;
- the page research law (owner, 3.10): record the 4-5 competitors' broker pages for the Kikar intent (Open House,
  Sotheby's Israel, IP-TLV ranked 5-7 for "מגדלי כיכר המדינה", `biyar-review.md:81`) before the final copy;
- the language-dna blacklist grep.

---

## 4. DESIGN: the broker slot on the Kikar page

### 4.1 Where it sits (content-first is kept by construction)

| Width | Rendered order (world page grid, `inc/project-stage.php:1286, 1294`) |
|---|---|
| Phone (<1100px) | H1 → answer paragraph (`.nl-lead`) → CTAs (WA · "דירות למכירה במגדלים" · tour) → stage → map → facts → deals (he) → **rail: Gili's square + the empty slot** → article … `#nlws-sale` → **the line** |
| Desktop | text column (H1, answer, CTAs) beside the stage → map → facts → deals → **rail row** → article … `#nlws-sale` → **the line** |

Both placements come **after** H1 → answer → CTAs → stage, so `tools/content_first_check.py` C3/C4 cannot move. Neither one
adds an H1. The square's name is an `h3`, as today. The line uses `<p>`, so the article's outline stays the article's.

### 4.2 The rail square (all 5 pages)

- `nadlan_ps_current()` takes the rail from `nadlan_bx_project_brokers( 'hamedina', $lang )`.
- `nadlan_ps_square()` delegates to `nadlan_bx_square_html()`.
- On `/projects/hamedina/` Gili's square stands before the "רוצה להופיע כאן?" slot. On `-en/-fr/-ru/-ar` the square stands
  alone: the slot stays Hebrew-only, as today.
- **A click on his name or on "לאתר של גיל"** opens `/brokers/heh-biyar/`. From `-en`, `-fr`, `-ru` and `-ar` it opens
  `/en/brokers/heh-biyar/` (the owner's "a click opens his mini-site").
- WhatsApp goes straight to the broker, with the page's name in the message.
- Views and clicks go to insights (`place_view`/`place_click`, slot `bx-hamedina-<lang>`). GA events go out on world pages,
  which have no bridge.js (draft `:454-472`).

### 4.3 The line in "למכירה ולהשכרה" (`#nlws-sale`)

- **Placement:** after the paragraph that links to the brokers directory, before "דירות להשכרה" (draft
  `nadlan_bx_strip_insert()` `:399-421`). It fails open: no section, no line. It is never inserted twice.
- **Content:**
  - the tag "פרסומת";
  - the heading "מתווכים שפעילים במגדלי כיכר המדינה";
  - one row per broker: the name (link), the office, the licence line, "לאתר של גיל".
- **Why there:** the hero's "דירות למכירה במגדלים" lands on this section. Its own text already sends the reader to brokers.
  This is the page's real broker intent, answered with a real broker.
- Switch: option `nadlan_bx_strip` (`'0'` = rail only).

### 4.4 No cannibalization of the hub

- The square and the line carry **no project text**: no facts, prices, counts or tower words. They show the name, the
  office, the licence and two buttons.
- His site holds 2 sentences about Kikar plus one link to the hub (3.3). Its title and H1 are the office, not the project.
- No broker URL carries `hamedina`/`kikar` (3.1). The hub stays the only page for "מגדלי כיכר המדינה".
- No Offer, RealEstateListing or Product schema for the broker on the hub page.

---

## 5. BUILD PLAN for main

### 5.0 Gates (in this order)

1. **Design first** (owner law 27.9): add to the design system artifact:
   - BrokerSquare v-next: localized, office name, site button, preview badge;
   - the BrokerSaleLine (`#nlws-sale`);
   - the exposure screen.
   Then the screenshot review (`aesthetic-ownership`).
2. **Release lock**, one runner at a time (`docs/coordination/claude-codex.md` lock lines). Read the lock and the health in
   a separate command, and never run another session's runner.
3. **Maya's QA gate:** local, then the route-swap preview, then her QA, **then a new word from Ben**. Green QA is not a
   deploy order.
4. **Gili's content:** his written approval, the licence answer and the research law (3.4). These are needed before any
   public level, **not** before the hidden build.

### 5.1 Files and hunks (apply to the LIVE text, MD5-pinned)

| # | File | Change |
|---|---|---|
| A | `inc/broker-exposure.php` (NEW) | the draft module, after main's review |
| B | `nadlan-config.php:33` | add `'broker-exposure'` to the module list (right after `'brokers-list'`); bump the version on the live text |
| C | `inc/project-stage.php` `nadlan_ps_current()` after `:577-580` | `if ( function_exists( 'nadlan_bx_on' ) && nadlan_bx_on() ) { $memo['rail'] = nadlan_bx_project_brokers( $slug, $lang ); }` (keeps the `unset` of film/deals for language pages as it is on live) |
| D | `inc/project-stage.php` `nadlan_ps_square()` first line inside `:605` | `if ( function_exists( 'nadlan_bx_on' ) && nadlan_bx_on() && function_exists( 'nadlan_bx_square_html' ) ) { return nadlan_bx_square_html( (int) $pid, $ps ); }` |
| E | `inc/project-stage.php` `nadlan_ps_compose()` just before the final `return $html;` (`:1003`) | `if ( function_exists( 'nadlan_bx_strip_insert' ) ) { $html = nadlan_bx_strip_insert( $html, $ps ); }` |
| F | `inc/brokers-list.php` `nadlan_bl_brokers()` `:28-37` | the query takes `array( 'publish', 'private' )` when `nadlan_bx_preview()`; in the loop: `if ( function_exists( 'nadlan_bx_on' ) && nadlan_bx_on() ) { if ( ! nadlan_bx_can( $id, 'directory' ) ) { continue; } if ( nadlan_bx_can( $id, 'featured' ) ) { $feat[] = (int) $id; continue; } } else { /* today's tier/pinned rule */ }`; then sort `$feat` by the entry's `order` |
| G | `inc/brokers-list.php` `nadlan_bl_feature_card()` `:95-96` | `$href = function_exists( 'nadlan_bx_site_url' ) && nadlan_bx_on() ? ( nadlan_bx_site_url( $id, 'he' ) ?: get_permalink( $id ) ) : <today>` |
| H | `inc/home-v3.php:176` | the column "המאגר" = `array_merge( [ כל המאגר, מתווכים ], nadlan_bx_menu_links( 'he' ) ?: [], [ הצטרפות למאגר ] )` |
| — | snippets 687/699/707 | **no change.** The join default is handled in the module (`nadlan_bx_join_level`) |

Hunks C-H all go through `function_exists()` + `nadlan_bx_on()`. With the module missing or the option at `'0'`, every page
is byte for byte today's.

### 5.2 The runner (`scripts/broker-exposure/deploy<N>.py`, from the current template chain)

**Files:** A (new), B, C-E (`project-stage.php`), F-G (`brokers-list.php`), H (`home-v3.php`).
- Lint each one on the server through the bridge.
- Keep `.bak<N>` siblings.
- Pin MD5 against the live text.

**Ops through the bridge**, recorded in `deploy-result-<N>.json`:
1. Back up the option `nadlan_broker_exposure` (absent today) and the statuses of 7833, 7644 and 7804.
2. `nadlan_bx_seed()` with Meital's entry (2.11).
3. **Gili's build** (can be a second, separate runner after Ben's word on the content):
   - **Card:** create the card **private**, with:
     - `profession=metavech`, `company_name=ה׳ באייר נדל״ן`, `nl_brand_en=Heh B’iyar Real Estate`;
     - `nl_name_he=גיל נסים`, `nl_name_en=Gil Nissim` (or the licence holder's name, per Ben);
     - `phone=054-2442555` (per the open question), `city=תל אביב יפו`;
     - `areas_served=כיכר המדינה,הצפון הישן,הצפון החדש,נווה שאנן`, `nl_areas_en=Kikar Hamedina,Old North,New North,Neve Sha'anan`;
     - `source=broker_minisite`, `source_url=https://biyar.co.il/`, `nl_gender=m`, `nl_langs=he,en`, `nl_slug=heh-biyar`;
     - `license_number` empty;
     - **no** `verified_at`, **no** `nl_drop_on`, **no** thumbnail.
   - **Pages:** create `/brokers/heh-biyar/` (parent 7645) and `/en/brokers/heh-biyar/` (parent 7803), both **private**,
     with:
     - the handcrafted `nlb-*` HTML from 3.2-3.4, using the engine's CSS (`nl_drop_site_css()`) for one look with Meital's
       and the engine sites;
     - `nl_broker_site=<card>`, `nl_lang=he|en`, `nl_hreflang={he,en}`, and the Yoast title and description.
   - **Back on the card:** `nl_site_he/en` = the page ids.
   - **Entry:** `nadlan_bx_save`-equivalent through the bridge: `hidden`, `hamedina: [he,en,fr,ru,ar]`, `menu=1`,
     `order=20`, `licence_ok=0`, note "not in the active register 3.10.2026 (HAD-394)".
4. Purge (`purge` op), then wait for the version, then run the checks (5.3).

**Never:**
- send anything to Gili;
- set `nl_drop_on` (no upload link until Ben decides);
- add noindex;
- touch Maya Rotenberg's cards.

### 5.3 Runner checks (anonymous, cache-busted raw HTML)

| URL | need | never |
|---|---|---|
| `/projects/hamedina/` | `class="nlbslot"`, `id="nlws-sale"`, `nl-project-page-title` ×1 | Gili's card id as `data-nlbx="<id>"` / `data-nlps-pro="<id>"`, `heh-biyar`, `ה׳ באייר נדל״ן`, `nlbx-strip`, `nlbx-preview` |
| `/projects/hamedina-en/`, `-fr`, `-ru`, `-ar` | `id="nlws-sale"`, h1 ×1 | `heh-biyar`, `Gil Nissim`, `nlbx-strip`, `nlbx-preview`, any Hebrew outside the article (`tools/lang_pages_check.py hamedina`) |
| `/projects/rainbow-tel-aviv/` | `data-nlps-pro="7833"`, `רישיון תיווך`, `3131540`, `התייעצות בוואטסאפ`, `נדל״ן על הים` (new, declared), `לאתר של מיטל` (new, declared), `class="nlbslot"` | `nlbx-preview` |
| `/projects/rainbow-tel-aviv-en/` | (rail as today: no square) | `data-nlps-pro="7833"` |
| `/projects/duo-tel-aviv/`, `dimri-yama-sde-dov/`, `ashira-sde-dov/` | `class="nlbslot"` | `data-nlps-pro=` |
| `/brokers/` | `nlds-bfeat`, `מיטל קציר`, `3131540`, the same total in the lead as before the release (record it first) | `heh-biyar`, `גיל נסים`, `nlbx-preview` |
| `/brokers/heh-biyar/`, `/en/brokers/heh-biyar/`, `/professionals/heh-biyar/` | HTTP **404** | — |
| every page above | `id="nlhp-top"` or the old header as today | `ה׳ באייר`, `heh-biyar` in the header menu |
| all broker surfaces (after Gili goes public) | the licence number, `פרסומת`/`Advertisement` | `עמלה`, `דמי תיווך`, `commission`, `המתווך שלנו`, `our broker`, `ייעוץ חינם` (outside the bar) |
| `/wp-json/nadlan/v1/health` | `broker_exposure.on=true`, `entries=2`, `by_level={featured:1, hidden:1}` | — |

Also run:
- `python tools/content_first_check.py` (all 10 pages green);
- `python tools/lang_pages_check.py hamedina`;
- `python tools/wa_wording_check.py`;
- `python nad-lan-co-il/tools/source_audit.py` snapshots + diff on Kikar ×5, Rainbow ×2 and `/brokers/` (the only expected
  diffs: Rainbow he square + the version);
- the skill's `meital_site.py --journey` (Meital's journey must stay PASS).

### 5.4 Real presses (Ben's Chrome "gmktec", phone 390 and PC 1440, a screenshot after every press, the URL checked in tabs_context after each click; the eyes evidence class)

**Logged in:**
1. wp-admin › NadLan Ops › "חשיפת מתווכים". Meital and Gili are listed. Gili's public radios are locked, and the reason is
   shown.
2. Gili's row › "כיכר המדינה (תצוגה)". The Kikar page shows his square with the red "תצוגה למנהל בלבד", and the line in
   "למכירה ולהשכרה".
3. Press his name. His private site opens (he).
4. "English". The English private site opens.
5. Back. Press "לאתר של גיל". Same result.
6. Repeat on `?nlbx_preview=<id>` for `/projects/hamedina-en/`, `-ru` and `-ar`. Check the language words, that no Hebrew
   is left, and that the click goes to the English site.
7. Rainbow (he): Meital's square. Press "לאתר של מיטל". Her site opens.

**Logged out** (an incognito window): Kikar ×5 shows no Gili. `/brokers/heh-biyar/` returns 404. `/brokers/` shows no Gili.

**The toggle shown working:**
- (a) **No public effect:** on Gili's row, untick Kikar `ru`, then save. `?nlbx_preview` on `-ru` shows no square; on `-en`
  it still shows. Tick it back.
- (b) **Public, only with Ben's word:** either
  - Gili, once the licence is confirmed: raise to "גם בעמודי הפרויקטים"; incognito Kikar ×5 shows him; lower to
    "מוסתר"; incognito shows him gone (purge proven); or
  - Meital: add `en` to Rainbow; incognito `/projects/rainbow-tel-aviv-en/` shows her square in English; remove it.
- Record each step in the audit log (שונה ... ← ...).

### 5.5 Rollback

1. **Instant:** option `nadlan_bx_on = '0'`. Every hunk falls back to today's code path, and the screen disappears. Gili's
   records stay private: they are created private, and nothing public depends on the module.
2. **Files:** `.bak<N>` siblings via the runner's `--rollback`; then `opcache_reset` and `litespeed_purge_all`.
3. **Data:**
   - restore the backed-up option (absent before the release, so delete it);
   - put back the statuses stored in each log row's `flips`;
   - Gili's card and pages go to **draft**. No hard delete: permanent deletion is Ben's.

### 5.6 Tracking

- HAD-436: link this spec, the drafts, the PR/commit, the runner result and the screenshots.
- Child issues for the gaps in 1.8.
- The Notion row in "מרכז הבקרה של הפרויקטים".
- HAD-394 stays "In Review" until Ben's licence answer.

---

## 6. Open questions for Ben (only he can answer)

1. **The licence:** whose licence is it (Gil Nissim, or Oved Zangi = "זנגי עובדיה חי"?), and what is the number? Until he
   answers, Gili stays hidden.
2. **Whose name is on the site:** the office "ה׳ באייר נדל״ן" with both partners (slug `heh-biyar`), or the licence
   holder's name?
3. **Self-serve joiners after the release:** keep them listed at once, as today (as the join screen promises), or start
   them hidden or link-only like everyone else?
4. **"A place in the brokers menu":** does it mean a card on `/brokers/` (the menu item "מתווכים" opens it), or also his
   name in the header menu under "אנשי מקצוע"? The build supports both; Gili's menu box is pre-ticked and only acts at
   "מומלץ".
5. **"Link only":** is it enough that nad-lan never links to the site, or should Google also not index it? Adding noindex
   is only ever your order.
6. **Raising a broker to public** fires the site's generic sitemap ping. Keep it, or never ping for brokers?
7. **The other switches:** should the placements (ad cards on guides) and the home-page paid slot also obey this one
   screen? Today they are separate.
8. **Business with Gili:** no payment for now (collaboration and leads). Confirm that his WhatsApp leads go straight to him
   and that we keep only the view and click counts.
9. **The upload link:** does Gili get a drop box link when he goes public, or do we upload his apartments for him?
10. **The WhatsApp 054-2442555** (the floating button on his site): his own mobile, or the office's? It goes on every
    button.
