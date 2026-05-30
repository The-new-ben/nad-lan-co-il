# Cowork Runbook — Article Batch Execution (master recipe)

> **For Claude Cowork (and any agent the owner points at a batch):** this is the **single self-contained recipe** for producing a batch of high-ranking Hebrew articles on nad-lan.co.il, from cold session start to the owner's end-of-batch report. Read it once at the top of the session, then execute the loop section-by-section without stopping. The owner is walking away after he runs this; do not stop to ask permission on routine steps. **Stop only on:** broken REST connectivity, owner-facts you cannot infer (covered in §0), or a destructive-action gate.

> **Voice:** ChatGPT does the Hebrew heavy lifting (saves tokens). You do orchestration, publishing, QA, schema, links, design, navigation. **Never** write a long Hebrew article yourself — that burns the owner's tokens.

> **Last update:** 2026-05-30, after the 2026-05-29 Cowork-batch audit (6 of 7 spokes shipped broken) and the 2026-05-30 retro-wire sweep. The mistakes are named in §11.

---

## §0. Owner-supplied facts (cached here so you don't re-ask)

Cached for the next agent to use without lookup. Verify against `HANDOFF.md` and `site-state.md` on session start; trust this list otherwise.

```yaml
owner:
  name_hebrew:  "בן בטש"
  title:        "עו\"ד"
  bar_number:   29020
  bar_url:      "https://www.israelbar.biz/lawyer-fd/?lawyer=Cqcs/1T4N0I"
  other_site:   "https://jus-tice.co.il/"
  email_site:   "info@nad-lan.co.il"
  email_personal: "benbetesh@gmail.com"
  phone_cell:   "0525101555"
  phone_work:   "036916454"
  address:      "וולנברג ראול 18, תל אביב יפו"
  wp_admin_user_id: 1
  wp_admin_user_slug: "ben-betesh" (target; may currently be "nadlvzld_admin")

design:
  palette:       "green canonical (Codex)"  # owner 2026-05-30
  pattern_skill: "skills/article-guide-design-pattern.md"
  reference_pages_live:
    - "https://nad-lan.co.il/design-demo-green/"   # bare demo
    - "https://nad-lan.co.il/real-estate-lawyer/"   # in-the-wild exemplar
    - "https://nad-lan.co.il/investment/"           # 2026-05-30 retro-wired

monetization:
  pricing_page: "https://nad-lan.co.il/join-pro/"
  products:
    - {id: 475, name: "רישום בסיסי",         price: "0",     status: publish}
    - {id: 476, name: "Pro (חודש ראשון חינם)", price: "349",   status: publish}
    - {id: 477, name: "Premier",              price: "749",   status: publish}
    - {id: 489, name: "קמפיין פרויקט יזם",     price: "3990",  status: publish}
    - {id: 490, name: "מודעה מקודמת נכס",      price: "299",   status: publish}
  payment_gateway: "Green Invoice (Morning) - credit card, Bit, Google Pay, Apple Pay"
  registration:    "open (woocommerce_enable_myaccount_registration=yes)"

cta_targets:
  primary:   "/real-estate-lawyer/"
  calculator_purchase_tax: "/purchase-tax-calculator/"
  calculator_mortgage:     "/mortgage-calculator/"
  pricing:   "/join-pro/"
```

---

## §1. Pre-flight (do this once per session, takes 60 seconds)

```bash
# REST + auth + plugin alive
curl -s "$WP_BASE_URL/wp-json/nadlan/v1/healthcheck"
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/users/me?_fields=id,name,roles"

# Git on the working branch
git remote -v ; git branch --show-current
# Expect: claude/charming-meitner-mwVEW

# Last 6 site-state blocks (the situation report)
tail -180 skills/site-state.md
```

If healthcheck returns JSON with `plugin: nadlan-config` and `users/me` returns `roles: [administrator]`, you are connected. If either fails, **STOP** and tell the owner.

---

## §2. Pre-batch website check (mandatory — Cowork was skipping this)

Before adding a single new page, **open the live site in your head and scan critically**:

