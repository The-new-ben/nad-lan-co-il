# Professionals on nad-lan.co.il: what exists today (code survey, 12.11.2026)

Scope: read-only survey of the repo `C:\Users\777\nad-lan\nad-lan-co-il` (plugin `plugins/nadlan-config`) before designing a forum and social network attached to every professional's card. Nothing was run, deployed or changed except this file.

**Evidence class: code only.** Every claim below comes from reading repo files (file:line). Nothing was checked on the live site. **The repo is not the live site:** the repo's `nadlan-config.php` header says `Version: 1.72.372` (line 5) while releases are at 1.72.666 (`scripts/project-stage/deploy666.py`); the repo module list (line 33) does not even contain `expert-advisor`, which is live. Releases hunk the LIVE PHP text read through the bridge (see section 6), so any repo file below may differ from production. Before building, read the live copies of the files you will touch.

Paths below are relative to `plugins/nadlan-config/` unless stated.

---

## 1. Data model

### Post type
- `nadlan_professional`, registered in `nadlan-config.php:272-280`: public, `show_in_rest`, archive and rewrite slug `professionals` (so `/professionals/` archive and `/professionals/<slug>/` singles), supports `title, editor, thumbnail, custom-fields, excerpt`. **No `comments` support.** Capability type `listing/listings` with `map_meta_cap` (lines 248-252).
- Taxonomy `nadlan_profession` (non-hierarchical, slug `/profession/`) at `nadlan-config.php:285-288`. In practice the profession is stored as **post meta `profession`** (every query uses `meta_query key=profession`); the taxonomy is used only for archive titles (`inc/page-h1.php:122-128`) and the interior-designers page (`inc/design-pages.php:32-33`).
- Taxonomy `nadlan_city` is attached to properties and projects only (`nadlan-config.php:281-284`), **not** to professionals. A professional's city is meta `city` (free text, LIKE-matched in `inc/directory.php:218-220`).
- Private related CPTs: `nadlan_claim` (`inc/claim.php:24`), `nadlan_review` (`inc/reviews.php:19`), `nadlan_referral` (`inc/lead-ledger.php:41`), `nadlan_drop` (broker submissions, `inc/broker-drop.php:52`), `nadlan_room` (video rooms, `inc/together.php:85`).
- Custom table `{prefix}nadlan_endorse` (professional-to-professional recommendations), `inc/pro-network.php:109-133`.

### Meta keys on `nadlan_professional`
Registered in `inc/catalog-meta.php:111-145`:
`profession, registry_number, classification, license_number, company_name, address, city, areas_served (CSV), phone, email, website, years_active, project_count, rating, reviews_count, photos_csv, logo_url, source, source_url, claim_status (unclaimed|pending|verified), owner_user_id, verified_at, source_id, is_demo`.

