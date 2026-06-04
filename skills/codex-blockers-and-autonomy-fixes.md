# Codex Blockers & Autonomy Fixes — why it "stalls / asks permission / can't paste", and the fixes

> **Who this is for:** the owner + any agent driving **Codex CLI (logged into ChatGPT Pro)**
> on the owner's PC to run the nad-lan.co.il article loop (SERP research in Chrome → prompt
> ChatGPT like a human → generate image via ChatGPT → publish to WordPress → email proof).
>
> **Why this exists:** Codex produced 6 articles/hour one day, then regressed to "asking
> permission for everything", "I cannot copy", "I cannot paste", and making excuses. This
> doc is the researched, sourced root-cause + fix so we stop fighting the symptom. Pairs
> with `agent-tooling-strategy.md` (brain/hands division) and
> `codex-plugin-access-and-deploy.md` (REST is already a sanctioned content channel — §5).

---

## 0. The honest reframing (read this first)

The three complaints are **three different problems with three different fixes** — and two
of them are NOT "laziness", they are real, documented limits:

1. **"Asks permission for everything"** → a **configuration** problem (Codex `approval_policy`),
   *not* a prompting problem. You cannot prompt it away; you set it once. There are also real
   Codex bugs where the approval toggles don't stick — so the CLI + config.toml is the reliable lever.
2. **"I cannot copy / cannot paste"** → often **literally true**. Browser clipboard is gated
   (secure context + tab focus + real user-gesture + permission), and a *scripted* paste event
   is `isTrusted:false`, so the browser inserts **nothing** (MDN). The fix is **not** to bully
   Codex into the impossible — it is to give it a **method that actually works** (publish via
   REST, read the DOM, type — see §3).
3. **"Lazy / makes excuses / great yesterday, stalling today"** → textbook **context bloat**
   over a long thread and/or a **silent model-version regression**. Fix with thread hygiene,
   reasoning effort, model pinning, and a persistence instruction (§4).

**Bottom line:** give Codex a sanctioned, working path and the autonomy config, and the
"excuses" disappear because the action is now actually possible and pre-approved.

---

## 1. Symptom → root cause → fix (master table)