```bash
# 1. Index of all live pages (most recent first)
curl -s -u "$WP_USER:$WP_APP_PASSWORD" \
  "$WP_BASE_URL/wp-json/wp/v2/pages?per_page=50&orderby=modified&order=desc&_fields=id,slug,title,modified" \
  | python3 -c "import json,sys;[print(p['id'],p['modified'][:10],p['slug']) for p in json.load(sys.stdin)]"

# 2. Navigation menu items
curl -s -u "$WP_USER:$WP_APP_PASSWORD" "$WP_BASE_URL/wp-json/wp/v2/navigation" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d[0]['content']['raw'][:3000]) if d else print('no nav')"

# 3. Pillar map (skills/internal-linking-hub-spoke.md cluster map)
grep -A1 "Pillar slug" skills/internal-linking-hub-spoke.md | head -40
```

Then check **each pillar's last spoke** visually with a curl-fetched cache-busted GET, scanning for:
- Em-dashes `—` (must be 0)
- `{index=` ChatGPT citation markers (must be 0)
- `[N]` numbered citations (must be 0)
- `word+N` Perplexity citations (must be 0)
- `להלן` / `הנה המאמר` ChatGPT preamble (must be 0)
- Bare `<h2>` without `.nadlan-guide` wrapper (must be 0)
- Forbidden phrases from `copywriting-skill.md` §3-4

Anything found → fix BEFORE adding new content. Update `site-state.md` with what you found.

---

## §3. Choose the next batch — anti-cannibalization

The owner usually says "next batch" without specifying. Pick from the strategy by priority. **Never** write a query that already has a live page (cannibalization). The map of "what we already cover":

| Cluster | Pillar | Spokes already live |
|---|---|---|
| קניית דירה | `/buying-apartment/` | 11 spokes (apartment-buying-checklist, tabu, property-value, home-inspection, broker, appraiser, new-projects, purchase-tax, mortgage, cost-calc, lawyer) |
| מכירת דירה | `/selling-apartment/` | 5 spokes |
| דירה להשקעה (כללי) | `/investment-apartment/` | 7 spokes (mortgage, cashflow, mgmt, commercial, tax, new-projects, lawyer) |
| נדל"ן להשקעה (איפה ואיך) | `/investment/` ← NEW 421 | 3 spokes (`real-estate-yield`, `apartments-for-investment`, `bank-guarantee-purchase`) |
| השכרה לטווח קצר בחו"ל | `/short-term-rentals-abroad/` ← 345 | 7 spokes (greece/portugal/thailand/dubai/cyprus/spain/italy) |
| משכנתא | `/mortgage-calculator/` | 4 spokes |
| מיסוי מקרקעין | `/real-estate-tax-advisor/` | 4 spokes |
| עורך דין מקרקעין | `/real-estate-lawyer/` | 5 spokes |
| התחדשות עירונית | `/urban-renewal/` | 4 spokes |
| נדל"ן מסחרי | `/commercial-real-estate/` | 4 spokes |
| דירה מקבלן | `/new-projects/` | 5 spokes |
| אנשי מקצוע | `/professionals/` | 10 spokes |

**Recommended next batches (priority order, from `strategy-master.md` §2):**

1. **Tax-legal cluster expansion** — owner is a lawyer; SERP belongs to law firms; biggest E-E-A-T moat. New spokes: `מס שבח דירה יחידה`, `פטור ממס שבח 2026`, `היטל השבחה`, `ערבות חוק מכר` (already at id 424 — extend cluster), `חוזה מכר דירה`, `ליווי בנקאי לפרויקט`.
2. **Mortgage cluster deepening** — 40,500/mo on "מחשבון משכנתא", banks dominate, we can take spokes. New: `משכנתא הפוכה`, `מחזור משכנתא 2026`, `יחס מימון משכנתא`, `ביטוח משכנתא`, `משכנתא לדירה שנייה`.
3. **City pages** — `דירות למכירה בתל אביב/ירושלים/חיפה/באר שבע/ראשון/פתח תקווה` — pillar + neighborhood spokes. Lower priority because Yad2+Madlan block top SERP, but builds the long tail.
4. **Urban renewal expansion** — `תמא 38/2 הריסה ובנייה`, `פינוי בינוי זכויות דייר`, `חוזה תמא 38 - מה לבדוק`, `איך לבחור יזם להתחדשות עירונית`.
5. **Investment cluster deepening** (built on the new `/investment/` pillar): `תזרים מזומנים דירה להשקעה`, `מינוף בנדלן`, `דירה להשקעה דרך חברה`, `קרן REIT ישראלית`.