Added elsewhere:
- `inc/professional-profile.php:49-53`: `specialties_csv, languages_csv, bio, response_time, meeting_url, calendar_url, nl_video, lat, lng, profile_views` (REST-writable only by `edit_post`).
- `inc/tiers.php:33-42`: `paid_tier` (free|pro|premier), `trial_started` (both server-only).
- `inc/broker-drop.php:44-46` (snippet x-broker-drop): `nl_drop_on, nl_name_he, nl_name_en, nl_name_ru, nl_brand_en, nl_gender (f|m), nl_site_he/en/ru/fr, nl_auto_publish, nl_langs, nl_tier, nl_slug, nl_hero, nl_areas_en/ru/fr, nl_bio_en`. Private: `_nl_drop_token` (24 chars), `_nl_email`, `_nl_signup` (`inc/broker-join.php:509-518`).
- `inc/profile-extras.php:37-56`: `social_facebook, social_instagram, social_tiktok, social_youtube, website, video_url`.
- `inc/pro-cards.php`: `procard_impressions, procard_sponsor_until, procard_sponsor_domains`; `inc/pro-network.php:318-327`: `trade` (register contractors' trade key).
- `reviews_verified` (stars are shown only when set: `inc/directory.php:285`, `inc/professional-profile.php:196`).
- `is_pinned` (brokers list, `inc/brokers-list.php:34`), `view_count` (stats mail, `inc/pro-stats-email.php:22`).
- Firgun joins: `_nl_invite_token, _nl_join` (`inc/firgun.php:438-439`).
- **Gender**: `nl_gender` f|m drives gendered labels (`inc/directory.php:92-118`). **WhatsApp**: there is no separate WhatsApp field; `phone` is converted to wa.me digits (`inc/professional-profile.php:143-150`). **Verified badge**: computed, not stored: `nadlan_dir_registry_verified()` = `verified_at > 0` OR `source` in (`pinkas_hakablanim`, `metavhim`) (`inc/directory.php:121-134`); "owner-managed" label = `claim_status=verified` (`inc/pro-card.php:92`).

### Professions (keys and Hebrew labels)
Three overlapping lists:
1. Directory base, 8 keys (`inc/directory.php:47-58`): kablan קבלן, shamai שמאי מקרקעין, bedek_bait בדק בית, mashkanta יועץ משכנתאות, architect אדריכל, lawyer עו״ד מקרקעין, mefakeach מפקח בנייה, metavech מתווך.
2. Profile extras, 6 keys (`inc/professional-profile.php:27-35`): interior_designer מעצב/ת פנים, engineer מהנדס/ת בניין, accountant רו״ח מיסוי נדל״ן, surveyor מודד/ת מוסמך, property_manager ניהול נכסים, urban_planner מתכנן/ת ערים.
3. **The full network registry, 34 professions in 5 groups** with singular, plural and female forms (`inc/pro-network.php:23-73`), the most complete list and the one a forum should use:
   - קנייה, מכירה ומימון (7): metavech מתווך, shamai שמאי מקרקעין, lawyer עורך דין מקרקעין, mashkanta יועץ משכנתאות, accountant רואה חשבון מיסוי מקרקעין, actuary אקטואר, insurance סוכן ביטוח דירה.
   - תכנון ובנייה (9): architect, engineer, mefakeach, surveyor, urban_planner, kablan, renovation קבלן שיפוצים, bedek_bait, developer יזם.
   - מערכות הבית (7): electrician, plumber, hvac, waterproofing, solar, pools, security.
   - עיצוב וריהוט (7): interior_designer, kitchens, flooring, windows, furniture, lighting, gardens.
   - מעבר דירה ושירותים (4): movers, cleaning, property_manager, organizer ארגון דיירים.
   The directory filter pills show only list 1 (`inc/directory.php:523-530`), so most of the 34 keys have no pill on `/professionals/`.
- Data sources (meta `source`): `pinkas_hakablanim` (contractors register, data.gov.il), `metavhim` (MoJ brokers register), `broker_join`, `broker_minisite`, `firgun_join`, `editorial`, `demo_seed` (`inc/cards-render.php:149-155`, `inc/claim-prompt.php:34`, `inc/brokers-list.php:32`). The directory header claims ~2,700 contractors (`inc/preferred-partners.php:15`, `inc/professional-profile.php:7`); live counts not checked.

### How a broker differs
- Same post type, `profession=metavech`. Brokers who joined alone get `source=broker_join`, `claim_status=verified`, `verified_at` at creation, a private drop token, a Hebrew site page at `/brokers/<latin-name>/` and listings at `/properties/<slug>/` (`inc/broker-join.php:461-531`).
- On a broker card the contact buttons go **straight to the broker** (HAD-249, `inc/professional-profile.php:138-142, 272-276`; `inc/directory.php:654-655`), the portal's date-booking band is switched off (`inc/professional-profile.php:162-168`), and a broker's own listings are "owned" pages where portal blocks are stripped (`inc/property-owner.php:42-91`, owner = `nl_broker_id` / `nl_broker_site` / `nl_broker_auto` on the listing, or a verified card whose `owner_user_id` matches).
- Register brokers without gender are labelled "תיווך נדל״ן" (`inc/directory.php:97-98`).

---

## 2. The card today, and why people come to the owner

### Where cards render
| Surface | Code | URL |
|---|---|---|
| Directory archive (takes over the archive template) | `inc/directory.php:477-585` (`template_redirect` prio 5) + REST `GET nadlan/v1/directory` (`:427-453`) | `/professionals/?q=&city=&profession=&verified=&sort=` |
| The ONE directory card renderer (ProNetwork v98) | `nadlan_dir_card()` `inc/directory.php:245-310`, facts/trust/privacy from `inc/pro-card.php`, CSS `assets/pronet/procard.css` (9.3 KB) | used by directory, similar pros, brokers list, firgun |
| Single profile page | `inc/professional-profile.php:187-355` (the_content prio 6) + similar pros `inc/directory.php:689-728` (prio 5) + facts table/claim `inc/cards-render.php` (prio 20) + extras `inc/profile-extras.php` (prio 23) + claim prompt `inc/claim-prompt.php` (prio 24) | `/professionals/<slug>/` |
| Inline "experts of the field" cards on content | `inc/pro-cards.php:156-283` (the_content prio 14 on `nadlan_term` and `post`) | glossary terms, guides, articles |
| Brokers list | `inc/brokers-list.php:187` (page id 7645 only) | `/brokers/` (broker sites at `/brokers/<slug>/`) |
| Recommendations page | `[nadlan_firgun]` shortcode `inc/firgun.php:255-257` | `/firgun/` |
| Basket team (project pages with a stage) | REST `GET nadlan/v1/basket/pros` `inc/basket.php:42-96`; team slots `nadlan_bk_team()` `:27-39` = interior_designer, lawyer, shamai, mashkanta, accountant, engineer(+mefakeach) | project pages |
| Interior designers static list | `inc/design-pages.php:83-100` | designers profession page |

### What the directory card shows and does (`inc/directory.php:288-306`)
Cover band with profession mark and a state chip (פרופיל לדוגמה / פרופיל פעיל / מהפנקס הרשמי), portrait or monogram, name, business line, gendered role + city, the strongest register fact, trust labels (owner-managed, in contractors register, licence in brokers register, government-recognised, unlimited scope), verified-only stars, optional foot (recommendations count). **Two actions only:** "לפרופיל" (link) and a save bookmark that writes to the visitor's localStorage `nl_saved_pros` (no server, `inc/pro-card.php:110-118`). "מקודם" chip for pro/premier. **No contact button on the directory card.**

### Profile hero buttons (`inc/professional-profile.php:271-286`)
- **Broker with a usable mobile** (`profession=metavech`): "תיאום סיור" (the broker's own calendar link or wa.me to the broker), "וואטסאפ" `https://wa.me/<broker>?text=שלום ..., הגעתי מהכרטיס שלך ב-nad-lan`, "חיוג" `tel:` broker. **Direct to the professional.**
- **Every other professional:**
  - `$wa = get_option('nadlan_whatsapp_e164')` (line 204), the SITE OWNER's number (default `972525101555`, `inc/keys-hub.php:40`). The green primary button "פנייה בוואטסאפ" (line 278) opens `https://wa.me/<OWNER>?text=היי, אשמח לחיבור אל <name> דרך האתר`.
  - "התקשרו" `tel:` the professional, **only if** `nadlan_tier_can_show($id,'phone')` (line 200), which is true only for a claimed card in its 30-day trial or on pro/premier (`inc/tiers.php:66-107`). An unclaimed card is `public_stub` → no phone. A private person from a register who has not claimed is also stripped (`inc/pro-card.php:32-45`, applied at line 203).
  - Otherwise "קבלו הצעת מחיר" (line 280) → `window.prompt` name + phone → `POST nadlan/v1/referral/route` with `notify_partner:0` (`inc/directory.php:591-606`) → a private `nadlan_referral` with status `new`, **email to the site admin only**, the professional is not contacted ("Owner routes manually", `inc/lead-ledger.php:119-123, 151-170`).
  - Premium (pro/premier or demo) adds "תיאום שיחת וידאו" → form → `POST nadlan/v1/lead` (`inc/professional-profile.php:312-324, 475-482`), i.e. a lead to the owner.
- Schema: `LocalBusiness` / `GeneralContractor` with `telephone`/`email` unless private (`inc/schema.php:60-87`); note it does not apply the tier gate, so the JSON-LD can carry a phone that the hero hides (code observation, not checked live).

**Answer to "why do people come to me for professionals' details":** by design. For every non-broker card the visible contact path is the owner: the primary WhatsApp button dials the owner's WhatsApp asking "to be connected to X" (`inc/professional-profile.php:204, 278`), the quote button creates an owner-only referral (`inc/directory.php:603`, `inc/lead-ledger.php:119-123`), and the phone is hidden on every unclaimed card and every claimed card past its 30-day trial unless paid (`inc/tiers.php:79-107`). The design intent was the lead-ledger commission model ("FAT MONEY door", `inc/preferred-partners.php:5-16`) plus the paywall ("Closes the free listings give away links + contacts leak", `inc/tiers.php:5-17`). Brokers were exempted on 24.9.2026 (HAD-249).

Inconsistency: the inline content cards `nadlan_procard_html()` (`inc/pro-cards.php:167-200`) print WhatsApp `wa.me/<professional>` and `tel:` whenever meta `phone` exists, **without** the tier gate and without the private-person check. So the same professional can be reachable directly from an article but only through the owner on their own profile.

---

## 3. One professional's profile page

- URL `/professionals/<slug>/`; broker joiners also get `/brokers/<latin-name>/` site pages.
- Section order (the_content): similar pros shielded (5), rich profile (6): demo banner, hero (portrait/monogram, profession pill, single H1 "name · office", city, licence or register badge, recommendations count, verified stars, CTAs), stats (since/years, projects, classification, response time), bio, chip groups (התמחויות linking to `/professionals/?q=`, שפות, אזורי פעילות), listings video (`nl_video`), recommendations strip (firgun, only when `nadlan_pro_network_on=1`), video-meeting form, Leaflet area map (lat/lng), "ask the AI" box (premium + AI on), "פרויקטים באתר" (developer/contractor name match), related tools/guides; then facts table + gallery + claim form (20), socials + video (23), claim prompt (24). `profile_views` counted per IP every 6 h, never shown (lines 229-235, 306). Demo cards get `noindex` (lines 381-386).
- Schema: section 2 above.
- Who can edit:
  - **wp-admin** editors; **a claimed owner**: `nadlan_claim_approve()` assigns or creates a WP `subscriber` by the claim email and sends WP's set-password mail (`inc/claim.php:131-169`); `map_meta_cap` then lets that user `edit_post` only their own verified card and `upload_files` (`inc/claim.php:196-225`). Editing then happens in wp-admin/REST (no front-end editor for non-brokers was found).
  - **Brokers: login-less personal link** `/drop/<24-char token>/` (x-broker-drop, `inc/broker-drop.php:1-29, 182-198`; token in private meta `_nl_drop_token`, compared with `hash_equals`). x-broker-edit adds "הפרופיל שלי" there: name, office, phone, about, areas, photo, plus full listing editing, through `nadlan/v1/drop/<token>/edit/{listings,listing/<id>,prepare/<id>,profile}` (`inc/broker-edit.php:26-28, 64-77`). These three modules are **Code Snippets** (x-broker-drop, x-broker-edit, x-broker-join), not in the plugin module list (`inc/broker-drop.php:27`, `inc/broker-edit.php:29`, `inc/broker-join.php:21`); the repo files are copies.
  - Login: `/login/` + `/signup/` with password and flag-gated Google OAuth; "NO magic links and NO email verification loops" because outbound mail was unreliable on 12.7.2026 (`inc/auth.php:14-17`). Persona `pro` lands on `/join-pro/` (line 41).
- Identity verification:
  - Brokers who join: licence checked live against the MoJ brokers register on data.gov.il (resource `a0f56034-88db-4132-8803-854bcdb01ca1`, `inc/broker-join.php:28, 143-174`), Hebrew name must match the registered name (`:183-200, 441`), a signed declaration, trap field, rate limits, daily cap 40, one record per licence (`:396-455`).
  - Everyone else: none automated. "The identity-verification METHOD ... is intentionally left to admin judgement ... phone OTP, registry cross-check is a TODO" (`inc/claim.php:10-13`).

---

## 4. Removal: is there any way to remove or hide a profile?

**No self-service removal or hide exists for a professional's card.** What exists:
- No REST route, button, form or token flow that unpublishes, hides or deletes a `nadlan_professional` (grep of `inc/` for הסרה/הסרת/להסיר/unpublish/remove/opt-out found only listing photos, mailing-list unsubscribes and lead drip opt-outs).
- The only "update or removal" path for professionals is a **mailto** on the static interior-designers list: `'עדכון או הסרה מרשימת מעצבי הפנים: ' . $name` → `<a href="mailto:...">לעסק הזה? עדכון או הסרה</a>` (`inc/design-pages.php:90, 99`). Those records are not `nadlan_professional` cards.
- The firgun join form's privacy text promises "אפשר לבקש תיקון או מחיקה בכל עת" with a mailto to `nl_join_contact()` (`inc/firgun.php:183-184`), i.e. by email to the owner, manual.
- For a joined broker, blocking is an admin action: "לחסימת אתר: מבטלים את 'פעילה' בתיבת הנכסים ומעבירים את עמודי האתר לטיוטה" (`inc/broker-join.php:562`). A broker can mark a listing sold/let and change a price from the drop page (`inc/broker-drop.php:15-17`) but not hide the profile.
- Endorsements can be hidden by their receiver (drop token or claimed login) or an admin: `POST nadlan/v1/endorse/<id>` with `do=hide` (`inc/pro-network.php:300-315`).
- Projects (not professionals) have a public promise: "חברה שמבקשת לתקן פרט או להסיר פרויקט מהמערכת, נעשה זאת מיד" (`inc/developers-page.php:126`, `inc/legal-notice.php:46`).

### Claim flows ("this is me")
Three overlapping, inconsistent paths on an unclaimed card:
1. **Facts-table claim form** (`inc/cards-render.php:129-145`, JS `:214-217`): name, phone, email, honeypot → `POST nadlan/v1/claim` → private `nadlan_claim` with a random token, rate limit 5 per 10 min per IP, email to admin; the card does NOT change state until an admin presses "Approve & assign owner" (`inc/claim.php:50-123, 172-193`).
2. **Claim prompt** "זה הכרטיס שלכם?" "בקשת בעלות + 30 ימי Pro חינם" (`inc/claim-prompt.php:54-76`): three `prompt()` dialogs → `POST nadlan/v1/lead` with `source:'claim-prompt'`. Quote: `fetch('<?php echo esc_js( rest_url( 'nadlan/v1/lead' ) ); ?>',{...body:JSON.stringify({name:n,email:e,phone:p,goal:'בקשת בעלות + 30 ימי Pro חינם',...source:'claim-prompt',card_id:id})})` (line 70). This creates a **lead, not a `nadlan_claim`**, so it does not appear in the inbox's "בקשות בעלות" count (`inc/lead-inbox.php:30-32`) and has no approve button. Both 1 and 2 can show on the same page (priorities 20 and 24).
3. **Register brokers** (`source=metavhim`): the prompt links to `/brokers/?licence=<n>#join` (`inc/claim-prompt.php:39-52`, prefill `:86-92`). Possible dead end (code reading, unverified live): `nl_join_rest` first calls `nl_join_by_licence()` which matches ANY card with that `license_number`, including the register-imported one, and returns 409 "this licence already has a site" (`inc/broker-join.php:363-373, 408-410`). The "send the link again" path needs `_nl_email` (`:542-543`), which an imported card does not have, so it silently does nothing. Needs a live test before relying on it.

The firgun join (`POST nadlan/v1/pros/join`, `inc/firgun.php:400-445`) creates a NEW pending card; it does not claim an existing one.

---

## 5. Building blocks reusable for a forum

### Login-less identity
- **Drop token** (24 chars a-z0-9, `nl_drop_new_token()` `inc/broker-drop.php:200-202`, lookup `:182-198` with `hash_equals`): already accepted by the endorsement API as the actor (`nadlan_endorse_actor()`, `inc/pro-network.php:242-260`), so the same link can post forum content. The firgun page takes it as `?t=` (`inc/firgun.php:193-199`). Re-send only to the signup email (`inc/broker-join.php:533-549`). Only brokers with `nl_drop_on=1` have one today.
- **Invite tokens**: endorsement invites (`invite_token`, `inc/pro-network.php:178-181`, join link `/firgun/?inv=`), renewal-room invites (`invite_token` + `nadlan/v1/renewal-join/<token>`, `inc/urban-space.php:675, 749-766`).
- **Claimed owner login** via WP user + `owner_user_id` (`inc/claim.php`).
- **HMAC page token** pattern (not identity, anti-abuse): `nadlan_adv_token()` = HMAC(page|day, wp_salt) (`inc/expert-advisor.php:76-86`).
- Video-room participants: per-room pid + key hashed with `nadlan_tr_hash()` (`inc/together.php:195-199`).
- **Not found:** phone OTP, SMS provider, magic links (explicitly refused, `inc/auth.php:14-17`), Turnstile, reCAPTCHA, hCaptcha.

### Mail
- Every module calls `wp_mail()`; `inc/mailer.php:22-58` routes it through Brevo SMTP when `nadlan_smtp_host/pass` are set and valid, otherwise the host's PHP mail, with aligned envelope and optional DKIM. Admin probe `POST nadlan/v1/mail-test`.
- Owner notifications: claim (`inc/claim.php:112-120`), referral (`inc/lead-ledger.php:156-170`), review (`inc/reviews.php:125-130`), broker join (`inc/broker-join.php:529`), the owner morning mail (`nadlan_om_send`, folded digest, `inc/lead-inbox.php:124-125`), room mails `nadlan_omx_send` (seen in `make_deploy661.py:23`).
- Mail studio with consent lists and legal unsubscribe (`inc/mail-studio.php:234-263, 423`), drip opt-out tokens (`inc/lead-drip.php:56-94`).
- Monthly professional stats mail exists but is OFF until `nadlan_pro_stats_email_enabled=1`; preview `GET nadlan/v1/pro-stats-preview?card=` (admin) (`inc/pro-stats-email.php:10-16, 58-109`).

### Rate limiting (all transient-based, no shared helper)
- `nadlan_tr_rl($bucket,$max,$window)` fixed window per IP (`inc/together.php:184-194`): the cleanest reusable one. Plus a site-wide daily cap (`:60-67`).
- `nl_join_limited()` with HMAC'd IP (`inc/broker-join.php:344-355`), `nl_drop_rate($bid,...)` per actor (`inc/broker-drop.php:211-217`), `nadlan_adv_rate_ok()` 20/10 min + 80/day hashed IP (`inc/expert-advisor.php:113-123`), claim 5/10 min (`inc/claim.php:82-88`), lead 8/hour (`inc/conversion-cta.php:308-314`), review 3/hour + 30-day duplicate (`inc/reviews.php:95-109`), endorse 20/hour per actor + 12 per 30 days (`inc/pro-network.php:166-167, 285-288`), firgun join 5/day per IP + 60/day site (`inc/firgun.php:407-411`). A live `final-hardening.php` public-POST filter is referenced by the release runner (`deploy666.py:2696-2697`); not read.

### Spam protection and content rules
- Honeypot fields named `company` or `website` everywhere (claim, lead, referral, review, firgun join, broker join).
- Positive-only text cleaner `nadlan_endorse_clean_line()`: strips links, phone-like digit runs, long dashes, 140 chars (`inc/pro-network.php:144-154`); fixed positive quality vocabulary (`:136-142`). A forum can reuse this pattern.
- Banned-word gate `nl_drop_banned_hits()` (used `inc/broker-join.php:435`), fair-housing steering patterns (`inc/ai-features.php:67-72`).

### Moderation and admin screens
- `💰 Lead Inbox` admin menu with pending counts and a site-wide admin notice (`inc/lead-inbox.php:51-57, 140-147`).
- Reviews: `pending` → admin publishes → rating recomputed (`inc/reviews.php`).
- Joined cards wait as `pending` with an admin notice (`inc/firgun.php:467-472`) and attach waiting endorsements on publish (`:448-455`).
- Claim CPT with an approve button (`inc/claim.php:172-193`). Preferred partners list (`inc/preferred-partners.php`). Feature switchboard `Settings > NadLan Features` (`inc/feature-flags.php:9-60`).

### Existing "social" pieces
- **Endorsements network** ("המלצות", firgun): table, REST `GET nadlan/v1/pros/search`, `POST nadlan/v1/endorse`, `POST nadlan/v1/endorse/<id>`, `POST nadlan/v1/pros/join`; display behind `nadlan_pro_network_on='1'` (`inc/pro-network.php`, `inc/firgun.php`). Counts as a thumbs-up "RecCount", never a score (`inc/pro-network.php:212-240`).
- Save list in the browser (`inc/pro-card.php:110-118`).
- Renewal rooms have an updates feed with invite-by-token membership (`inc/urban-space.php:6-7, 792-803`), the nearest thing to a group feed.
- **No forum, Q&A, thread, community or WordPress comments feature exists** for professionals (grep for forum/community/thread/discussion/comment_form/wp_insert_comment found nothing relevant; the CPT has no comments support).

### REST conventions
Namespace `nadlan/v1` everywhere; public routes use `permission_callback => '__return_true'` with in-callback checks; errors return 400 not 403 because "uPress turns a 403 into its 404 page" (`inc/pro-network.php:284`). Admin routes use `current_user_can('manage_options')`. Full professional-related route list:

| Route | File:line | Auth |
|---|---|---|
| GET `/directory` | `inc/directory.php:428` | public |
| POST `/claim` | `inc/claim.php:41` | public, honeypot, 5/10 min |
| POST `/lead` | `inc/conversion-cta.php:255` | public, 8/h |
| POST `/referral/route`, GET/POST `/referral/<token>/accept` | `inc/lead-ledger.php:107, 201` | public |
| POST `/review-submit` | `inc/reviews.php:68` | public |
| GET `/pros/search`, POST `/endorse`, POST `/endorse/<id>` | `inc/pro-network.php:264, 280, 301` | public / token / login |
| POST `/pros/join` | `inc/firgun.php:402` | public, switch |
| POST `/brokers/join`, `/brokers/relink` | `inc/broker-join.php:340-341` | public |
| `/drop/<token>/edit/*` (listings, listing/<id>, prepare/<id>, profile) | `inc/broker-edit.php:65-76` | drop token |
| `/drop/<token>...` (engine routes) | `inc/broker-drop.php` (5 routes, not listed here) | drop token |
| GET `/basket/pros` | `inc/basket.php:43` | public |
| GET `/pro-stats-preview` | `inc/pro-stats-email.php:59` | admin |
| `/admin-control/cards`, `/admin-control/card/<id>` | `inc/admin-control.php:595, 600` | admin (not read) |
| POST `/prof-dossier-generate` | `inc/related-content.php:102` | not read |
| POST `/concierge-lead` | `inc/ai-concierge.php:461` | not read |

### Shipping hidden (gates)
- Option switches: `nadlan_pro_network_on` (`inc/firgun.php:21-23`), `nadlan_procard_enabled` (`inc/pro-cards.php:213`), `nadlan_basket`, `nadlan_brokers_list`, `nadlan_owned_rule`, `nadlan_register_contacts` (`inc/pro-card.php:37`), `nadlan_advisor` + page list.
- Query switches: `?advisor=on` on listed page ids only (`inc/expert-advisor.php:47-67`), `?scan=on` kept in the browser (`assets/designer/studio.js:27-31`, option `nadlan_designer_scan` `inc/designer.php:973`), `?kikar=next` / `?kikar=journey` (`inc/project-stage.php:1119, 1177`, `assets/project-stage/world/journey.js:17`), `?nudge=fresh|show` (`inc/price-nudge.php:26, 278`), `?skin=a` (`inc/skin-a.php:15-24`). The advisor pattern (option ON + `?x=on` + page allow-list) is the safest template for a hidden forum.

### Assets and versions
- `wp_enqueue_style/script(..., plugins_url('assets/<module>/<file>', dirname(__FILE__)), array(), NADLAN_CONFIG_VERSION)` (e.g. `inc/basket.php:99-104`); modules with their own constant (`NADLAN_ADV_VERSION`, `inc/expert-advisor.php:41, 638-639`). The ProCard CSS is printed once per page as a `<link>` with `?ver=NADLAN_CONFIG_VERSION` (`inc/pro-card.php:104-121`). Inline CSS/JS via `wp_add_inline_style/script` is common (`inc/professional-profile.php:397-502`). Modules load from the module list in `nadlan-config.php:33` (live list differs; releases prove it with `apply_main`).

### The expert advisor and professionals
It never picks or names a specific professional; its rules forbid matching the visitor with anyone and say to use the "השאירו פרטים" form to reach the NadLan team (`inc/expert-advisor.php:315-326`). It only links the `/professionals/` hub (line 280).

---

## 6. Release chain (`scripts/project-stage/`)

Newest six releases (name, bytes):

| # | make_deploy | deploy |
|---|---|---|
| 661 | make_deploy661.py 8,350 | deploy661.py 398,451 |
| 662 | make_deploy662.py 803 | deploy662.py 397,987 |
| 663 | make_deploy663.py 3,184 | deploy663.py 399,390 |
| 664 | make_deploy664.py 5,885 | deploy664.py 399,324 |
| 665 | make_deploy665.py 2,591 | deploy665.py 399,670 |
| 666 | make_deploy666.py 3,834 | deploy666.py 400,707 |

How a release is built (read from `make_deploy666.py`, `make_deploy661.py`, `kl_release.build_release` lines 346-435, and `deploy666.py`; nothing was run):
1. `make_deployN.py` declares FILES (asset files to swap), NEW (files that must not exist live yet), HUNKS (`{rel: [(old, new), ...]}` exact-anchor replacements on live PHP), LIVE (`{rel: md5}` the live PHP text must have, proven from a dated live read such as `docs/qa/live-read/20261112T022923Z/inc/rfp.php`), and extra check ROWS (url, must-contain, must-not-contain).
2. It asserts the previous release's record `deploy-result-(N-1).json` says `released`.
3. `kl_release.build_release()` copies `deploy(N-1).py` to `deployN.py`, renaming every version, `.bakN`, `?tN` cache-busters and result files; it requires the repo copy of each hunked PHP to equal the proven live md5, applies each hunk only if its anchor appears exactly once, runs `php -l` (and `node --check` on JS), pins the md5 of every swapped file (PIN), writes `kikar_N.py` (the hunks plus a proof that the live module list is unchanged), and sets `PHP_RELS` = the hunked files.
4. `deployN.py` (runs only via a runner): reads `GET /wp-json/nadlan/v1/health` (must be ok and the expected previous version), refuses if its own release is in flight.
5. Creates a one-run **bridge**: a temporary Code Snippet `x-tmp-psN-ops-<time>` with a random REST namespace `nadlan-psN-<token>` (`deploy666.py:129-131, 568-580`), authenticated with the WP application password decrypted by DPAPI inside the runner.
6. Drift guards: every swapped live file must equal what the last release wrote; the live posts and module list must be the expected ones; live copies of all touched files and `nadlan-config.php` are saved to `docs/qa/.../live-backup/` with a timestamp.
7. Reads the LIVE PHP through the bridge, checks its md5 against `PX.LIVE_MD5`, applies the hunks, `php -l` again; bumps `* Version:` and `NADLAN_CONFIG_VERSION` in the live `nadlan-config.php` (must land on the exact new version).
8. Writes each file with `put(rel, data, expect=<live md5 or "missing">)`; the bridge keeps a `.bakN` copy beside every replaced file; records `deploy-result-N.json` immediately.
9. Writes any posts/meta with md5-guarded before/after and an UNDO list.
10. Purges (opcache, LiteSpeed, object cache), waits for health to report the new version, runs CHECKS (served bytes equal at `?ver=`, page markers, home/project order, rainbow and h-infinity spot checks), retries once after a second purge.
11. On any failure, `rollback()`: undo non-file writes in reverse, restore `nadlan-config.php` + `PHP_RELS` + replaced files from `.bakN`, unlink NEW files, restore posts, purge, wait for the old version, record "rolled back".
12. `finally`: bridge snippet deleted (route must answer 404), sweep. `PHP_RELS` must list every hunked file or rollback will not restore it (memory note "Rollback hunk outage 25.10").

Broker modules (x-broker-drop, x-broker-edit, x-broker-join) are released separately as persistent Code Snippets by `scripts/broker-drop/deploydrop.py` and `scripts/broker-edit/deployedit.py` (per their headers), not by this chain.

---

## 7. "Reverse Engineer Anything"

**Not found under that name.** Looked in: `C:\Users\777\Documents\agent-tools` (names, depth 2; `TOOLS-AND-KEYS.md` headings only, no section mentions reverse engineering), `C:\Users\777\.claude\skills`, `C:\Users\777\nad-lan\nad-lan-co-il\.claude\skills`, `C:\Users\777\nad-lan\nad-lan-co-il\skills` (names filtered on reverse|forum|community|social|pro), `C:\Users\777\Documents` (two levels), `C:\Users\777`, Desktop, Downloads, `.claude\projects`, `.claude\plugins`, and every `SKILL.md` under `.claude` (depth 4) for the phrase.

Closest match: the user skill **`serp-reverse-engineer`** at `C:\Users\777\.claude\skills\serp-reverse-engineer\` (SKILL.md 3.3 KB, `scripts/onpage.py`, `scripts/d4s.py`). How to use it:
1. Invoke the skill (`serp-reverse-engineer`), after running `google-israel-manual-search` yourself to get the real SERP.
2. For each top-10 site plus 3 strong foreign equivalents: page identity and full heading outline (`scripts/onpage.py OUTDIR url...` for server HTML; browser `get_page_text` or DataForSEO content parsing for SPAs).
3. Record why it ranks, its technology (framework, map library, pixels, data APIs from network requests), every product feature (filters, cards, contact flow, alerts, AI), and its content DNA.
4. Output a feature matrix, an n-gram delta against our page, a "fairness declaration" (each component, where seen, how we rebuilt it; never copy code, text, photos or listing data), and a build brief.
5. Rules: read-only, no bot-check bypass, no 301/noindex/indexing proposals, Hebrew report.
For a forum, the targets would be product sites (Israeli and foreign professional communities) rather than a keyword SERP; the same matrix and fairness declaration apply. Also related: project skill `competitor-profiling` in `nad-lan-co-il\.claude\skills`.

---

## What was verified and what was not
- Verified by reading code: every file:line above.
- Not determined: live versions of any file; live counts of cards; whether `nadlan_pro_network_on`, `nadlan_procard_enabled`, `nadlan_register_contacts`, `nadlan_whatsapp_e164` and `nadlan_owner_whatsapp` are set live and to what; whether the claim-prompt and the broker re-claim dead end behave as read; contents of `inc/admin-control.php`, `inc/related-content.php`, `inc/final-hardening.php`, `inc/broker-drop.php` beyond lines 1-240.
