# Cowork FULL-OPERATOR Runbook v3.2 — drive ChatGPT, harvest, publish (autonomous, non-stop)

> **This is the single source of truth for the autonomous article batch. Cowork reads this whole file at session start, then runs the loop in §6 non-stop until §13 stop condition fires.** The owner has ZERO time. Cowork does the ENTIRE pipeline: opens ChatGPT, pastes the prompt, ChatGPT writes the Hebrew article, Cowork harvests the output, sanity-checks, publishes to WordPress, wires internal links, visual-QA, commits, moves on. No approvals. No pausing. No questions to the owner.

> **THE IRON CONSTRAINT: Cowork NEVER writes article prose in Hebrew. ChatGPT writes every word.** Anthropic tokens are expensive; ChatGPT Plus is flat-rate. Cowork's job is orchestration + publishing, never authorship. If you ever feel the urge to "just write this section myself" — STOP. Re-prompt ChatGPT instead.

---

## §1. The full pipeline (what Cowork owns end-to-end)

```
  ┌──────────────────────────────────────────────────────────────────────┐
  │ COWORK (you) — the operator. Runs the whole thing, start to finish.   │
  └──────────────────────────────────────────────────────────────────────┘
       │
       │ 1. open browser → chatgpt.com → Project "Nadlan COIL projects articles"
       │ 2. NEW chat (fresh chat per article — never reuse)
       │ 3. paste the next prompt (from the 23-prompt Drive Doc) + append the
       │    code-block fallback line
       │ 4. send. ChatGPT thinks 60-120s and WRITES the Hebrew article.
       │
       ▼
  ┌──────────────────┐     output lands in ONE of two places:
  │     ChatGPT      │ ──► (a) Drive /inbox/ as <slug>.html  (if Drive-write works)
  │  writes Hebrew   │ ──► (b) a ```html code block in the chat (fallback, reliable)
  └──────────────────┘
       │
       │ 5. Cowork HARVESTS:
       │    - poll Drive /inbox/ ~2 min. If Doc present → read it.
       │    - else → read the ```html code block from the chat DOM (NOT canvas)
       │      and save it to Drive /inbox/ yourself.
       │ 6. sanity-check (hard gate — §8)
       │ 7. publish to WordPress (REST) — UPDATE for rewrites, CREATE for new (§9)
       │ 8. wire internal links (§10)
       │ 9. visual-QA the live URL (§11)
       │ 10. commit + push site-state.md (§12)
       │ 11. move Drive Doc to /published/
       │ 12. NEXT article — no pause, no approval
       ▼
  Live page on nad-lan.co.il  +  git commit  +  /published/ Doc  =  the only output channels
```

**Key reliability principle:** Cowork drives ChatGPT's INPUT (paste + send + occasional follow-up). Cowork reads ChatGPT's OUTPUT from a stable source — the Drive Doc, or the chat's fenced code block. **Never extract from ChatGPT Canvas** (it virtualizes and broke v2). The code-block fallback sidesteps Canvas entirely because fenced code blocks stay in the normal message DOM with a Copy button.

---

## §2. Access — you have ALL of this. Never say "I don't have access."

| Capability | How | Proof it works |
|---|---|---|
| Browser / computer-use | Your built-in browser tooling | You drove ChatGPT in v2 — same capability |
| ChatGPT Plus | Owner is logged in at chatgpt.com; Project exists | Project name: "Nadlan COIL projects articles" |
| Google Drive read+write | Drive MCP tools (create_file, read_file_content, get_file_metadata, search_files, list_recent_files, copy_file) | Folders + Docs already created via these tools |
| WordPress REST (admin) | env: WP_BASE_URL, WP_USER, WP_APP_PASSWORD | healthcheck + users/me in preflight |
| Git push | repo at /home/user/nad-lan-co-il, branch claude/charming-meitner-mwVEW | — |
| GitHub MCP | scope the-new-ben/nad-lan-co-il | — |

If a tool call fails, it is a transient error to retry per §13 — NOT a missing capability. You have everything. Use it.

---

## §3. Locations — memorize