**Confirm the batch with the owner ONCE at session start**, then proceed without stopping. If owner doesn't reply within 5 minutes, default to the recommended top batch (#1 tax-legal).

---

## §4. Per-article workflow — the loop

For each article in the batch, execute §4.1 through §4.10. **No skipping.** No stopping between articles. Update `site-state.md` after every article so a crash doesn't lose context.

### §4.1 Choose target query

One Hebrew search query a real user would type. Write the query, the intent (one sentence), and the cluster (which pillar it belongs to) at the top of a scratch note.

### §4.2 Google Blueprint (manual SERP research)

Per `strategy-master.md` §13. Cowork has browser tools — **use them**. Open https://www.google.co.il in incognito (Hebrew, IL location), search the exact query, record:

- Top 10 organic results (URL + title + meta description)
- All "אנשים גם שואלים" questions (expand each)
- All "חיפושים קשורים"
- Featured snippet if present
- Ads (commercial intent signal)

For each top-10 result classify: type (blog/law-firm/bank/news/forum/gov/aggregator), approximate word count, format (long guide/Q&A/list/calculator/case study), h2 sub-topics, missing angles.

**Output of §4.2** — saved in a scratch note for §4.4:
- Intent (1 sentence)
- Shared backbone (h2s 7+ of 10 cover — MANDATORY)
- Differentiators from top-3 (1-2 unique angles we steal/improve)
- Gaps (PAA questions NONE of the top 10 answered well — our edge)
- Outline (H1 + h2s + Q&A block at bottom)

If you cannot do manual Google search in this session, **tell the owner** rather than guessing. Guessed intent → wrong article → no rank.

### §4.3 Numbers + sources

Every claim of a number needs a primary source with date. Allowed sources for nad-lan.co.il:

| Topic | Allowed sources |
|---|---|
| ישראל (כללי) | נדלן.gov.il, cbs.gov.il (לשכה מרכזית לסטטיסטיקה), boi.org.il (בנק ישראל), gov.il, פסיקה, חוקים מרכזת |
| ישראל (מסים) | רשות המסים (שערים, מדרגות, פטורים) |
| חו"ל | המשרד הסטטיסטי הלאומי של כל מדינה, הבנק המרכזי שלה, רשות המסים שלה, משרד התיירות שלה |
| EU | Eurostat |
| **אסור** | אתרי מתחרים (Madlan, Yad2, נדלן מאסטר, בלוגי מתווכים), Wikipedia, סיכומי ChatGPT, "דוחות תעשייה" של חברות מכירות |

Every number gets `(מקור: X, תאריך)` inline. Numbers without sourceable evidence get cut, even if probably true.

### §4.4 The master ChatGPT prompt (paste this into ChatGPT)

The owner runs ChatGPT manually (or you instruct him to). The prompt below is the master template — fill in the bracketed parts for the specific article.

