# Cowork Runbook v3 — Drive-bridged article batch (autonomous, sequential, non-stop)

> **For Claude Cowork (fresh session, no memory of prior work). Read this whole file once at session start.** Then execute the loop in §6 non-stop until the article queue is empty. **Do not ask the owner whether to continue, do not pause between articles, do not message the owner unless §10 stop condition fires.**

> **v3 supersedes v2 (2026-05-30).** v2 had Cowork drive ChatGPT through the browser DOM — that hit Canvas virtualization, blank-response glitches, lockout risk. v3 inverts the architecture: **the owner runs ChatGPT inside a Project; ChatGPT writes the article into a Google Drive folder; Cowork polls the folder and publishes.** Cowork never touches the ChatGPT DOM. ChatGPT's 60-120s thinking time is no longer a bottleneck — Cowork does other work during it.

> **This is a learning project. Every decision and lesson lives in `skills/site-state.md`. Append after every article. Future sessions read it back as their memory.**

---

## §0. The new architecture (the whole picture)

```
                    OWNER                              YOU (Cowork)
              ┌─────────────────┐               ┌────────────────────────┐
              │ ChatGPT Project │               │  watch Drive inbox     │
              │ "nadlan article │  writes Doc   │  →  read HTML          │
              │     batch"      │ ──────────►   │  →  sanity-check       │
              │ (Plus, Project  │  to Drive     │  →  wrap design+schema │
              │ +Drive sync)    │  inbox/       │  →  publish via REST   │
              └─────────────────┘               │  →  wire links         │
                       │                        │  →  visual QA          │
                       │                        │  →  move Doc → published/ │
                       │                        │  →  commit site-state    │
                       │                        └────────────────────────┘
                       ▼
              Drive folder structure:
              /NadLan/nadlan-articles-output/
                  ├── prompts/        ← SYSTEM + template (don't touch)
                  ├── inbox/          ← owner drops ChatGPT outputs here
                  ├── published/      ← you move them here after publish
                  └── ARTICLE QUEUE   ← the live list of what to write
```

**Critical:** Cowork does NOT prompt ChatGPT. Cowork does NOT browse the ChatGPT UI. The owner does that. Cowork's job starts at the Drive inbox.

---

## §1. Owner facts (cached — do not re-ask)

```yaml
owner:
  name_hebrew:  "בן בטש"
  title:        "עו\"ד"
  bar_number:   29020
  bar_url:      "https://www.israelbar.biz/lawyer-fd/?lawyer=Cqcs/1T4N0I"
  other_site:   "https://jus-tice.co.il/"
  email_site:   "info@nad-lan.co.il"
  phone_cell:   "0525101555"   # SOLE phone — mobile. Use everywhere (tel:, wa.me, schema). No other number.
  # phone_work (036916454) RETIRED 2026-06-01 by owner — outdated landline. Do NOT reintroduce.
  address:      "וולנברג ראול 18, תל אביב יפו"
  wp_admin_user_id: 1
  drive_account: "mistabrajustice@gmail.com"

drive_folders:
  root:       "1okuUY-MNyWwyBLQqyH0kgftZk1eOw9Zp"   # nadlan-articles-output
  inbox:      "13jtpQF9wsYdeT78UQvvcHPnhtbKCPeWA"   # ChatGPT drops here
  published:  "1uMSVp0RYBICgbJj8pmPRjq-C4hD637xe"   # move after publish
  prompts:    "1WqpI1oBTmkYv8w6OqdYbgFwnoiNQ2Bd9"   # SYSTEM + template

queue_doc_id: "1aAJXLFmYqVKiDkWBhN3Xi-quxtDcPF5iqdMYu1zDK5U"   # ARTICLE QUEUE

design:
  palette:       "GREEN canonical (Codex)"
  pattern_skill: "skills/article-guide-design-pattern.md"
  reference_url: "https://nad-lan.co.il/design-demo-green/"
  green_css:     "skills-templates/article-guide.css"  # ~3,297 bytes, inline verbatim
```