| Symptom (what the owner sees) | Real root cause | Fix (section) |
|---|---|---|
| Asks "Approve once / this session / reject" before every command | `approval_policy` not set to `never`/`on-request`; "don't ask again" bug | §2 — set config.toml + launch flags |
| Re-asks for the *same* read-only command (line numbers changed) | Known Codex approval bug (#6395, #10187) | §2 — `approval_policy="never"` + workspace-write |
| "Agent (full access)" / `never` ignored in the IDE | IDE/desktop bug (#5038, #13117) | §2 — use the **CLI**, not the IDE; WSL2 on Windows |
| "I cannot copy the text" from ChatGPT | Clipboard read needs focus + permission + gesture; "Document is not focused" | §3 — read the message from the **DOM**, don't use the OS clipboard |
| "I cannot paste into the editor" (Gutenberg) | Scripted paste is `isTrusted:false` → inserts nothing; Gutenberg is React/contenteditable | §3 — **publish via REST**, or Code-editor textarea, or type |
| "Pasted but it vanished / reformatted" | React valueTracker drops direct DOM writes; Gutenberg re-parses pasted HTML | §3 — native-setter + `input` event, or wrap in `<!-- wp:html -->` |
| Stops mid-task, one-line changes, "I'll let you do it" | Context bloat in a long thread; pre-5.3 preamble early-stop | §4 — one thread per article + persistence line |
| "Dumb as a rock this week" / declares done falsely | Silent model-version regression | §4 — pin last-good model; raise reasoning effort; define DONE |

---

## 2. Blocker 1 — stop the permission prompts (CONFIG, one-time owner setup)

**This is set by the owner once; it is not something Codex can "decide" to stop doing.**

### `~/.codex/config.toml` (user-level; precedence: CLI flag > profile > config.toml > default)
```toml
# Autonomous local content loop on the owner's own machine + own WordPress site.
approval_policy = "never"          # or "on-request" for a safer middle ground
sandbox_mode    = "workspace-write"

[sandbox_workspace_write]
network_access = true              # Codex needs Chrome + REST calls to the live site
```

### Or per-launch on the CLI (equivalent, overrides config):
```bash
codex --ask-for-approval never --sandbox workspace-write
# shorthand:           -a never -s workspace-write
# full bypass (only in a trusted env): codex --dangerously-bypass-approvals-and-sandbox   # alias: --yolo
```

**Verified (official OpenAI Codex docs):**
- `approval_policy` ∈ `untrusted | on-request (default) | never | granular`.
- `sandbox_mode` ∈ `read-only | workspace-write (default) | danger-full-access`.
- `--ask-for-approval`/`-a`, `--sandbox`/`-s`, `--dangerously-bypass-approvals-and-sandbox` (`--yolo`).
- `--full-auto` still works but is **deprecated in `codex exec`** — prefer the explicit pair above.
- Docs: developers.openai.com/codex/config-reference, /codex/agent-approvals-security, /codex/cli/reference.

**Known bugs to route around (community + GitHub issues):**
- The **VS Code / desktop** apps sometimes ignore `never` / "Agent (full access)" and re-prompt
  (issues #5038, #10187, #11298, #13117, #15770). **Practical advice: drive the loop from the
  Codex CLI, not the IDE.** On Windows, **WSL2** behaves far better than native Windows for approvals.
- In the IDE you must explicitly enable "use config.toml" and mark the folder a Trusted Workspace, then restart.

---

## 3. Blocker 2 — "cannot copy / cannot paste" in Chrome (give it a method that WORKS)

### Why it genuinely fails (verified, MDN / web.dev)
- The async Clipboard API (`navigator.clipboard.readText/writeText`) requires **all** of:
  **secure context (HTTPS/localhost)**, **the tab to be focused/active**, **a recent real
  user gesture (transient activation)**, and the **`clipboard-read`/`clipboard-write` permission**.
  Fail any one → `NotAllowedError` / "Document is not focused". Backgrounded automation tabs fail the focus gate constantly.
- A **scripted** `ClipboardEvent('paste')` is `isTrusted:false` → MDN: *"this will not affect the
  document's contents."* So "synthetically pasting" into Gutenberg inserts **nothing**.
- **Gutenberg** is a React + `contenteditable` surface; a raw `el.value = html` is dropped by React's
  valueTracker, and real pastes get re-parsed/sanitized into blocks. **TinyMCE** (Classic) lives in an
  **iframe** — the textarea you see is just a backing store.

### The working method — decision order (most robust first)

**① Don't round-trip the OS clipboard. Publish via WordPress REST API (already sanctioned — see `codex-plugin-access-and-deploy.md` §5).**
```bash
# content = raw HTML body; UTF-8 Hebrew is fine; --data @file avoids RTL shell-quoting pain
curl -X POST https://nad-lan.co.il/wp-json/wp/v2/posts \
  --user "USER:APP_PASSWORD" \
  -H "Content-Type: application/json" \
  --data @article.json     # {"title":"...","status":"draft","content":"<h2>...</h2>", "slug":"ascii-slug"}
```
- Auth = **Application Password** (WP ≥ 5.6), generated at wp-admin → Users → *your user* → Application Passwords, over HTTPS. If Codex doesn't hold one → **stop and ask the owner to generate it** (that's a real owner-only step, not an excuse).
- Images: `POST /wp-json/wp/v2/media` (multipart), then set `featured_media` on the post. Alt text + caption per `image-pipeline.md`.
- This is the path that makes "I can't paste" obsolete — there is no editor to paste into.

**② Read ChatGPT's output from the DOM, not the clipboard.** Don't click "Copy" and read the OS
clipboard. Read the assistant message text/HTML directly:
```js
// in the ChatGPT tab, headful + focused
const msg = [...document.querySelectorAll('[data-message-author-role="assistant"]')].pop();
const html = msg.innerText;   // or pull the <pre><code> block if you asked for raw HTML
```

**③ If the UI must be used:** Gutenberg **Code editor** (`Ctrl+Shift+Alt+M`) exposes a plain
`<textarea>`. Set it with the native setter + dispatch `input`, then switch back to Visual:
```js
const ta = document.querySelector('.editor-post-text-editor');           // code-editor textarea
const set = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set;
set.call(ta, '<!-- wp:html -->\n'+html+'\n<!-- /wp:html -->');           // wrap so it isn't re-parsed
ta.dispatchEvent(new Event('input', {bubbles:true}));
```
Classic editor: use the **Text** (HTML) tab `<textarea#content>`, or `tinymce.activeEditor.setContent(html); tinymce.activeEditor.save();`.

**④ Last resort: type it** (trusted key events, no clipboard needed), chunked for long Hebrew —
`page.keyboard.type(chunk)` / Playwright `locator.pressSequentially()`.

**⑤ Only if a real `Ctrl+V` path is unavoidable:** run **headful**, `page.bringToFront()` to focus,
and grant permissions (Playwright `context.grantPermissions(['clipboard-read','clipboard-write'],{origin})`;
Puppeteer needs CDP `Browser.grantPermissions` with `clipboardReadWrite` **and** `clipboardSanitizedWrite`).
Headless does **not** touch the OS clipboard.

---

## 4. Blocker 3 — "lazy / excuses / great yesterday, stalling today"

This is the textbook profile of **context bloat** and/or a **silent model regression**, not character.

- **One thread per article, not one thread per project.** Long threads "bloat context and worse
  results over time" (official best-practices). Use `/compact` when long, or start a fresh session
  per article. The loop is *per-article* anyway — start clean each block.
- **Reasoning effort:** `model_reasoning_effort = "high"` (or `xhigh`) for these long agentic
  research-and-publish runs; medium is fine for trivial edits.
- **Pin a known-good model** if a version regressed (users reverted 5.5→5.4 when 5.5 degraded).
- **Persistence instruction** (verified, OpenAI's own wording — put in AGENTS.md or the task prompt):
  > "You are an agent — keep going until the task is completely resolved before yielding. Persist
  > end-to-end: do not stop at analysis or partial fixes; carry the change through implementation,
  > verification, and a clear summary. Default to implementing with reasonable assumptions; do not
  > end your turn with clarifications unless you are truly blocked."
- **Define DONE as the QA checklist** (raw HTML only, exact H2 plan, 0 em/en dashes, 0 AI-tells,
  0 internal terms, unique H2s, cards/table/notes present, ASCII slug, correct parent, hub-spoke
  links, Yoast title/meta, one H1, image present). An unambiguous done-condition stops false "done".
- **Pre-5.3 only:** remove "tell me your plan first" preambles — OpenAI says they cause early stops.

---

## 5. The corrected loop flow (keeps the human-like Chrome generation, fixes publishing)

```
1. Codex CLI (approval=never, sandbox=workspace-write, reasoning=high), fresh thread per article.
2. Chrome (real, visible) → live Google Israel SERP research. Record titles/meta/PAA/AIO/formats. NO shortcuts.
3. Chrome → type the strict blueprint prompt into ChatGPT web UI like a human. ChatGPT writes the
   long Hebrew HTML article (>=1800 words for spokes) AND generates the image. Codex never writes
   the Hebrew article itself and never generates the image itself.
4. Extract the article HTML from the ChatGPT DOM (§3 ②). Download the generated image file.
5. PUBLISH via WordPress REST (§3 ①): POST media → POST/UPDATE post with raw HTML, ASCII slug,
   correct parent, Yoast title/meta, featured image. Do NOT fight the Gutenberg paste path.
6. QA on the live (cache-busted) URL against the DONE checklist. Fix or STOP+report — never fake.
7. Document: append to site-state.md + the relevant blueprint; update this file's field log (§7).
8. Hebrew email to benbetesh@gmail.com with all proofs (URL, parent, siblings, SERP proof, ChatGPT
   evidence, image status, QA result, cannibalization statement, repo updates, blockers, next plan, honesty line).
```

**Hard rules (carry into every prompt):** real visible Chrome only (no internal/headless browser
for the ChatGPT step); prompt ChatGPT like a human (no OpenAI API, no scraping internal endpoints —
ToS per `agent-tooling-strategy.md`); never self-write Hebrew articles; never self-generate images;
never compromise on SERP/sub-research; if cannibalization / weak research / ChatGPT failure /
auth-plugin-deploy blocker / QA failure → **stop that article and report honestly**, do not publish.

---

## 6. Ready-to-paste steering prompt for Codex

> A copy of the current steering prompt also lives with the owner; keep this block in sync.

```
You are continuing the nad-lan.co.il article production loop. Work in English in chat to save tokens.

NON-NEGOTIABLE FIRST STEP: read/re-check the repo knowledge before acting —
skills/serp-reverse-engineering-article-generation.md, skills/runbook-cowork-article-batch-v3.md,
skills/strategy-master.md (section 13), skills/copywriting-skill.md, skills/internal-linking-hub-spoke.md,
skills/article-qa-audit.md, skills/url-slug-governance.md, skills/image-pipeline.md,
skills/codex-blockers-and-autonomy-fixes.md, and the latest skills/site-state.md blocks.

You are an agent. Keep going until the task is completely resolved before yielding. Persist
end-to-end: do not stop at analysis or partial fixes; implement, verify, and summarize. Default to
implementing with reasonable assumptions; do not end your turn with clarifications unless truly blocked.

You previously "could not copy/paste". That is expected and is NOT your job to brute-force. Browser
clipboard is gated and scripted paste inserts nothing. Use the working method instead:
  - Generate the article + image by prompting ChatGPT in a REAL visible Chrome window, like a human.
  - Read ChatGPT's output from the DOM (assistant message / code block), not the OS clipboard.
  - PUBLISH via the WordPress REST API (POST /wp-json/wp/v2/media then POST/UPDATE /wp-json/wp/v2/posts
    with raw HTML, ASCII slug, correct parent, Yoast title/meta, featured image). Do NOT paste into
    Gutenberg. If you lack the Application Password, STOP and ask the owner — do not invent a workaround.

You are launched with approval_policy=never and sandbox_mode=workspace-write, so you do NOT need to
ask permission for local commands, Chrome control, or REST calls to nad-lan.co.il. Proceed.

Per article: pick ONE keyword; check anti-cannibalization FIRST; analyze the live Google Israel /
Hebrew SERP (top organic titles+meta, first-rank opening DNA, PAA/related, AI Overview/featured
snippet, result formats, competitor headings, image patterns, authoritative primary sources). Build
a STRICT ChatGPT blueprint prompt (target keyword, ASCII slug, parent pillar, sibling/synonym pages
NOT to cannibalize, exact H2 plan, verified data+sources, forbidden AI-tells/internal terms, raw
HTML-only, first-paragraph DNA, image brief). ChatGPT output must be long and beat competitors
(>=1800 words for spokes, more when SERP depth requires) with data, tables, FAQ, examples, direct answers.

NEVER write the Hebrew article yourself. NEVER generate the image yourself. NEVER compromise on
SERP/sub-research. Use only Chrome + the ChatGPT web UI (no API, no internal endpoints).

QA before publish (this is the definition of DONE): raw body HTML only; exact H2 plan; 0 em/en
dashes; 0 AI-tell phrases; 0 internal terms; no citation artifacts; unique H2s; enough numbers +
primary-source references; cards/table/notes present; one public H1 via WP title only; ASCII slug;
correct parent; hub-spoke internal links; Yoast title/meta; schema/design wrapping; live cache-busted
visual check. One realistic relevant image where feasible (SEO filename, Hebrew descriptive alt,
caption, surrounding sentence, no logos/text/watermarks, media-log note).

If cannibalization, weak research, ChatGPT failure, Drive/WP/auth/plugin/deploy blocker, or QA
failure: STOP that article and report honestly. Do not publish.

Context hygiene: one fresh thread per article (avoid bloat). Use high reasoning effort.

After each PUBLISHED article: send a Hebrew email to benbetesh@gmail.com with live page URL, parent
pillar URL, sibling/synonym/supporting links, hierarchy explanation, SERP proof summary (top
competitors + why followed), ChatGPT proof link/evidence, image proof/status, QA checklist result,
cannibalization statement, what was updated in repo/site-state, blockers, next article plan, and an
honesty statement that you did your best and did not skip research.

Document any new blocker + its fix in skills/codex-blockers-and-autonomy-fixes.md (§7 field log) and
append a block to skills/site-state.md. Keep Chrome tabs minimal — leave only deliverable proof tabs.
```

---

## 7. Field log (Codex: append real results here — keep it short)

- _(template)_ `YYYY-MM-DD` — blocker hit: `<what>` → fix that worked: `<what>` → publish method used: `REST | code-editor | type`.

---

## 8. Sources (V = verified/official, C = community/issue-tracker)

**Approval / autonomy:** V developers.openai.com/codex/config-reference, /agent-approvals-security,
/cli/reference, /learn/best-practices. C GitHub openai/codex #5038, #6395, #10187, #11298, #13117,
#15770; community.openai.com approval threads.
**Laziness / regression:** V codex_prompting_guide & gpt-5-1_prompting_guide (cookbook), /codex/prompting.
C openai/codex #6384, #12225; community.openai.com degradation threads (5.2/5.4/5.5); HN 46902638.
**Clipboard:** V MDN Clipboard API (readText/writeText, security), execCommand, ClipboardEvent;
web.dev async-clipboard; Playwright grantPermissions/keyboard. C Puppeteer #7888/#10211, Cypress
#18198, Playwright #29509, chromedriver headless reports.
**WordPress publish:** V WP REST API Posts/Media + Application Passwords; WP-CLI `post create`;
TinyMCE `setContent`; Gutenberg Code-editor shortcut. C gutenberg #16990/#61923, React native-setter pattern.
**AGENTS.md / prompting:** V developers.openai.com/codex/guides/agents-md, agents.md; GitHub Blog
"great AGENTS.md (2,500 repos)". C blakecrosley AGENTS.md patterns; arXiv 2601.20404 (don't auto-bloat).

---

## Revision log
- 2026-06-04 — Created (Claude, the "brain"). Captures the researched fix for Codex regressing into
  permission-asking, copy/paste failures, and laziness during the article loop. Codex maintains §7.