```
אתה עורך תוכן בכיר באתר נדל"ן ישראלי פרמיום (nad-lan.co.il) שמתמחה בייעוץ מקצועי לקונים, מוכרים ומשקיעים. הטון: רגוע, סמכותי, עובדתי, ענייני. אתה לא מוכר - אתה מסביר. הקוראים הם ישראלים שמחפשים תשובה אמינה לפני החלטה כלכלית-משפטית גדולה.

כותב המאמר הנקרא: עו"ד בן בטש (חבר לשכת עורכי הדין בישראל, רישיון 29020).

הקוואריה היעד (Google Blueprint): "[QUERY]"
הכוונה (intent): "[ONE-SENTENCE INTENT]"
הקלאסטר: [PILLAR SLUG]
פילר אב: [PILLAR URL]
ספוקים אחיים שאסור לחזור על התוכן שלהם: [SIBLING URLS + topics]

מבנה חובה (h2 לכל סעיף, על פי הסדר):
1. [SHARED BACKBONE TOPIC 1 from Blueprint §4.2]
2. [SHARED BACKBONE TOPIC 2]
3. [DIFFERENTIATOR TOPIC from top-3]
4. [GAP TOPIC nobody covers well]
... (אורך 1,800-2,500 מילים לספוק; 2,500-4,000 לפילר)
n-1. נקודות מפתח לפני חתימה / לפני החלטה (סעיף סיכום, ב-h2)
n. שאלות נפוצות (h2). מתחתיו 5-8 שאלות מ"אנשים גם שואלים" עם תשובה של 80-150 מילים לכל אחת.

כללי כתיבה - חובה לעמוד בכולם:
1. עברית מדויקת, לא תרגום מאנגלית.
2. ללא em-dash (—). השתמש ב-",", ב-" - " (מקף רגיל עם רווחים), או ב-":".
3. אסור לכלול את הביטויים: "חשוב להבין", "ראוי לציין", "במילים אחרות", "בעידן הנוכחי", "בעידן הדיגיטלי", "עולם הנדל"ן", "אכן", "בהחלט", "ללא ספק", "בעולם שבו", "אינסוף", "באופן כללי", "בסופו של דבר", "לסיכום", "כפי שראינו", "במאמר זה", "מצד אחד...מצד שני" כפסקה.
4. אסור לכלול את המילים הפנימיות: ליד, leads, CRM, פילר, spoke, hub, cluster, intent, money page, UTM, KD, SEO.
5. כל מספר עם מקור ותאריך: "(מקור: בנק ישראל, מרץ 2026)". אם לא בטוח - כתוב "טעון אימות".
6. מספרים גדולים עם פסיקים: "1,978,745 ₪". אחוזים בלי רווח: "8%". טווחים עם en-dash קצר: "1,978,745–2,347,040 ₪".

פלט - חובה לעמוד בכל הסעיפים, אחרת הפלט ייפסל אוטומטית:

א. HTML גולמי בלבד, מוכן להדבקה.
ב. רק תגי <h2>, <h3>, <p>, <ul>, <li>, <strong>, <table>, <thead>, <tbody>, <tr>, <th>, <td>. אסור <h1> (WordPress מוסיף מהכותרת). אסור <html>, <head>, <body>. אסור markdown. אסור <style>. אסור <script>.
ג. שמור על dir="rtl" בכל בלוק חוסם (כל <p>, <h2>, <h3>, <ul>, <table>).
ד. בנוסף לתגי הטקסט - בנה את המבנה הבא בעזרת div עם class:
   - פסקת פתיחה ראשונה ושנייה עטופות בלי class מיוחד (יוצב בתוך .hero ע"י המפרסם).
   - כל סעיף מבני (לאחר h2 חדש), אם יש בו 3 אופציות / 3 קטגוריות / 3 בחירות - בנה גריד של 3 כרטיסים:
       <div class="cards">
         <div class="card"><b>כותרת קצרה</b><p>הסבר 2-3 שורות.</p></div>
         <div class="card"><b>כותרת קצרה</b><p>הסבר 2-3 שורות.</p></div>
         <div class="card"><b>כותרת קצרה</b><p>הסבר 2-3 שורות.</p></div>
       </div>
   - אם יש השוואה (מסים, תשואות, ערים, מסלולים) - השתמש ב-<table> עם <thead> ו-<tbody>.
   - בכל סעיף ראשי, אחרי הפיסקאות והכרטיסים/טבלה, הוסף בלוק נקודת-מפתח אחת:
       <div class="note">נקודה קריטית של הסעיף, משפט אחד או שניים בלבד.</div>
   - אחרי כל 2-3 סעיפי h2, הוסף קריאה לפעולה:
       <div class="cta"><a class="btn" href="/real-estate-lawyer/">קבעו ייעוץ עם עו"ד בן בטש</a></div>
ה. אל תפתח את הפלט בביטויים כמו "להלן המאמר", "הנה המאמר", "להלן HTML נקי להדבקה", או כל הערת שקיפות. הפלט מתחיל ישירות בפסקת הפתיחה (לפני h2 הראשון של הגוף).
ו. אסור לכלול footnotes של מקורות בפורמט "Source+9", "[1]", "{index=0}", "AADE+1", או כל סימן ציטוט מספרי. אם אתה מצטט מקור, שלב אותו פנימית בעברית בתוך הפסקה: "(מקור: בנק ישראל, מרץ 2026)".
ז. בדיקה עצמית לפני שאתה משיב: אין em-dash, אין footnotes, אין preamble, אין forbidden phrases, יש h2/h3, יש לפחות div.cards אחד, יש לפחות table אחד, יש לפחות div.note אחד, יש לפחות div.cta אחד, האורך 1,800-2,500 מילים (ספוק) או 2,500-4,000 (פילר). אם משהו חסר - בנה את החסר ושלח רק את התקין.
```

