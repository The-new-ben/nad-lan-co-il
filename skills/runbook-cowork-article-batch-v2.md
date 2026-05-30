# Cowork Runbook v2 — Strategy Completion Batch (autonomous, sequential)

> **For Claude Cowork.** Read this whole file once at session start. Then execute non-stop, one article at a time, in the order below. **Do not stop to ask the owner for approval between articles.** The owner has pre-approved the full backlog. Stop ONLY on the conditions in §11. When the backlog is done, write the final report in §12 and end the session.

> **Version note (2026-05-30):** v2 supersedes the original runbook. v1 successfully shipped 9 high-quality articles, then surfaced two real failure modes (Cowork's stitching produced duplicate H2 sections on page 493; Gemini opened page 519 with the forbidden "במאמר זה נפרט"). v2 has hardened sanity-check, tighter source preference, the verified browser bridges, and the **specific 24-article backlog**.

---

## §0. Owner-supplied facts (DO NOT re-ask)

```yaml
owner:
  name_hebrew:  "בן בטש"
  title:        "עו\"ד"
  bar_number:   29020
  bar_url:      "https://www.israelbar.biz/lawyer-fd/?lawyer=Cqcs/1T4N0I"
  other_site:   "https://jus-tice.co.il/"
  email_site:   "info@nad-lan.co.il"
  phone_cell:   "0525101555"
  phone_work:   "036916454"
  address:      "וולנברג ראול 18, תל אביב יפו"
  wp_admin_user_id: 1

design:
  palette:        "GREEN canonical (Codex)"  # owner-locked
  pattern_skill:  "skills/article-guide-design-pattern.md"
  reference_url:  "https://nad-lan.co.il/design-demo-green/"
  green_css:      "skills-templates/article-guide.css"  # 3,297 bytes - inline this verbatim

cta_targets:
  primary:                "/real-estate-lawyer/"
  calculator_purchase_tax: "/purchase-tax-calculator/"
  calculator_mortgage:    "/mortgage-calculator/"
  pricing_join:           "/join-pro/"
```

---

## §1. THE BACKLOG — execute in this exact order (24 articles)

Each row: `slug | target_query | parent_pillar_id | priority_reason`. Cowork does them sequentially top-to-bottom. **Do not re-order. Do not skip. Do not parallelize.**

### Phase A — Tax-legal cluster (highest E-E-A-T moat, 3 articles)

| # | Slug | Target query (Google Hebrew) | Parent | Why first |
|---|---|---|---|---|
| 1 | `purchase-tax-first-home` | מס רכישה דירה ראשונה 2026 | 92 (real-estate-tax-advisor) | 5,400/mo, ₪4 CPC, your moat |
| 2 | `purchase-tax-investor` | מס רכישה משקיע / דירה שנייה 2026 | 92 | high CPC, lawyer SERP |
| 3 | `capital-gains-tax-guide` | מס שבח 2026 — המדריך המלא | 92 | broad pillar, complements 493 |

### Phase B — Urban renewal cluster (highest revenue per deal, 4 articles)

| # | Slug | Target query | Parent | Why |
|---|---|---|---|---|
| 4 | `tama-38-rights-obligations` | תמא 38 — זכויות וחובות 2026 | 73 (urban-renewal) | 1,000/mo, owner's revenue sweet spot |
| 5 | `pinui-binui-tenant-guide` | פינוי בינוי מדריך לדייר | 73 | 6,600/mo |
| 6 | `tama-38-contract-checklist` | חוזה תמא 38 מה לבדוק | 73 | converts to legal-rep deals |
| 7 | `choosing-urban-renewal-developer` | איך לבחור יזם להתחדשות עירונית | 73 | high commercial intent |

### Phase C — Lawyer-cluster completion (5 articles)

| # | Slug | Target query | Parent |
|---|---|---|---|
| 8 | `sale-of-apartments-law` | חוק מכר דירות | 11 (real-estate-lawyer) |
| 9 | `option-period-real-estate` | תקופת אופציה במכר דירה | 11 |
| 10 | `form-4-occupancy-permit` | טופס 4 ואכלוס דירה מקבלן | 11 |
| 11 | `building-permit-citizen-guide` | תב"ע והיתרי בנייה לאזרח | 11 |
| 12 | `when-real-estate-lawyer-required` | עורך דין נדל"ן מתי חובה | 11 |

### Phase D — Selling cluster (4 articles, currently almost empty)

| # | Slug | Target query | Parent |
|---|---|---|---|
| 13 | `who-pays-broker-fees` | מי משלם דמי תיווך במכירת דירה | 70 (selling-apartment) |
| 14 | `selling-without-broker` | תהליך מכירת דירה ללא מתווך | 70 |
| 15 | `pricing-apartment-for-sale` | תמחור דירה למכירה | 70 |
| 16 | `reduced-capital-gains-sale` | מכירת דירה במס שבח מופחת | 70 |

### Phase E — Investment supporting spokes (4 articles)

| # | Slug | Target query | Parent |
|---|---|---|---|
| 17 | `bank-supervision-project` | ליווי בנקאי לפרויקט | 421 (investment) |
| 18 | `investment-via-company` | דירה להשקעה דרך חברה | 421 |
| 19 | `real-estate-leverage` | מינוף בנדל"ן | 421 |
| 20 | `airbnb-israel-regulation` | דירת Airbnb בישראל רגולציה | 421 |

### Phase F — Buying + Commercial gap-fills (4 articles)

| # | Slug | Target query | Parent |
|---|---|---|---|
| 21 | `buying-apartment-step-by-step` | קניית דירה צעד אחר צעד | 9 (buying-apartment) |
| 22 | `new-vs-second-hand` | דירה מקבלן או יד שנייה | 9 |
| 23 | `office-for-rent` | משרד להשכרה — מדריך לשוכר | 79 (commercial-real-estate) |
| 24 | `store-for-rent` | חנות להשכרה — מדריך לשוכר | 79 |

**Total batch:** 24 articles. At ~12-18 minutes per article (research + ChatGPT + publish + wire), the full backlog is ~6-8 hours of session time.

---

## §2. Pre-flight (60 seconds at session start, ONCE)

```bash
# 1. REST + auth alive
curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck"
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,name,roles"

# 2. Git branch
git remote -v ; git branch --show-current   # expect claude/charming-meitner-mwVEW

# 3. Last 6 site-state blocks
tail -180 skills/site-state.md

# 4. Load the canonical green CSS into a session variable
GREEN_CSS=$(cat skills-templates/article-guide.css)
```

Healthcheck must show `plugin: nadlan-config`, `users/me` must show `roles: [administrator]`. If either fails → §11 stop.

---

## §3. The writing engines — preference order + parallelism rule

**STRICT rule: only ONE prompt running at any time.** Two parallel prompts trigger ChatGPT's rate limit and **both** come back empty/blocked. Single-threaded only.

Preference order (try the next one only if the previous one is blocked/failing):

1. **ChatGPT Pro (Instant model)** — primary. Fastest, cleanest Hebrew, best at following the prompt format. Use Instant model, NOT Extended (Extended truncates at ~6KB and intermittently returns empty).
2. **Gemini Pro** — fallback when ChatGPT returns blank twice in a row. Quality good in Hebrew, but tends to use forbidden openers ("במאמר זה נפרט") so always sanity-check the lede after extraction.
3. **Claude Chat** — final fallback. Owner has a paid subscription. Use only when both above are blocked. Hebrew is solid but more verbose; trim 10-15%.

Between articles, wait 30-60 seconds before sending the next prompt — burst-rate avoidance.

---

## §4. Per-article loop (execute §4.1 through §4.10 for EACH of the 24)

### §4.1 Google Hebrew Blueprint (15-20 min per article, mandatory)

Open Google.co.il in incognito (Hebrew language, IL location). Search the target query (exact, no quotes). Record in a scratch note:

- Top 10 organic URLs + their title + meta in SERP
- All "אנשים גם שואלים" questions (expand each, get sub-questions)
- All "חיפושים קשורים"
- Featured snippet (if present, copy text + source URL)

For each top-10 result, classify in one line: type (law-firm/bank/blog/news/gov/aggregator), approximate word count, h2 sub-topics, missing angles.

**Output of §4.1** — capture before §4.2:
- Intent (1 sentence)
- Shared backbone (h2s ≥7 of 10 results cover — MANDATORY in our article)
- Differentiators from top-3 (1-2 unique angles to steal/improve)
- Gaps (PAA questions none of top 10 answered well — our edge)
- Outline (H1 + h2 list in order + Q&A at bottom)

**Do not skip §4.1.** Guessed intent → wrong article → no rank. The 19 articles already live all had genuine Blueprint research and that's why they look polished.

### §4.2 Primary sources

Every number cited needs a primary source with date. Allowed:

| Topic | Allowed source |
|---|---|
| Israeli market | `nadlan.gov.il`, `cbs.gov.il`, `boi.org.il`, `gov.il`, rulings, Knesset bills |
| Tax-legal | רשות המסים, חוק מיסוי מקרקעין specific sections |
| Urban renewal | חוק התחדשות עירונית, חוק פינוי ובינוי, תמ"א 38 |
| Mortgage | בנק ישראל הוראות, BoI quarterly |
| **Forbidden** | Madlan, Yad2, נדלן מאסטר, broker blogs, Wikipedia, ChatGPT summaries, vendor "industry reports" |

Format inline in Hebrew: `(מקור: בנק ישראל, מרץ 2026)`. Cut numbers without source.

### §4.3 The master ChatGPT prompt (paste verbatim, fill brackets)

**Use this single canonical prompt every time.** ChatGPT Instant model. One prompt = one article. Wait for completion fully before sending the next.

```
אתה עורך תוכן בכיר באתר נדל"ן פרמיום ישראלי (nad-lan.co.il) שמתמחה בייעוץ לקונים, מוכרים, משקיעים ודיירים. הטון: רגוע, סמכותי, עובדתי, ענייני. אתה לא מוכר - אתה מסביר. הקוראים הם ישראלים שמחפשים תשובה אמינה לפני החלטה משפטית או כלכלית גדולה.

כותב המאמר הנקרא: עו"ד בן בטש, חבר לשכת עורכי הדין בישראל (רישיון 29020).

הקוואריה היעד: "[TARGET QUERY]"
הכוונה (intent): "[ONE-SENTENCE INTENT FROM §4.1]"
הפילר האב: [PILLAR URL, e.g. /real-estate-tax-advisor/]
ספוקים אחים (אסור לחזור על תוכן): [SIBLING URLS]

מבנה חובה — חייב להופיע h2 לכל אחד מהבאים, על פי הסדר, ולכל אחד 2-4 פסקאות:

[BACKBONE H2 LIST — paste from §4.1 outline; 6-8 sections]

הסעיף האחרון לפני הסיכום חייב להיות h2 בשם "שאלות נפוצות", ומתחתיו 5-8 שאלות h3 שכל אחת מקבלת תשובה של 80-150 מילים בפסקה.

כללי כתיבה — חובה לעמוד בכולם:
1. עברית מדויקת, לא תרגום מאנגלית.
2. ללא em-dash (—). השתמש ב-",", ב-" - " (מקף רגיל עם רווחים), או ב-":".
3. אסור לפתוח את המאמר או פסקה ב: "במאמר זה", "המאמר הזה", "כאן נציג", "הנה". אסור "חשוב להבין", "ראוי לציין", "במילים אחרות", "בעידן הנוכחי", "בעידן הדיגיטלי", "עולם הנדל"ן", "אכן", "בהחלט", "ללא ספק", "בעולם שבו", "אינסוף", "באופן כללי", "בסופו של דבר", "לסיכום", "כפי שראינו", "מצד אחד...מצד שני" כפסקה.
4. אסור מילים פנימיות: ליד, leads, CRM, פילר, spoke, hub, cluster, intent, money page, UTM, KD, SEO.
5. כל מספר עם מקור ותאריך: "(מקור: בנק ישראל, מרץ 2026)". אם לא בטוח: "טעון אימות".
6. מספרים גדולים עם פסיקים: "1,978,745 ₪". אחוזים בלי רווח: "8%". טווחים עם en-dash: "1,978,745–2,347,040 ₪".
7. אסור להזכיר שאתה עוזר/מודל/בינה מלאכותית. אסור "המאמר נכתב על ידי" בגוף המאמר (זה כבר בבייליין).

מבנה ה-HTML של הפלט (חובה):
א. רק תגי <h2>, <h3>, <p>, <ul>, <li>, <strong>, <table>, <thead>, <tbody>, <tr>, <th>, <td>.
ב. אסור <h1>, <html>, <head>, <body>, <style>, <script>, markdown.
ג. dir="rtl" בכל בלוק חוסם (כל <p>, <h2>, <h3>, <ul>, <table>).
ד. עבור כל סעיף h2 חדש שיש בו 3 אופציות/קטגוריות, בנה גריד 3 כרטיסים:
   <div class="cards">
     <div class="card"><b>כותרת קצרה</b><p>הסבר 2-3 שורות.</p></div>
     ×3
   </div>
ה. עבור כל השוואה (טבלת מסים/תשואות/אזורים), השתמש ב-<table> עם <thead>+<tbody>.
ו. בכל סעיף ראשי הוסף בלוק נקודת-מפתח אחת:
   <div class="note">משפט אחד-שניים, ההמלצה הקריטית של הסעיף.</div>
ז. אחרי כל 2-3 סעיפים, הוסף קריאה לפעולה:
   <div class="cta"><a class="btn" href="/real-estate-lawyer/">קבעו ייעוץ עם עו"ד בן בטש</a></div>

תחילת הפלט: ישירות בפסקת פתיחה (2-3 פסקאות לפני ה-h2 הראשון). אסור "להלן", "הנה", הערות שקיפות, footnotes.
סוף הפלט: אחרי סעיף ה-h2 "שאלות נפוצות". אסור citation footnotes ("Source+9", "[1]", "{index=N}").
אורך: 1,800-2,500 מילים. ספור לפני שאתה שולח.

חובת בדיקה עצמית לפני התגובה:
- ספור h2 — חייב להיות 7-10 (כולל הראשון וכולל "שאלות נפוצות").
- ודא שאין כפילויות של h2 (כל h2 חייב להיות ייחודי).
- ספור מילים בעברית — חייב להיות בטווח 1,800-2,500.
- חפש "—" — חייב להיות 0.
- חפש "במאמר זה" / "להלן" / "הנה המאמר" — חייב להיות 0.
- חפש "{index=" / "+9" / "[1]" — חייב להיות 0.
- אם משהו לא תקין, תקן ושלח רק את התקין.

עכשיו כתוב את המאמר כ-HTML גולמי, מוכן להדבקה.
```

### §4.4 Extraction (the verified browser bridges)

When ChatGPT finishes, extract the HTML reliably. The methods that worked in v1, in order of reliability:

1. **Single `<pre>` extraction** — if ChatGPT used a code block (` ```html `), pull the `<pre>` text content. Cleanest.
2. **textContent on the largest assistant message** — when output rendered as literal text. Use `document.querySelector("article[data-message-author-role='assistant']").textContent`.
3. **innerText on the assistant message** — fallback when textContent fails.
4. **Local-browser slice relay** — only if same-browser tab is involved. Build the article in 800-char slices, append to a window-scoped buffer on the wp-admin tab, verify checksum at the end. **Do not use clipboard** — Chrome blocks writes from backgrounded tabs in MCP context.

After extraction, save to `/tmp/article.html`.

### §4.5 HARD sanity-check (the runbook's brain — DO NOT skip)

This is what catches the failure modes. Run all checks. Any **must be 0** failure → send back to ChatGPT with the failing items listed; do **not** patch in place.

```bash
F=/tmp/article.html

# Artifact checks (must be 0)
echo "em-dash: $(grep -c '—' $F)"
echo "{index=: $(grep -c '{index=' $F)"
echo "[N] cite: $(grep -oP '\[\d+\]' $F | wc -l)"
echo "word+N (Perplexity-style): $(grep -oP '[A-Za-z]+\+\d+' $F | wc -l)"
echo "preamble openers: $(grep -cE 'להלן|הנה המאמר|הערת שקיפות' $F)"

# Structure checks (must meet minimum)
H2_COUNT=$(grep -oc '<h2' $F)
H2_UNIQUE=$(grep -oP '<h2[^>]*>(.+?)</h2>' $F | sort -u | wc -l)
echo "h2 total: $H2_COUNT (must be 7-10)"
echo "h2 unique: $H2_UNIQUE (must equal h2 total - else duplicate sections!)"
echo "cards: $(grep -c 'class=\"cards\"' $F) (must be ≥ 1)"
echo "table: $(grep -oc '<table' $F) (must be ≥ 1)"
echo "note: $(grep -c 'class=\"note\"' $F) (must be ≥ 3)"
echo "cta: $(grep -c 'class=\"cta\"' $F) (must be ≥ 2)"

# Word count - the real one
WORD_COUNT=$(python3 -c "
import re,sys
t=re.sub(r'<[^>]+>',' ',open('$F').read())
t=re.sub(r'\s+',' ',t).strip()
print(len(t.split()))
")
echo "WORD COUNT: $WORD_COUNT (must be 1,800-2,500)"

# Forbidden opener phrases - ONLY flag outside the disclaimer
echo "במאמר זה (outside disclaimer): $(grep -o 'במאמר זה[^י]' $F | grep -v 'במאמר זה י' | wc -l)"

# Forbidden AI-tells
for p in "חשוב להבין" "ראוי לציין" "במילים אחרות" "עולם הנדל" "בעידן" "ללא ספק" "אינסוף" "באופן כללי" "בסופו של דבר" "לסיכום" "כפי שראינו"; do
  c=$(grep -c "$p" $F)
  [ "$c" != "0" ] && echo "FORBIDDEN: $p ($c)"
done

# Forbidden internal words
for w in "ליד" "leads" "CRM" "פילר" "intent" "SEO"; do
  c=$(grep -c "$w" $F)
  [ "$c" != "0" ] && echo "INTERNAL LEAK (check context): $w ($c)"
done

# Redundant byline in body
echo "byline-in-body: $(grep -cE '<p[^>]*>\s*המאמר נכתב על ידי' $F) (must be 0)"
```

**NEW in v2 — the two checks v1 was missing:**

- **`h2 unique != h2 total`** → ChatGPT/Cowork stitched two passes and produced duplicate sections (the page 493 bug). Send back: "יש כפילות בכותרות h2. כל h2 חייב להיות ייחודי. תקן ושלח שוב."
- **`במאמר זה (outside disclaimer)` > 0** → the AI-tell opener slipped in (the page 519 Gemini bug). Send back: "אסור לפתוח ב'במאמר זה'. נסח מחדש את הפסקה."

If ANY check fails, do NOT publish. Send back to ChatGPT (single turn) with the failing items listed verbatim. Wait for fixed version. If 2 attempts in a row fail the same check → fall back to Gemini → fall back to Claude Chat.

### §4.6 Word-count verification (extra-strict per owner 2026-05-30)

If `WORD_COUNT < 1,800` → article is too short. Send back: "המאמר קצר מדי. אורך נדרש 1,800-2,500 מילים. הוסף עומק לסעיפים [LIST 2 WEAKEST]. שלח מחדש."

If `WORD_COUNT > 2,800` → padding suspected, trim. Send back: "המאמר ארוך מדי. צמצם ל-1,800-2,500 מילים. מחק חזרות וסעיפים שלא תורמים. שלח מחדש."

**Never publish under 1,800 words.** Cowork must verify word count is real (run the Python wc command), not trust the chat model's claim.

### §4.7 Publish (the proven script template)

```python
import os, requests, json, html as htmllib
USER=os.environ['WP_USER']; PWD=os.environ['WP_APP_PASSWORD']; BASE=os.environ['WP_BASE_URL'].rstrip('/')
A=(USER,PWD)

INNER = open('/tmp/article.html').read()
# Last-mile defensive scrub (cheap, idempotent)
INNER = INNER.replace(' — ', ' - ').replace('—', ' - ')
import re
INNER = re.sub(r'\{index=\d+\}', '', INNER)

SLUG          = "[from backlog]"
TITLE         = "[from backlog - full Hebrew title]"
PARENT_ID     = [from backlog]
FOCUS_KW      = "[target query verbatim]"
METADESC      = "[150-160 chars, factual + what reader gets + soft CTA]"

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
     "url":f"https://nad-lan.co.il/[NESTED_PATH]/{SLUG}/",
     "datePublished":"2026-05-30","dateModified":"2026-05-30",
     "author":{"@id":"https://nad-lan.co.il/#person-ben-betesh"},
     "publisher":{"@type":"Organization","name":"נדלן חכם","url":"https://nad-lan.co.il/"},
     "inLanguage":"he-IL","isAccessibleForFree":True}
  ]
}, ensure_ascii=False)