```yaml
chatgpt:
  url:          "https://chatgpt.com/"
  project_name: "Nadlan COIL projects articles"

drive:
  root:        "1okuUY-MNyWwyBLQqyH0kgftZk1eOw9Zp"   # nadlan-articles-output
  inbox:       "13jtpQF9wsYdeT78UQvvcHPnhtbKCPeWA"    # harvest target
  published:   "1uMSVp0RYBICgbJj8pmPRjq-C4hD637xe"    # move here after publish
  prompts_dir: "1WqpI1oBTmkYv8w6OqdYbgFwnoiNQ2Bd9"
  SYSTEM_doc:  "1efl0pGloDXUCQWv3XyChVSUxK8Amz8WSzw4bMM8OKsw"
  PROMPTS_doc: "1zBBuran1LuPkAkIS-Aip98dZ1xQlCuFSnfo76mxfNFU"  # ← the 23 ChatGPT prompts
  QUEUE_doc:   "1aAJXLFmYqVKiDkWBhN3Xi-quxtDcPF5iqdMYu1zDK5U"  # backbones + Hebrew titles
  # create these two on first need:
  needs_owner: "(create subfolder 'needs-owner' in root)"
  rejected:    "(create subfolder 'rejected' in root)"

repo:
  path:   "/home/user/nad-lan-co-il"
  branch: "claude/charming-meitner-mwVEW"
  css:    "skills-templates/article-guide.css"   # inline verbatim on every publish
```

---

## §4. Mandatory reading at session start (one pass)

1. `AGENTS.md`, `HANDOFF.md`
2. `skills/README.md`, `skills/cowork-briefing.md`
3. `skills/site-state.md` — **last 8 blocks**
4. `skills/strategy-master.md`, `skills/copywriting-skill.md`
5. `skills/internal-linking-hub-spoke.md`, `skills/article-guide-design-pattern.md`
6. `skills/runbook-cowork-article-batch-v3.md` — §6.1 sanity-check + §6.2 publish script live here
7. `skills-templates/article-guide.css`
8. Drive `SYSTEM_doc` (voice contract) + `PROMPTS_doc` (cache all 23 prompts) + `QUEUE_doc` (backbones)

---

## §5. Preflight (60s)

```bash
curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck"                                            # plugin alive
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,name,roles"  # administrator
git branch --show-current                                                                       # claude/charming-meitner-mwVEW
```
- List Drive `inbox` (13jtp…) — confirm reachable.
- Read Drive `PROMPTS_doc` — cache all 23 prompt blocks (delimited by `═══`).
- Create Drive subfolders `needs-owner/` and `rejected/` in root if absent.
- Open browser to chatgpt.com, confirm logged in, confirm the Project is visible.

Any hard failure → investigate once, retry, else §13 stop.

---

## §6. The master loop (run non-stop)

```
QUEUE = [A1..A5 rewrites, B1..B18 new]   # order fixed, see §7
i = 0
while i < len(QUEUE):
    slug = QUEUE[i].slug

    # --- already harvested? (owner or earlier session may have dropped it) ---
    doc = drive_find_in_inbox(slug)
    if not doc:
        # --- DRIVE ChatGPT to produce it ---
        html = drive_chatgpt(slug, QUEUE[i].prompt)   # §6A — returns HTML or None
        if html is None:
            log("ChatGPT produced nothing usable for "+slug+"; will retry later")
            move_to_end(QUEUE, i)        # try again after the others
            continue
        doc = drive_save_inbox(slug, html)            # Cowork saves to /inbox/

    html = drive_read(doc)

    # --- HARD GATE ---
    ok, fails = sanity_check(html, slug)              # §8
    if not ok:
        retries[slug] += 1
        if retries[slug] <= 2:
            # re-prompt ChatGPT with the specific failures appended
            html2 = drive_chatgpt(slug, QUEUE[i].prompt + revise_note(fails))
            if html2: drive_overwrite(doc, html2); continue
        drive_move(doc, NEEDS_OWNER); comment(doc, fails); log(slug+" → needs-owner: "+fails)
        i += 1; continue

    # --- PUBLISH + WIRE + QA + LOG ---
    wp_id = publish(slug, html)            # §9  UPDATE if rewrite else CREATE
    wire_internal_links(slug, wp_id)       # §10
    visual_qa_live(slug)                   # §11 — fix+republish if dirty
    commit_and_push(slug, wp_id)           # §12
    drive_move(doc, PUBLISHED)
    i += 1                                  # NEXT — no pause, no approval
```

### §6A. `drive_chatgpt(slug, prompt)` — driving ChatGPT in the browser