### §4.5 Sanity-check ChatGPT output (before publishing)

Save the output to `/tmp/article.html`. Run these checks. Any fail → send back to ChatGPT with the specific gap, **do not patch in place**.

```bash
F=/tmp/article.html
echo "em-dash: $(grep -c '—' $F)              (must be 0)"
echo "{index=: $(grep -c '{index=' $F)          (must be 0)"
echo "[N] cite: $(grep -oP '\[\d+\]' $F | wc -l) (must be 0)"
echo "word+N:  $(grep -oP '[A-Za-z]+\+\d+' $F | wc -l) (must be 0)"
echo "preamble: $(grep -cE 'להלן|הנה המאמר|הערת שקיפות' $F) (must be 0)"
echo "h2: $(grep -oc '<h2' $F) (must be > 4)"
echo "cards: $(grep -c 'class=\"cards\"' $F) (must be > 0)"
echo "table: $(grep -oc '<table' $F) (must be > 0)"
echo "note: $(grep -c 'class=\"note\"' $F) (must be > 0)"
echo "cta: $(grep -c 'class=\"cta\"' $F) (must be > 1)"
echo "word count (Hebrew, rough): $(wc -w < $F)"
for p in "חשוב להבין" "ראוי לציין" "במילים אחרות" "עולם הנדל" "בעידן" "ללא ספק" "אינסוף" "באופן כללי" "בסופו של דבר" "לסיכום" "כפי שראינו"; do
  c=$(grep -c "$p" $F); [ "$c" != "0" ] && echo "FORBIDDEN: $p ($c)"
done
# "במאמר זה" is allowed ONLY inside the legal disclaimer ("אין לראות במאמר זה ייעוץ משפטי").
# Flag it only when it appears OUTSIDE that exact disclaimer phrase (an AI-tell opener like "במאמר זה נסקור").
bad=$(grep -o 'במאמר זה[^י]' $F | grep -v 'במאמר זה י' | wc -l)
[ "$bad" != "0" ] && echo "FORBIDDEN (opener): במאמר זה ($bad) — disclaimer use is OK, opener use is not"
for w in "ליד" "leads" "CRM" "פילר" "intent" "SEO"; do
  c=$(grep -c "$w" $F); [ "$c" != "0" ] && echo "INTERNAL LEAK (check context): $w ($c)"
done
```

Run all of the above. If any of "must be 0" fails or "must be > 0/1/4" fails — **send back to ChatGPT** with the failing checks listed, ask it to fix and resend.

### §4.6 Build the page (Python sweep, idempotent)

Use this script template (already proven on the 2026-05-30 retro-wire):