BYLINE = '<div class="byline"><div class="avatar" aria-hidden="true">בב</div><div class="who"><b>מאת בן בטש, עורך דין</b><span>חבר לשכת עורכי הדין בישראל · רישיון 29020 · נבדק לאחרונה: 2026-05-30</span></div></div>'
DISCLAIMER = '<div class="disclaimer">אין לראות במאמר זה ייעוץ משפטי. כל מקרה דורש בדיקה פרטנית של נסיבותיו. ליצירת קשר עם עו"ד בן בטש לייעוץ ראשוני: <a href="/real-estate-lawyer/">/real-estate-lawyer/</a>.</div>'
LAWYER_CTA = '<div class="cta"><a class="btn" href="/real-estate-lawyer/">קבעו ייעוץ עם עו"ד בן בטש</a><a class="btn secondary" href="/purchase-tax-calculator/">מחשבון מס רכישה</a></div>'

content = (
  '<!-- nadlan-guide-wrap-v1 -->\n'
  '<!-- wp:html -->\n'
  f'<script type="application/ld+json">{PERSON_ARTICLE_JSONLD}</script>\n'
  f'<style>{GREEN_CSS}</style>\n'
  '<div class="nadlan-guide"><div class="wrap">\n'
  + BYLINE + '\n'
  + INNER + '\n'
  + LAWYER_CTA + '\n'
  + DISCLAIMER + '\n'
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

r = requests.post(f'{BASE}/wp-json/wp/v2/pages', auth=A, json=payload, timeout=60)
print('PUBLISHED:', r.status_code, r.json().get('id'), r.json().get('link'))
```

### §4.8 Wire internal links (3 directions + lawyer CTA)

Per `internal-linking-hub-spoke.md`:
1. **Up to pillar** — one anchor in opening 200 words of the article body. Anchor text = pillar's H1.
2. **Across to 2 siblings** in same cluster — in body prose, not as a list. Anchor text = sibling's target query.
3. **Down to 1-2 tools** — `/purchase-tax-calculator/`, `/mortgage-calculator/`, `/buy-vs-rent/`.
4. **Lawyer CTA block** is already in the publish template.

Then update the PILLAR to link down to the new spoke (idempotent `<!-- nadlan-hub-related-v1 -->` block).

### §4.9 Visual QA on the live URL

```bash
URL="$WP_BASE_URL/[parent-path]/[slug]/"
curl -sL "$URL?nc=$(date +%s)" -o /tmp/visual.html
echo "size: $(wc -c </tmp/visual.html)"
grep -c 'class="nadlan-guide"' /tmp/visual.html       # must be 1
grep -c 'מאת בן בטש'           /tmp/visual.html       # must be ≥ 1
grep -c '"@type":"Article"'    /tmp/visual.html       # must be ≥ 1
grep -c '"@type":"Person"'     /tmp/visual.html       # must be ≥ 1
grep -oc '—' /tmp/visual.html                          # must be 0
grep -oc '{index=' /tmp/visual.html                    # must be 0
```

If Cowork has browser visualization, open the URL and visually confirm: green hero, byline avatar+name, cards, table styled with green header, yellow note box, green pill buttons.

### §4.10 site-state log + commit

Append to `skills/site-state.md`:

```markdown
### 2026-MM-DD HH:MM - Cowork - Published spoke `[slug]` (id [N])
- Target query: [QUERY]
- Cluster: [PILLAR_SLUG] → spoke
- Word count: [N]
- Internal links: pillar ✓, siblings ✓ ([id, id]), tool ✓ ([slug]), lawyer CTA ✓
- Yoast title + metadesc + focuskw set ✓
- Author byline + Person/Article JSON-LD ✓
- Visual QA passed ✓ ([URL])
- Generation: ChatGPT Instant | Gemini | Claude Chat (mark which)
```

Then commit + push to `claude/charming-meitner-mwVEW`. Don't wait for next article; commit per article so a crash loses at most one.

---

## §5. Token discipline

- **ONE prompt at a time.** No parallel ChatGPT calls. Wait 30-60s between articles.
- The SYSTEM block (§4.3 header) gets pasted ONCE per chat session. Reuse the same chat for multiple articles when possible (cheaper for owner).
- Don't summarize the article back to the owner. He sees the live URL.
- Don't ask ChatGPT to "show me the word count" — verify with Python yourself (the model lies about counts).
- Don't regenerate if 80% right; patch with a targeted follow-up: "החלף את ה-h2 השלישי, השאר את שאר המאמר."

For Cowork's own token use:
- Reuse the Python publish template; don't rewrite it per article.
- Cache the `GREEN_CSS` once; don't re-read per article.
- Don't re-fetch the cluster map; load it once into a variable.

---

## §6. Engine failure protocol

ChatGPT returns blank twice in a row OR returns mixed-render output you can't extract cleanly twice in a row → **switch to Gemini** for that article. Don't fight ChatGPT. Don't waste owner's quota.

Gemini fails twice → **switch to Claude Chat** (paid subscription, reliable Hebrew, slightly verbose — trim 10-15% post-extraction).

All three fail → §11 stop with reason "all engines blocked on article #N".

---

## §7. Reference materials (load when needed)

| When you need to... | Read |
|---|---|
| Voice / forbidden phrases | `skills/copywriting-skill.md` |
| Cluster map / anti-cannibalization | `skills/internal-linking-hub-spoke.md` |
| Yoast meta + Person schema | `skills/yoast-config.md` |
| Design tokens / CSS contract | `skills/article-guide-design-pattern.md` |
| Strategy / competitor map | `skills/strategy-master.md` |
| Money model | `skills/payments-woo-greeninvoice.md` |
| Project history | `skills/cowork-briefing.md` |
| Current state | `skills/site-state.md` (last 6 blocks) |
| Reference live design | `https://nad-lan.co.il/design-demo-green/` |

---

## §8. Anti-cannibalization (re-verified for this batch)

The 24 backlog queries were checked against all 74 live pages. **No collisions.** Each target query in §1 maps to a distinct intent that no existing page targets. Cowork does not need to re-check cannibalization for the listed backlog — already validated. **But:** if owner adds an ad-hoc query mid-session, Cowork MUST run a slug-collision + intent-collision check before writing.

---

## §9. The reference page (open this if uncertain about design)

**https://nad-lan.co.il/design-demo-green/** — every component on one page (hero, eyebrow, cards, table, note, CTA, byline, disclaimer). The visual yardstick. If your output doesn't look as polished as this, something is missing.

In-the-wild exemplars (already shipping this design):
- https://nad-lan.co.il/real-estate-tax-advisor/capital-gains-tax-exemption/
- https://nad-lan.co.il/mortgage-calculator/reverse-mortgage/
- https://nad-lan.co.il/real-estate-lawyer/power-of-attorney-real-estate/

---

## §10. Failures the 2026-05-30 batch made (do NOT repeat)

| What broke | Why | Prevention in v2 |
|---|---|---|
| Page 493: 4 duplicate H2 sections | Cowork stitched ChatGPT's 2 truncated passes naively | §4.5 NEW: `h2 unique != h2 total` check |
| Page 519: opener "במאמר זה נפרט" | Gemini ignored the bare ban; v1 sanity-check exempted disclaimer too aggressively | §4.5 NEW: regex flags `במאמר זה` outside disclaimer |
| Page 493: redundant body byline | ChatGPT added "המאמר נכתב על ידי..." inside prose | §4.3 prompt rule 7; §4.5 grep check |
| 5 short-rent spokes 2026-05-29 | Escaped HTML + ChatGPT preamble + missing meta + orphan links | v1 §4.4 + §4.7 + §4.8 — STILL APPLIES |
| Parallel ChatGPT prompts → rate limit blank | Cowork sent 2 generations same minute | §3 STRICT rule: one prompt at a time |
| Word count short of strategy minimum | ChatGPT trimmed under Extended truncation | §4.6 hard floor 1,800; refuse to publish under |

---

## §11. Stop conditions (the ONLY reasons to halt)

Halt the session and report to owner ONLY when:

1. REST returns 401/403/404 for `users/me` (auth lost — owner needs to re-login)
2. REST 5xx repeated for 5+ minutes (server actually down)
3. All three writing engines (ChatGPT, Gemini, Claude Chat) returned blank/blocked on the same article in the same session
4. A page revision shows accidental wipe — restore from revision BEFORE continuing
5. A NEW skill or rule contradicting this runbook surfaced from the owner mid-session
6. The full 24-article backlog completed → write §12 final report and END

**Do NOT halt for:**
- An article needing a retry (use the §6 engine fallback)
- An article needing a re-prompt (just send it back)
- A single failed sanity-check (fix and continue)
- Owner being away (proceed; he pre-approved the full backlog)
- Owner asking mid-stream "how's it going?" — answer in one line and keep going

---

## §12. Final report template (write when backlog is done)

Append to `skills/site-state.md` and copy to chat:

```markdown
## Batch v2 final report - 2026-MM-DD

**Backlog progress:** [done] of 24 articles published.

**Articles published this session (link list):**
[list each: id, slug, target query, generation engine]

**Engine usage stats:**
- ChatGPT Instant: [count]
- Gemini: [count]
- Claude Chat: [count]

**Average word count per article:** [N] (target 1,800-2,500)

**Sanity-check rescue count:** [N retries triggered before publish]

**Honesty - what went wrong:**
- [each defect found pre-publish]
- [each engine block]
- [any owner-action item]

**Score (brutal):**
- Google Blueprint compliance: [N]/10
- Design adherence: [N]/10
- E-E-A-T (byline, schema, sources): [N]/10
- Internal-link wiring: [N]/10
- Anti-cannibalization: [N]/10
- Hebrew prose quality: [N]/10
- Word count adherence: [N]/10

**Next-batch recommendation:** [from strategy §2.4 cities, §4.7 price-guides, or developer-driven]
```

---

## §13. What "done" looks like

When you finish all 24, the site will have:

- **9 articles** in tax-legal cluster (vs the 4 we had) — completes the highest-value E-E-A-T moat
- **5 articles** in urban-renewal cluster (vs the 1 we had) — unlocks the lawyer's revenue sweet spot
- **8 articles** in lawyer cluster (vs the 3 we had)
- **4 articles** in selling cluster (vs the 0 we had)
- **5 articles** in mortgage cluster (already done in v1)
- **7 articles** in investment cluster (vs the 3 we had)
- **3 articles** in commercial cluster (vs the 1 we had)
- **3 articles** in buying cluster (vs the 1 weak we had)

Total content pages: **~87** (from current 63). That's complete coverage of strategy §2 Priority 1+2 keyword clusters. After this batch, the absent-spoke list per `strategy-master.md` goes to ZERO for P1+P2.

---

## §14. The one rule above all rules

**The owner is away. You are autonomous. Run the loop. Publish article 1, then article 2, then article 3, all the way to article 24. Commit per article. Stop only on §11. Report only on §12.**

You have the runbook. You have the backlog. You have the engines. Go.

---
_Created 2026-05-30 by Claude Code (claude-opus-4-7). v2 supersedes v1. v2 incorporates the 2026-05-30 9-article-batch lessons + the explicit 24-article backlog from strategy-master §2._