---

## §2. Mandatory reading at session start

Cowork starts from scratch each session. **You have no memory.** Before doing anything, read in this order:

1. `AGENTS.md` (repo root) — cross-agent contract
2. `HANDOFF.md` (repo root) — credentials, current state
3. `skills/README.md` — skills tree index
4. `skills/cowork-briefing.md` — project history + voice
5. `skills/site-state.md` — **read the last 8 blocks**, that is the live situation
6. `skills/strategy-master.md` — the SEO/business brief
7. `skills/copywriting-skill.md` — voice + forbidden phrases
8. `skills/internal-linking-hub-spoke.md` — cluster map (current)
9. `skills/article-guide-design-pattern.md` — the green design contract
10. `skills/runbook-cowork-article-batch-v3.md` — this file

Then run §3 preflight.

---

## §3. Preflight (60 seconds)

```bash
# 1. REST + auth + plugin alive
curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck"
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,name,roles"

# 2. Git branch
git remote -v ; git branch --show-current   # expect claude/charming-meitner-mwVEW

# 3. Last 8 site-state blocks
tail -240 skills/site-state.md

# 4. Drive access (use Drive MCP)
# List the inbox folder (1WqpI1oBTmkYv8w6OqdYbgFwnoiNQ2Bd9 — see §1)
# Expect: 0+ Google Doc files when ready

# 5. Load the canonical green CSS into a session variable
GREEN_CSS=$(cat skills-templates/article-guide.css)
```

Healthcheck must show `plugin: nadlan-config`, `users/me` must show `roles: [administrator]`, Drive must list the inbox folder. If any fails → §10 stop.

---

## §4. The queue

The owner-maintained article queue lives at Drive doc id `1aAJXLFmYqVKiDkWBhN3Xi-quxtDcPF5iqdMYu1zDK5U`. Read it once at session start. It contains:

- **Part A: 5 rewrites** (replace existing pages because their content is below the rank-first bar). These have existing WordPress page IDs you UPDATE, not create.
- **Part B: 18 new articles** (create new WordPress pages).

The owner adds finished Docs to the `inbox/` folder. **The Doc's filename is the slug.** You match the filename against the queue to know whether it's a rewrite (update existing id) or a new article (create page).

**Rewrite map (Part A):**

| inbox filename | WP page id | parent pillar | what's wrong with the current version |
|---|---|---|---|
| `mortgage-repayment-capacity.html` | 519 | /mortgage-calculator/ (121) | 1287 words (too short), 10 numbers, 7 law refs, padded prose |
| `reverse-mortgage.html` | 512 | /mortgage-calculator/ (121) | 1737 words, 0 law refs — no legal citation density |
| `pinui-binui-tenant-guide.html` | 543 | /urban-renewal/ (73) | AI padding phrases, only 4 numbers in 2,661 words |
| `tama-38-rights-obligations.html` | 540 | /urban-renewal/ (73) | 3 numbers, 7 law refs — thin data |
| `tama-38-contract-checklist.html` | 547 | /urban-renewal/ (73) | 3 numbers, 20 law refs — thin data |

**For rewrites:** when you publish, `requests.post(f'{BASE}/wp-json/wp/v2/pages/{EXISTING_ID}', ...)` to UPDATE, do NOT create a new page (the URL must stay the same).

**New articles map (Part B):** 18 articles. Slug → pillar id mapping is in the queue Doc.

---

## §5. The architectural switch — what's different in v3

**Was (v2, broken):**
- Cowork sends prompt to ChatGPT via browser
- ChatGPT thinks 60-120s → Cowork blocks, eats context window
- ChatGPT renders to Canvas → Cowork can't extract → falls back to Gemini → quality drops
- Cowork bridges ChatGPT tab → WordPress tab via clipboard (broken) or fragment-carry (works but fragile)
- One ChatGPT failure delays the whole pipeline