```python
import os, requests, json
USER=os.environ['WP_USER']; PWD=os.environ['WP_APP_PASSWORD']; BASE=os.environ['WP_BASE_URL'].rstrip('/')
A=(USER,PWD)

INNER = open('/tmp/article.html').read()  # ChatGPT's cleaned output

SLUG = "..."     # decided in §4.1, slug-form: short, dashed, English where standard
TITLE = "..."   # H1 / page title, full Hebrew with year if relevant
PARENT_ID = ... # pillar page ID (0 for pillar itself)
FOCUS_KW = "..."  # the target query verbatim
METADESC = "..."  # 150-160 chars, factual + what reader gets + soft CTA

GREEN_CSS = open('skills-templates/article-guide.css').read()  # or inline from article-guide-design-pattern.md

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
    {"@type":"Article","headline":TITLE,"url":f"https://nad-lan.co.il/{SLUG}/",
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
    '_yoast_wpseo_is_cornerstone': '',  # '1' only for pillars
  }
}

r = requests.post(f'{BASE}/wp-json/wp/v2/pages', auth=A, json=payload, timeout=60)
print('created:', r.status_code, r.json().get('link'))
```

### §4.7 Wire internal links

Follow `internal-linking-hub-spoke.md`. Every spoke gets 3 directions:

1. **Up to its pillar** — anchor in the first 200 words of the article body. Anchor text uses the pillar's H1.
2. **Across to 2-4 sibling spokes** — anchor in body text, not as a "related articles" list. Anchor text uses each sibling's target query.
3. **Down to 1-2 tools** — `/purchase-tax-calculator/`, `/mortgage-calculator/`, `/buy-vs-rent/`, etc.