1. In the ChatGPT Project, click **New chat** (fresh chat — NEVER reuse a chat for two articles).
2. Paste the prompt for this slug (from the cached `PROMPTS_doc`), then **append this fallback line** so output is always harvestable:
   ```
   חשוב: פלוט את כל ה-HTML כבלוק קוד אחד ```html ... ``` בתוך הצ'אט. אל תשתמש ב-Canvas. אם אתה יכול לשמור Google Doc בתיקייה id 13jtpQF9wsYdeT78UQvvcHPnhtbKCPeWA בשם <slug>.html — עשה גם את זה. רק ה-HTML, בלי הקדמה.
   ```
3. Send. **Do not sit and screenshot ChatGPT in a loop** (burns tokens). Instead: wait ~90s, then poll Drive `/inbox/` for `<slug>.html`.
4. **If Drive Doc appeared** → use it (preferred; ChatGPT's Drive-write worked).
5. **If not after ~2-3 min** → ChatGPT output in the chat. Read the **fenced ```html code block** from the chat (stable DOM, has a Copy button — NOT Canvas). That HTML is the article. Save it to Drive `/inbox/` yourself via `create_file`.
6. **If the chat shows Canvas instead of a code block** → send one follow-up in the SAME chat: `אנא פלוט מחדש את אותו מאמר כבלוק קוד ```html יחיד בצ'אט, בלי Canvas.` Then re-harvest.
7. **If the chat is blank / errored / rate-limited** → wait 60s, send the prompt once more in a NEW chat. If blank twice → return None (loop will retry this slug after the others).
8. Return the harvested HTML.

**Token discipline:** the expensive thing is screenshots in a tight loop. After sending, switch to cheap Drive MCP polling. Only return to the ChatGPT tab to read the code block once (when Drive came up empty) or to send a single follow-up.

---

## §7. The queue (fixed order — REWRITES first)

Part A — **REWRITES** → `POST /wp-json/wp/v2/pages/<wp_id>` (URL preserved):

| # | slug | wp_id | parent_id | parent path |
|---|---|---|---|---|
| A1 | mortgage-repayment-capacity | 519 | 121 | /mortgage-calculator/ |
| A2 | reverse-mortgage | 512 | 121 | /mortgage-calculator/ |
| A3 | pinui-binui-tenant-guide | 543 | 73 | /urban-renewal/ |
| A4 | tama-38-rights-obligations | 540 | 73 | /urban-renewal/ |
| A5 | tama-38-contract-checklist | 547 | 73 | /urban-renewal/ |

Part B — **NEW** → `POST /wp-json/wp/v2/pages` with `parent`:

| # | slug | parent_id | parent path |
|---|---|---|---|
| B1 | choosing-urban-renewal-developer | 73 | /urban-renewal/ |
| B2 | sale-of-apartments-law | 11 | /real-estate-lawyer/ |
| B3 | option-period-real-estate | 11 | /real-estate-lawyer/ |
| B4 | form-4-occupancy-permit | 11 | /real-estate-lawyer/ |
| B5 | building-permit-citizen-guide | 11 | /real-estate-lawyer/ |
| B6 | when-real-estate-lawyer-required | 11 | /real-estate-lawyer/ |
| B7 | who-pays-broker-fees | 70 | /selling-apartment/ |
| B8 | selling-without-broker | 70 | /selling-apartment/ |
| B9 | pricing-apartment-for-sale | 70 | /selling-apartment/ |
| B10 | reduced-capital-gains-sale | 70 | /selling-apartment/ |
| B11 | bank-supervision-project | 421 | /investment/ |
| B12 | investment-via-company | 421 | /investment/ |
| B13 | real-estate-leverage | 421 | /investment/ |
| B14 | airbnb-israel-regulation | 421 | /investment/ |
| B15 | buying-apartment-step-by-step | 9 | /buying-apartment/ |
| B16 | new-vs-second-hand | 9 | /buying-apartment/ |
| B17 | office-for-rent | 79 | /commercial-real-estate/ |
| B18 | store-for-rent | 79 | /commercial-real-estate/ |

Hebrew titles, intents, sibling-exclusions, h2 backbones → Drive `QUEUE_doc`. The ready-to-paste ChatGPT prompts → Drive `PROMPTS_doc`.

---

## §8. Sanity-check (HARD GATE — refuse to publish if any fails)

Full implementation in `skills/runbook-cowork-article-batch-v3.md` §6.1. Non-negotiable:

- 0 em-dashes `—`; 0 `{index=N}`; 0 `Source+N` / `AADE+N`; 0 `[1]` footnotes
- 0 preamble (`<p>להלן`, `<p>הנה המאמר`)
- 0 opener `במאמר זה (נסקור|נפרט|נדון|נציג|נראה)` outside the disclaimer div
- 0 body-byline (`<p>מאת ` outside disclaimer)
- h2 count 6-11; **all h2 unique** (duplicate = stitched output → fail)
- word count 1800-3500 (from stripped text)
- ≥20 numeric data points; ≥15 law/section/regulator refs
- ≥1 `div.cards`, ≥1 `<table>`, ≥3 `div.note`, ≥2 `div.cta`
- 0 forbidden phrases: חשוב להבין / חשוב מאוד / חשוב לזכור / חשוב לבדוק / ראוי לציין / במילים אחרות / עולם הנדל / בעידן / ללא ספק / אינסוף / באופן כללי / בסופו של דבר / לסיכום / כפי שראינו / חוד החנית / אבן יסוד / מורכבות ההליך / דורשת הבנה מעמיקה

Borderline (e.g., 1790 words) still **fails** — re-prompt; the bar is the bar.

---

## §9. Publish (use the proven script in v3 runbook §6.2)

- Inline `skills-templates/article-guide.css` verbatim in `<style>`.
- Wrap in `<!-- nadlan-guide-wrap-v1 -->` + `<!-- wp:html -->…<!-- /wp:html -->`.
- Inject Person+Article JSON-LD graph (template in §6.2).
- Append BYLINE + DISCLAIMER + LAWYER_CTA at publish time (NOT in ChatGPT's draft — body-byline is forbidden).
- **REWRITE:** `POST /wp-json/wp/v2/pages/<wp_id>`; assert response slug == expected (fail loudly if WP appended `-2`).
- **NEW:** `POST /wp-json/wp/v2/pages` with `parent=<parent_id>`.
- Yoast meta: `_yoast_wpseo_title`, `_yoast_wpseo_metadesc`, `_yoast_wpseo_focuskw`.
- `status: publish`, `author: 1`.

BYLINE / DISCLAIMER / CTA (consistent across the batch):
```
BYLINE     = <div class="byline" dir="rtl"><div class="avatar" aria-hidden="true">בב</div><div class="who"><b>מאת בן בטש, עורך דין</b><span>חבר לשכת עורכי הדין בישראל · רישיון 29020 · עודכן 2026</span></div></div>
DISCLAIMER = <div class="disclaimer" dir="rtl">אין לראות באמור ייעוץ משפטי; כל מקרה נבחן לגופו. לייעוץ עם עו"ד בן בטש: <a href="/real-estate-lawyer/">/real-estate-lawyer/</a>.</div>
LAWYER_CTA = <div class="cta" dir="rtl"><a class="btn" href="/real-estate-lawyer/">קביעת ייעוץ עם עו"ד בן בטש</a><a class="btn secondary" href="/purchase-tax-calculator/">מחשבון מס רכישה</a></div>
```

---

## §10. Internal link wiring (same iteration)

a) Add link FROM parent pillar TO this spoke (idempotent markers from `internal-linking-hub-spoke.md`).
b) 2-3 reciprocal sibling links — read the cluster map first, do not cannibalize.
c) One relevant tool link (purchase-tax-calculator / mortgage-calculator).
d) Verify no duplicate insertion via the marker.