**Is (v3, working):**
- Owner sends prompt to ChatGPT inside the Project (SYSTEM doc auto-loaded as Project context)
- ChatGPT thinks, then writes the article HTML directly into Drive `inbox/` folder as a Google Doc named `<slug>.html`
- Owner moves on — owner doesn't wait for Cowork to fetch
- Cowork polls Drive every 30s. When a new file appears, Cowork reads it, sanity-checks, wraps, publishes, moves to `published/`
- During the 60-120s ChatGPT think-time, Cowork is doing OTHER work in parallel: previous article's link wiring, visual QA on already-published pages, site-state commit, scanning for cannibalization on upcoming queue items, IndexNow pings
- One ChatGPT slow article doesn't delay anything — Cowork just keeps processing whatever is in the inbox

**Cowork's loop is now I/O-bound on Drive polling, not on ChatGPT DOM.** No Canvas, no blank-response, no extraction acrobatics.

---

## §6. The per-article loop (execute non-stop)

```python
# Pseudocode — implement in real Python with Drive MCP + WP REST
while True:
    new_files = drive.list_inbox()  # files in 1WqpI1oBTmkYv8w6OqdYbgFwnoiNQ2Bd9 ... wait, INBOX is 13jtp...
    # Drive inbox folder id: 13jtpQF9wsYdeT78UQvvcHPnhtbKCPeWA
    if not new_files:
        # Do parallel work: visual QA on last published, append site-state, scan
        # next-queue cannibalization, ping IndexNow for last 3 publishes
        do_parallel_work()
        sleep(30)
        continue

    for doc in sorted(new_files, key=lambda f: f.createdTime):
        slug = doc.title.replace('.html','')
        html = drive.read_file_content(doc.id)
        if not sanity_check(html, slug):
            # Move Doc to a sibling "rejected/" folder with a note; alert owner
            continue
        if slug in REWRITE_MAP:
            publish_or_update(REWRITE_MAP[slug], html, slug, action='update')
        else:
            publish_or_update(None, html, slug, action='create')
        wire_internal_links(slug)
        visual_qa_live(slug)
        commit_site_state(slug)
        drive.move_to_published(doc.id)
```

**The point:** Cowork is reactive to the Drive inbox, not driven by ChatGPT timing.

---

## §6.1 Sanity-check (the bar — refuse to publish if any fails)

```python
def sanity_check(html, slug):
    if html.count('—') > 0: return fail('em-dash')
    if '{index=' in html: return fail('chatgpt index marker')
    if re.search(r'[A-Za-z]+\+\d+', html): return fail('perplexity citation')
    if re.search(r'<p[^>]*>\s*להלן|<p[^>]*>\s*הנה המאמר', html): return fail('preamble')

    body_no_disc = re.sub(r'<div class="disclaimer".*?</div>',' ', html, flags=re.S)
    if re.search(r'במאמר זה (?:נסקור|נפרט|נדון|נציג|נראה)', body_no_disc): return fail('opener')
    if re.search(r'<p[^>]*>\s*מאת', body_no_disc): return fail('body-byline')

    h2_list = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.S)
    if len(h2_list) < 6 or len(h2_list) > 11: return fail(f'h2 count {len(h2_list)}')
    if len(set(h2_list)) != len(h2_list): return fail('duplicate h2')

    text = re.sub(r'<[^>]+>', ' ', html); words = len(text.split())
    if words < 1800: return fail(f'too short {words}')
    if words > 3500: return fail(f'too long {words}')   # owner says long is OK, but cap somewhere

    nums = len(re.findall(r'\d[\d,]*\s*(?:₪|%|מיליון|אלף|שנים|חודשים)', html))
    if nums < 20: return fail(f'data thin {nums}')

    laws = len(re.findall(r'(?:סעיף|חוק|תקנה|רשות המסים|בנק ישראל|תיקון)', html))
    if laws < 15: return fail(f'law refs thin {laws}')

    if html.count('class="cards"') < 1: return fail('no cards grid')
    if html.count('<table') < 1: return fail('no table')
    if html.count('class="note"') < 3: return fail('note < 3')
    if html.count('class="cta"') < 2: return fail('cta < 2')

    for p in ['חשוב להבין','חשוב מאוד','חשוב לזכור','חשוב לבדוק','ראוי לציין','במילים אחרות',
              'עולם הנדל','בעידן','ללא ספק','אינסוף','באופן כללי','בסופו של דבר','לסיכום',
              'כפי שראינו','חוד החנית','אבן יסוד','מורכבות ההליך','דורשת הבנה מעמיקה']:
        if p in html: return fail(f'AI-tell: {p}')

    return ok
```