Then update the pillar to link to the new spoke (per the cluster map's `<!-- nadlan-hub-related-v1 -->` marker).

Anti-cannibalization: never link to a spoke targeting the same query. Different queries within the same cluster only.

### §4.8 Navigation

For a new pillar (rare): add to main nav. For a spoke (common): do NOT add to main nav. Spokes live via pillar links + sitemap. The sitemap page (`/sitemap/`, id 336) auto-includes everything; no action needed.

### §4.9 Visual QA on the live page

**Mandatory before declaring the article done.** Open the live URL with cache-bust, save to /tmp, grep for:

```bash
URL="$WP_BASE_URL/[slug]/"
curl -sL "$URL?nc=$(date +%s)" -o /tmp/visual.html
echo "size: $(wc -c </tmp/visual.html)"
grep -c 'class="nadlan-guide"' /tmp/visual.html  # must be 1+
grep -c 'class="byline"'      /tmp/visual.html  # must be 1+
grep -c 'מאת בן בטש'           /tmp/visual.html  # must be 1+
grep -c 'class="disclaimer"'  /tmp/visual.html  # must be 1+
grep -c '@type":"Article"'    /tmp/visual.html  # must be 1+ (in JSON-LD)
grep -c '@type":"Person"'     /tmp/visual.html  # must be 1+
grep -oc '—' /tmp/visual.html                    # must be 0
grep -oc '{index=' /tmp/visual.html              # must be 0
```

If Cowork has browser tools, ALSO open the URL in a real browser and look at:
- Hero renders with eyebrow + h2 + lede + CTA
- Cards row exists somewhere
- At least one table styled with green header
- At least one yellow note box
- Buttons are green pills
- No raw HTML tags visible as text
- Byline shows initials avatar + name + license

### §4.10 Update site-state.md

Append after every article (not after every batch — every article):

```markdown
### 2026-MM-DD - Cowork - Published spoke `[slug]` (id [N])
- Target query: [QUERY]
- Intent: [ONE LINE]
- Cluster: [PILLAR_SLUG] → spoke
- Word count: [N]
- Internal links: pillar ✓, siblings ✓ (which), tool ✓ (which), lawyer CTA ✓
- Yoast title + metadesc + focuskw set ✓
- Author byline + Person/Article JSON-LD ✓
- Visual QA passed ✓ ([URL])
- Known gaps: [if any]
```

---

## §5. End-of-batch report (the honesty statement)

After all articles in the batch are done, write the report. **Honest. Critical. No flattery.** The owner explicitly asks for this.

```markdown
## Batch [N] report - [DATE]

**Articles published:** [count]
[list each: id, slug, target query, URL]

**What went well:** [bullet list, factual]

**What went wrong (must be honest):**
- [any artifact found in QA that was caught + fixed]
- [any forbidden phrase that slipped through ChatGPT]
- [any design break]
- [any failed PUT, broken link, missing field]

**Open items for owner:**
- [decisions you cannot make]
- [pages that need owner-only action (menu edit, plugin upload)]

**Score (be brutal):**
- Google Blueprint compliance: [N]/10
- Design adherence: [N]/10
- E-E-A-T (byline, schema, sources): [N]/10
- Internal-link wiring: [N]/10
- Anti-cannibalization: [N]/10

**Recommended next batch:** [topic / cluster]
```

Append to `skills/site-state.md` and copy to chat for the owner.

---

## §6. ChatGPT token-saving rules

Every ChatGPT call costs the owner money. To minimize:

1. **One paste of the SYSTEM block per ChatGPT session** (not per article).
2. **One paste of `§0` owner-facts block per session** (not per article).
3. The PER-ARTICLE prompt is just the bracketed parts of `§4.4` (query, intent, cluster, pillar URL, siblings, outline). ~300 tokens.
4. **Do not regenerate** if the article is 80% right. Patch with a targeted ChatGPT follow-up like "החלף את ה-h2 השלישי, השאר את שאר המאמר".
5. **Do not summarize** the article back to the owner. He sees the live URL.

For YOUR own (Cowork's) token use:
1. **Do not write Hebrew prose yourself.** Pass it to ChatGPT.
2. **Re-use the Python sweep template** (§4.6) - don't rewrite it per article.
3. **Don't read pages you already have in scratch.** Cache locally.

---

## §7. Reference materials (skills to load when needed)

| When you need to... | Read |
|---|---|
| Voice / forbidden phrases / em-dash ban | `skills/copywriting-skill.md` |
| Cluster map / anti-cannibalization | `skills/internal-linking-hub-spoke.md` |
| Yoast meta + cornerstone marking | `skills/yoast-config.md` |
| Plugin behavior / healthcheck | `skills/nadlan-config-plugin.md` |
| Design tokens / CSS contract | `skills/article-guide-design-pattern.md` |
| Strategy / competitor map | `skills/strategy-master.md` |
| Money model | `skills/monetization-lawyer-angle.md` + `skills/payments-woo-greeninvoice.md` (note: rename in progress) |
| Project history | `skills/cowork-briefing.md` |
| Cross-agent contract | `AGENTS.md` |
| Current state | `skills/site-state.md` (read last 6 blocks) |

---

## §8. Reference page for "what good looks like"

Open: **https://nad-lan.co.il/design-demo-green/** — a single page with every component (hero, cards, table, note, CTA). Use it as the visual yardstick. If your page doesn't look as polished as this demo, something is missing.

In-the-wild examples:
- https://nad-lan.co.il/real-estate-lawyer/ — Codex-era pillar (original green pattern source)
- https://nad-lan.co.il/investment/ — 2026-05-30 retro-wired (green pattern applied to existing prose)
- https://nad-lan.co.il/short-term-rentals-abroad/short-term-rentals-thailand/ — same, spoke level

---

## §9. Master example prompt — fully worked, for reference

For target query **`פטור ממס שבח דירה יחידה 2026`**, after Blueprint research:

```
[SYSTEM block from §4.4]

הקוואריה: "פטור ממס שבח דירה יחידה 2026"
הכוונה: מוכר דירה (יחידה או נוספת) שרוצה לדעת אם מגיע לו פטור, איך לבדוק, ואיך לתכנן מס לפני המכירה.
הקלאסטר: real-estate-tax-advisor
פילר אב: https://nad-lan.co.il/real-estate-tax-advisor/
ספוקים אחים שאסור לחזור על התוכן שלהם:
  - https://nad-lan.co.il/purchase-tax-calculator/ (מס רכישה, לא שבח)
  - https://nad-lan.co.il/apartment-purchase-cost-calculator/ (עלויות רכישה)
  - https://nad-lan.co.il/real-estate-lawyer/ (שירות, לא תוכן מס שבח)

מבנה חובה (h2 בסדר הזה):
1. מהו מס שבח ולמי הוא נוגע
2. תנאי הפטור לדירה יחידה - הקריטריונים המעודכנים ל-2026
3. מתי הפטור נשלל - דוגמאות מציאותיות
4. דוגמת חישוב - דירה יחידה שנמכרה ב-2026
5. הבדל בין פטור לדירה יחידה לבין פטור פעם ב-4 שנים
6. מה לבדוק לפני חתימת חוזה מכר
7. שאלות נפוצות (h2). 7 שאלות מ-PAA, 100-150 מילים תשובה.

[הנחיות הפלט החובה מ-§4.4ה-ז]

אורך: 1,800-2,200 מילים. כל מספר עם מקור (רשות המסים, חוק מיסוי מקרקעין סעיף 49ב, פסיקה).
```

The owner pastes this prompt, ChatGPT returns the inner HTML, Cowork runs §4.5 sanity-check, then §4.6 publish, §4.7 link wire, §4.9 visual QA, §4.10 state update. Loop to next article.

---

## §10. Failures the 2026-05-29 batch made (do not repeat)

Each line is a real failure, the detection that would have caught it, and the prevention in this runbook.

| Failure | Detected by | Prevented in runbook by |
|---|---|---|
| 6 of 7 spokes shipped with `&lt;h2&gt;` visible as literal text | §4.5: `grep '&lt;'` | §4.4 output rule א + ב; §4.5 sanity check |
| All 7 spokes had only 1 internal link (to pillar) | §4.9: link count < 3 | §4.7 anti-cannibalization wiring |
| 4 of 7 missing Yoast metadesc | §4.6: `meta` field missing | §4.6 payload includes `meta` |
| Multiple spokes opened with "להלן מאמר HTML נקי להדבקה" | §4.5: grep `להלן`/`הנה המאמר` | §4.4 output rule ה |
| Citation footnotes `AADE+1`, `{index=0}` left in body | §4.5: grep + regex | §4.4 output rule ו |
| No author byline despite tax/regulation content | §4.9: grep `מאת בן בטש` | §4.6 template includes BYLINE |
| No CTA / lawyer link / monetization path | §4.9: grep `class="cta"` | §4.6 template includes LAWYER_CTA |
| Bare `<h2>`/`<p>` without `.nadlan-guide` | §4.9: grep wrapper | §4.6 template wraps in `.nadlan-guide` |

---

## §11. Stop conditions (when to actually stop and ping the owner)

- REST 401/403 (auth broken)
- REST 5xx repeated (server down)
- The 11 wiring failures above could not be cleaned in 2 ChatGPT iterations
- A page revision history shows previous content was wiped accidentally — pause, restore from revisions BEFORE continuing
- Owner-fact missing (e.g., the SYSTEM author block needs a new author for a non-lawyer topic)
- You found a CRITICAL flaw in the existing site (broken homepage, expired payment, missing legal disclaimer) — fix that first

For everything else, **keep going**. The owner is away.

---

## §12. Where to put intermediate work

- Scratch notes: `/tmp/` (NOT in the repo; gone after session)
- Python sweep scripts: `/tmp/` (kept in `site-state.md` if reusable)
- New skills: `skills/` (committed and pushed)
- Updates to `site-state.md`: committed after every batch

Push to `claude/charming-meitner-mwVEW`. Commit messages: one line summary + 3-line body. Don't mention the model identifier in commits.

---

_Created 2026-05-30 by Claude Code (claude-opus-4-7), the boss-agent owner's request: "make a full runbook for Claude CoWork ... batch after batch ... save tokens ... embed all the skills". This file IS the recipe. Cowork: read once, execute the loop._