## §11. Visual QA (before "done")

`curl -s https://nad-lan.co.il/<parent>/<slug>/` → grep for em-dash, `{index=`, opener `במאמר זה נציג/נפרט/נדון`, `Source+`, `AADE+`, `<p>מאת `. If dirty → fix in WP (`POST pages/<id>`), re-check. Don't advance until clean.

## §12. Commit + log (per article)

Append a `site-state.md` block (template §9 of v3 runbook): words / numbers / law refs / sanity result / links wired / QA outcome. Then:
```bash
git add skills/site-state.md
git commit -m "Article: <slug> (id <N>) - [REWRITE|NEW] - <words>w/<nums>nums/<laws>laws"
git push -u origin claude/charming-meitner-mwVEW   # retry 4x: 2/4/8/16s on network error
```

---

## §13. Obstacle playbook — pre-resolved

**ChatGPT shows Canvas, not a code block** → follow-up in same chat: re-emit as a single ```html code block, no Canvas. Re-harvest.
**ChatGPT output in chat but truncated** (cut mid-tag) → follow-up: "המשך מהמקום שנעצרת, אותו בלוק קוד." Concatenate. If still truncated twice → New chat, resend whole prompt.
**ChatGPT blank / errored** → 60s wait, resend in a NEW chat. Blank twice → skip slug to end of queue, retry later.
**ChatGPT rate-limited** ("you've reached your limit") → back off 10-15 min doing parallel work (§14), then resume. Do NOT spam.
**ChatGPT didn't save to Drive** → expected; harvest the code block and save to Drive yourself.
**Drive Doc title not `<slug>.html`** → if body is article HTML, rename via metadata update, process.
**Drive Doc has a preamble line** → strip the first non-tag line before publish; don't reject for that alone.
**Drive Doc empty** → wait 60s, re-read; still empty → comment + leave in inbox, continue.
**Two Docs same slug** → process newest (createdTime), move older to /rejected/.
**Doc slug not in queue** → move to /rejected/, log, continue.
**WP REST 5xx** → retry 3x (5/15/30s); else save payload `/tmp/<slug>-pending.json`, continue; retry pendings every 4 articles.
**WP REST 401/403** → auth lost → log to site-state.md, commit, STOP (§ owner regenerates app password).
**WP 200 but Yoast meta missing** → follow-up POST with same `meta`; if still missing, page is live → log, patch later, continue.
**WP slug collision** → if it's an A1-A5 target, that's the page you're updating (good). If a stray draft, delete the draft then publish. NEVER ship a `-2` slug.
**Drive MCP auth error** → retry once; else save drafts to `/tmp/<slug>.html`, publish from disk (you don't need Drive to publish), sync to Drive when it recovers.
**Git push rejected (non-fast-forward)** → `git fetch && git rebase origin/claude/charming-meitner-mwVEW`; for site-state.md conflicts keep both blocks (append-only); push again.
**Browser lost the ChatGPT session / logged out** → cannot drive ChatGPT → switch to harvest-only mode: keep processing any Docs already in /inbox/; log that ChatGPT login is needed; continue the rest of the pipeline. Do NOT write articles yourself.
**Sanity-check fails 3+ times** → /needs-owner/ + detailed note; continue. Never lower the bar.
**You feel like writing a section yourself** → forbidden. Re-prompt ChatGPT.
**You want to "save context"/"compact"** → don't; the harness handles it.
**You want to ask the owner anything** → don't; re-read this file; the answer is here.

---

## §14. Parallel work while ChatGPT thinks / inbox idle / rate-limited

Rotate one per idle cycle: visual-QA last 3 published; verify each pillar (121,73,11,70,421,9,79) links DOWN to its current spokes; cannibalization scan for upcoming slugs; IndexNow ping last 5 publishes; refresh site-state tail.
**Never** during idle: write article prose, modify the design/CSS, force-push, change strategy, prompt extra ChatGPT chats in parallel.

---

## §15. Stop conditions (the ONLY reasons to halt)

1. WP auth 401/403 persistent → log + stop.
2. All 23 slugs live OR in /needs-owner/ with reason → write §16 final report + stop.
3. Next commit would damage the repo → stop, log.
4. ChatGPT login lost AND inbox empty AND nothing left to publish → log "waiting for ChatGPT login", stop politely.

Anything else → **continue.** Never ask "should I continue?". Never wait for approval. Output channels are: live pages, branch commits, /published/ folder.

## §16. Final report (only at stop #2)

Append "Batch v3.2 final report" to site-state.md + one chat message: shipped/23, needs-owner + reasons, avg words/numbers/law-refs, top 3 lessons, next recommended step.

---

## §17. The one rule above all

ChatGPT writes the Hebrew. You orchestrate and publish. You never author, never pause, never ask. Every prompt you paste becomes a live, sanity-checked, design-compliant, internally-linked page on nad-lan.co.il within minutes. Read the queue. Drive ChatGPT. Harvest. Publish. Repeat 23 times. Report once.

_Created 2026-05-31 by Claude Code (claude-opus-4-7). v3.2 = full-operator mode (Cowork drives ChatGPT end-to-end). Supersedes v3 (Drive-bridged, owner-prompts) and v2 (deprecated)._