**Failure handling:** when sanity fails, do NOT patch in place. Move the Doc to a new `rejected/` folder, append a comment file with the failure list, and continue with the next Doc. The owner re-prompts ChatGPT for that slug with the failure list, ChatGPT regenerates, drops a new Doc in inbox, you process it. **Two retries max, then escalate** (§10).

---

## §6.2 Publishing template (the proven script)

```python
import os, requests, json, html as htmlmod, re
USER=os.environ['WP_USER']; PWD=os.environ['WP_APP_PASSWORD']; BASE=os.environ['WP_BASE_URL'].rstrip('/')
A=(USER,PWD)

INNER = drive_doc_text  # read from Drive
# Last-mile defensive scrub (idempotent)
INNER = INNER.replace(' — ',' - ').replace('—',' - ')
INNER = re.sub(r'\{index=\d+\}', '', INNER)

SLUG, TITLE, PARENT_ID, FOCUS_KW, METADESC = lookup_from_queue(slug)
GREEN_CSS = open('skills-templates/article-guide.css').read()

PERSON_ARTICLE_JSONLD = json.dumps({
  "@context":"https://schema.org",
  "@graph":[
    {"@type":"Person","@id":"https://nad-lan.co.il/#person-ben-betesh",
     "name":"בן בטש","jobTitle":"עורך דין מקרקעין","honorificPrefix":"עו\"ד",
     "url":"https://nad-lan.co.il/author/ben-betesh/",
     "sameAs":["https://www.israelbar.biz/lawyer-fd/?lawyer=Cqcs/1T4N0I","https://jus-tice.co.il/"],
     "email":"info@nad-lan.co.il","telephone":"+972-3-691-6454",
     "address":{"@type":"PostalAddress","streetAddress":"וולנברג ראול 18","addressLocality":"תל אביב יפו","addressCountry":"IL"},
     "memberOf":{"@type":"Organization","name":"לשכת עורכי הדין בישראל","identifier":"29020"}},
    {"@type":"Article","headline":TITLE,
     "url":f"https://nad-lan.co.il/{parent_slug}/{SLUG}/",
     "datePublished":"2026-05-31","dateModified":"2026-05-31",
     "author":{"@id":"https://nad-lan.co.il/#person-ben-betesh"},
     "publisher":{"@type":"Organization","name":"נדלן חכם","url":"https://nad-lan.co.il/"},
     "inLanguage":"he-IL","isAccessibleForFree":True}
  ]
}, ensure_ascii=False)

BYLINE = '<div class="byline"><div class="avatar" aria-hidden="true">בב</div><div class="who"><b>מאת בן בטש, עורך דין</b><span>חבר לשכת עורכי הדין בישראל · רישיון 29020 · נבדק לאחרונה: 2026-05-31</span></div></div>'
DISCLAIMER = '<div class="disclaimer">אין לראות במאמר זה ייעוץ משפטי. כל מקרה דורש בדיקה פרטנית של נסיבותיו. ליצירת קשר עם עו"ד בן בטש לייעוץ ראשוני: <a href="/real-estate-lawyer/">/real-estate-lawyer/</a>.</div>'
LAWYER_CTA = '<div class="cta"><a class="btn" href="/real-estate-lawyer/">קבעו ייעוץ עם עו"ד בן בטש</a><a class="btn secondary" href="/purchase-tax-calculator/">מחשבון מס רכישה</a></div>'

content = (
  '<!-- nadlan-guide-wrap-v1 -->\n'
  '<!-- wp:html -->\n'
  f'<script type="application/ld+json">{PERSON_ARTICLE_JSONLD}</script>\n'
  f'<style>{GREEN_CSS}</style>\n'
  '<div class="nadlan-guide"><div class="wrap">\n'
  + BYLINE + '\n' + INNER + '\n' + LAWYER_CTA + '\n' + DISCLAIMER + '\n'
  '</div></div>\n'
  '<!-- /wp:html -->\n'
  '<!-- /nadlan-guide-wrap-v1 -->'
)

payload = {
  'title': TITLE, 'slug': SLUG, 'content': content, 'status': 'publish',
  'parent': PARENT_ID, 'author': 1,
  'meta': {
    '_yoast_wpseo_title': f'{TITLE} | נדלן חכם',
    '_yoast_wpseo_metadesc': METADESC,
    '_yoast_wpseo_focuskw': FOCUS_KW,
    '_yoast_wpseo_is_cornerstone': '',
  }
}

if existing_page_id:
    r = requests.post(f'{BASE}/wp-json/wp/v2/pages/{existing_page_id}', auth=A, json=payload, timeout=60)  # UPDATE
else:
    r = requests.post(f'{BASE}/wp-json/wp/v2/pages', auth=A, json=payload, timeout=60)  # CREATE
print('PUBLISHED:', r.status_code, r.json().get('id'), r.json().get('link'))
```

---

## §7. Parallel work during Drive idle (the patience answer)

The owner explicitly asked: when ChatGPT takes 1-2 minutes to think, you don't sit and wait. You do **other useful work**. Allowed parallel tasks:

1. **Visual QA on last 3 published pages** — fetch live URL, grep for em-dash/index markers/preamble
2. **Append site-state.md** for the article you just shipped, then commit
3. **Pre-research the next queue item's SERP** — open Google Hebrew incognito, capture top-10 + PAA + related searches into a scratch note, but do NOT prompt ChatGPT (that's the owner's job)
4. **Cannibalization scan** — for the next 3 queue slugs, check no existing page targets the same intent
5. **Pillar back-link audit** — make sure every spoke's pillar has a link back DOWN to the spoke
6. **Update `internal-linking-hub-spoke.md` cluster map** with newly published spokes
7. **IndexNow ping** the last 5 publishes via the plugin's healthcheck endpoint to confirm Bing knows

**NEVER do during idle:** prompt ChatGPT yourself (the owner does that), modify the design pattern, change pillar pages without owner approval, push destructive git commands.

---

## §8. The five rewrites — sanity check that the URL stays the same

When publishing a rewrite, the WordPress page ID stays the same → URL stays the same. Critical. Google has already indexed those URLs (or will soon). Changing the URL = losing the SEO signal we built.

Rewrite-specific payload addition:
```python
payload['id'] = EXISTING_ID   # ensures update, not create
# Verify after PUT
assert r.json()['id'] == EXISTING_ID
assert r.json()['slug'] == SLUG  # WordPress sometimes appends -2 if conflict
```

If WordPress refuses (slug collision because the existing page used the same slug), that means we're updating the right page. Good.

---

## §9. site-state log + commit (after every article)

```markdown
### 2026-05-31 HH:MM - Cowork - [REWRITE|NEW] `<slug>` (id <N>)
- Source: Drive Doc <doc_id> by ChatGPT-Project
- Target query: <query from queue>
- Cluster: <pillar slug>
- Word count: <N>  | numbers: <N>  | law refs: <N>
- Internal links: pillar ✓, siblings ✓ (<ids>), tool ✓, lawyer CTA ✓
- Yoast title+metadesc+focuskw set ✓
- Sanity-check: PASS (or list of fixes applied)
- Visual QA passed ✓ <live URL>
- Doc moved to /published/
```

Commit per article (small commits = recovery is easy if anything breaks).

---

## §10. Stop conditions (the ONLY reasons to halt)

Halt and message the owner **only** when:

1. REST returns 401/403/404 for `users/me` → auth lost, owner needs to re-login
2. REST 5xx repeated for 5+ minutes
3. A specific Drive Doc failed sanity-check TWICE (after the owner re-prompted)
4. A page revision shows accidental wipe — RESTORE FROM REVISION before continuing
5. Queue Doc empty AND inbox empty AND all queue items have a corresponding published page → write §11 final report and END

**Do NOT halt for:**
- Inbox empty for 5 minutes → owner is still working, do parallel work and keep polling
- One article fails sanity-check → move to rejected/, comment the failure, continue with the next
- ChatGPT being slow → not your problem; you're not prompting it
- Owner being away → continue, owner pre-approved the whole queue
- Asking "should I continue?" — NEVER. Continue.

---

## §11. Final report (write only when queue + inbox are empty)

Append to `skills/site-state.md` and announce in chat:

```markdown
## Batch v3 final report - 2026-05-31

**Queue completed:** A1-A5 rewrites + B1-B18 new = 23 articles.

**Average word count:** <N>
**Average numbers/article:** <N>
**Average law refs/article:** <N>

**Sanity-check rejections + re-prompts:** <N>

**Honesty - what went wrong:**
- <each rejection cause>
- <any rewrite that needed 2 passes>

**Scorecard:**
- Google Blueprint compliance: <N>/10
- Design adherence: <N>/10
- E-E-A-T (byline, schema, sources): <N>/10
- Internal-link wiring: <N>/10
- Anti-cannibalization: <N>/10
- Hebrew prose quality: <N>/10
- Word count adherence: <N>/10
- Data density (numbers + law refs): <N>/10

**Next step recommendation:** <link strategy, monetization repositioning, or city pillars per strategy §2.4>
```

---

## §12. Lessons from earlier sessions (for context)

These are real lessons from the prior sessions. Don't re-learn them.

| Lesson | Source |
|---|---|
| Don't run parallel ChatGPT prompts — triggers blank responses | 2026-05-30 v2 session |
| Cowork driving ChatGPT DOM hits Canvas virtualization unpredictably | 2026-05-30 v2 session |
| ChatGPT "Extended" reasoning mode truncates ~6KB articles | 2026-05-30 v2 session |
| Gemini ignores prompt rule about body-byline (adds "מאת:" inside prose) | 2026-05-30 v2, article 543 |
| Gemini uses padded openers ("חוד החנית", "מהווה כיום", "אבן יסוד") | 2026-05-31 scan |
| Duplicate H2 sections happen when ChatGPT's 2 truncated passes get stitched | 2026-05-30, article 493 |
| "במאמר זה" is allowed in the disclaimer ("אין לראות במאמר זה ייעוץ") but forbidden as opener | 2026-05-30, article 519 |
| The article-guide-design-pattern green palette is canonical, not the Lovable luxury | owner-locked 2026-05-30 |
| Stripe doesn't work on the site; payments go through Green Invoice (Morning) | owner-confirmed |
| The site's authority strategy is ON HOLD pending re-architecture toward an editorial brand (not a lawyer-referral funnel). Don't add new license-number callouts on monetization surfaces. | owner-consulted 2026-05-30 |

---

## §13. The one rule above all rules

**You are autonomous. The owner is away running ChatGPT and pouring Docs into the inbox. Your job: every Doc that lands in inbox/ becomes a live, sanity-checked, wired-up, design-compliant page on nad-lan.co.il within minutes of landing. You don't stop. You don't ask permission. You report only via site-state.md (per article) and the §11 final report (once).**

Read the queue. Poll the inbox. Process. Move on. Repeat.

---

_Created 2026-05-31 by Claude Code (claude-opus-4-7). v3 supersedes v2. The Drive-bridged architecture is the durable solution; earlier browser-driven approaches are deprecated._
