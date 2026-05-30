# Google Blueprint Workflow — reverse-engineer the SERP before writing

> **For Cowork (and any agent producing SEO content):** Cowork forgets this between sessions because it has no persistent memory. **This file is your memory.** Read it on session start and re-read it before every article.

> **Cross-references (single source of truth — do not duplicate here):**
> - Voice rules + forbidden phrases → `copywriting-skill.md`
> - Internal-link wiring after publish → `internal-linking-hub-spoke.md`
> - Yoast meta + Person schema → `yoast-config.md`
> - Competitor DNA + keyword clusters → `strategy-master.md`
> - **What to do AFTER ChatGPT returns the article → `article-publishing-protocol.md`** (the next file in the loop)

The workflow exists because we are a new domain with few backlinks. We cannot beat established competitors (Madlan, Yad2, the big law firms, the banks) on authority. We can only beat them on **content fit to the search intent**. Google ranks the page that answers the search best. The Blueprint is how we figure out what "best" means for a specific query — by looking at what Google itself already chose to rank.

## When to use this

Before writing any article that targets a query a human would type into Google. **Skip the Blueprint only for**: internal-process pages, legal-disclosure pages, transactional pages (calculator, lead form), and direct-traffic landing pages.

## The 7 steps — do not skip any

### 1. Choose the query (one query per article)

Pick the exact Hebrew search a real user would type. Examples:
- ✅ "השקעת נדל״ן בפורטוגל" (real query)
- ✅ "השכרה לטווח קצר קפריסין" (real query)
- ❌ "פורטוגל" (too broad)
- ❌ "נדל״ן בחו״ל לישראלים השקעה Airbnb" (keyword stuffing, no human types that)

The query must match how a buyer/investor/owner actually phrases it. Use natural Hebrew word order.

### 2. Manual Google search in Hebrew, from Israel

Open Google in an incognito window (so your history does not bias results). Search the exact query. Record:

- **Top 10 organic results** (URL + title + meta description shown in SERP)
- **"אנשים גם שואלים"** (People Also Ask) — every question listed; expand them, collect the sub-questions too
- **"חיפושים קשורים"** (Related searches) at the bottom — every suggested follow-up query
- **Featured snippet** if present — copy the snippet text, note the source URL
- **Knowledge panel / map pack** if present — note presence
- **Ads at top** (if any) — note whether the query is commercial enough to attract ads

For each top-10 organic result, briefly classify:
- Type: blog / law firm / bank / news / forum / government / aggregator
- Approximate word count (open the page, scan)
- What format: long-form guide / Q&A / list / calculator landing / case study
- What sub-topics it covers (their h2s)
- What angles it misses

This entire step is 30-60 minutes per article. **Do not shortcut it.** ChatGPT cannot do this for you — Google blocks LLM scraping and the results would be stale and US-biased anyway.

### 3. Derive the intent

After looking at the top 10, ask one question: **what is Google's model of this searcher**?

Examples of intent reads:
- "השקעת נדל״ן בפורטוגל" → Google is showing a mix of regulation explainers, tax breakdowns, and yield estimates. Intent = "I am considering buying property in Portugal; I need to know if it is legal/safe/worthwhile, with numbers." Not transactional. Not just informational. **Evaluation-stage**.
- "מס רכישה דירה ראשונה" → Google is showing tax-authority pages, calculators, and brief explainers. Intent = "I want to know how much I will pay." Transactional-adjacent. **Calculator + short clear explainer wins**.
- "עורך דין מקרקעין" → Google is showing law-firm landing pages and directory listings. Intent = "I am looking for a lawyer to hire now." Commercial. **Local-pack + trust signals + clear pricing/process wins**.

Write the intent in one sentence at the top of your article spec. Every section must serve that intent.

### 4. Pattern-match the SERP

From the top 10, identify:

- **The shared backbone** — sub-topics that 7+ of the 10 pages cover. These are mandatory in our article; missing them tells Google we did not answer the query.
- **The differentiators** — unique angles the #1-3 results have that the others lack. These are what we steal/improve.
- **The gaps** — questions in "People Also Ask" that NONE of the top 10 answer well. These are our edge. Write those sections at length.

Output a working outline:
- H1 (matches query intent, not the query verbatim)
- Mandatory sections (the shared backbone)
- Differentiator sections (the steals)
- Gap sections (the edge — usually the most valuable to Google because nobody else has them)
- Q&A block at the bottom (every PAA question we can answer)

### 5. Numbers and sources

For every claim of a number (price, yield, tax rate, occupancy), you need a primary source with a date. Allowed sources for nad-lan.co.il:

- Israeli: `נדלן.gov.il`, `cbs.gov.il` (CBS), `boi.org.il` (Bank of Israel), `gov.il`, court rulings, Knesset bills
- Foreign (for the abroad pillar): the country's national statistics office, central bank, tax authority, tourism ministry; Eurostat for EU
- **Forbidden as sources**: competitor sites (Madlan, Yad2, נדלן מאסטר, individual broker blogs), Wikipedia, ChatGPT summaries, "industry reports" from sales-driven firms

Every number in the article must have a parenthetical attribution: `(מקור: בנק ישראל, מרץ 2026)`. Numbers without a source get cut, even if they are probably true.

### 6. Write the ChatGPT prompt

The Blueprint output feeds into the ChatGPT prompt (we use ChatGPT for the actual Hebrew prose to save tokens). The prompt must include:

```
SYSTEM: כתוב מאמר בעברית מדויקת, ללא em-dash, ללא "חשוב להבין" / "ראוי לציין" / "בעידן הנוכחי" / "לסיכום" / "במאמר" / "באופן כללי" / "בעולם שבו" / "אינסוף" / "אכן" / "ללא ספק" / "בסופו של דבר" / "מצד אחד...מצד שני" כפסקה / "כפי שראינו" / "במילים אחרות". המאמר נכתב לאתר נדלן חכם (nad-lan.co.il).

קהל: [העתק את ה־intent מסעיף 3]
כותרת: [H1 מסעיף 4]

מבנה חובה (h2 לכל סעיף, על פי הסדר):
1. [נושא 1 מהשלד המשותף]
2. [נושא 2]
...
n. שאלות נפוצות (h2). מתחתיו 5-8 שאלות מ"אנשים גם שואלים" עם תשובה של 80-150 מילים לכל אחת.

כללי:
- שלב נתונים עם מקור ותאריך. אל תמציא מספרים. אם אינך בטוח, כתוב "טעון אימות".
- אורך כולל: 1,800-2,500 מילים.
- פסקאות קצרות (3-5 שורות).
- ללא רשימות bullet אלא אם זה רשימת שלבים או דרישות חוק.
- ללא דרמה, ללא הבטחות, ללא "ההזדמנות של 2026". עובדות בלבד.

פלט: HTML גולמי המוכן להדבקה. רק תגי <h2>, <h3>, <p>, <ul>, <li>, <strong>. ללא <html>, <head>, <body>. ללא markdown. ללא "להלן מאמר" / "הנה המאמר" / הערות שקיפות / footnotes כמו "Source+9". ללא em-dash. שמור על dir="rtl" בכל בלוק.

[הדבק כאן את הנתונים מסעיף 5 — כל מספר עם מקור ותאריך]
```

### 7. Hand off to the publishing protocol

The ChatGPT output goes to `article-publishing-protocol.md`. That is where the article becomes a live page with proper design, schema, Yoast meta, internal links, and CTA. **Do not skip the publishing protocol** — that is what produced the 6 broken country pages on 2026-05-29.

## What Cowork has done wrong (recorded for self-correction)

The 7 short-rent-abroad country spokes published 2026-05-29 by Cowork:

- 6 of 7 were pasted into WordPress with the HTML **double-escaped** — users saw `<h2 dir="rtl">title</h2>` as literal text. Fixed by Claude Code 2026-05-30.
- 4 of 7 were missing Yoast meta description entirely (Greece, Italy, Spain, Cyprus). Google falls back to the first paragraph, which on the broken pages was "להלן מאמר HTML נקי להדבקה" — visible in SERP.
- Every spoke had only 1 internal link (back to pillar). No spoke→sibling, no spoke→calculator, no spoke→lawyer CTA. Orphaned.
- Several spokes opened with ChatGPT's transparency note ("כלי החיפוש לא החזיר תצוגה מלאה של 'אנשים גם שואלים'...") which should have been removed before publishing.
- Citation footnotes from Perplexity / ChatGPT (e.g. `Government of Israel+9נדלן מאסטר+9Portukey+9`) were left in the body.
- None included an author byline despite touching tax and regulation (per `copywriting-skill.md` §8, mandatory).

Every one of these failures would have been caught by the publishing protocol. **Cowork: read the publishing protocol next.**

## Quality bar — is the article Google-Blueprint eligible?

Before publishing, the article must pass this checklist:

- [ ] Every mandatory h2 from the shared SERP backbone is present.
- [ ] At least 2 differentiator sections from the SERP top-3.
- [ ] At least 1 gap section that answers a PAA question NONE of the top 10 answered well.
- [ ] Every number has source + date.
- [ ] No forbidden phrases (see `copywriting-skill.md` §3 + §4).
- [ ] No em-dashes anywhere.
- [ ] Q&A block at the bottom covering 5-8 PAA questions.
- [ ] Author byline if the article touches tax, contract, or legal (per copywriting-skill §8).
- [ ] Length 1,800-2,500 words for a spoke; 2,500-4,000 for a pillar.

If the article fails any item, do not publish. Send back to ChatGPT with the specific gap.

## Worked example — the Portugal article (what it should have been)

Query: השקעת נדל״ן בפורטוגל

Intent: evaluation-stage investor, has capital, comparing destinations, wants regulation + tax + yield in one place.

Shared backbone (from the SERP top-10):
- מצב רגולציית Alojamento Local (Mais Habitação + Decreto-Lei 76/2024)
- מס רכישה לזרים (IMT)
- מס הכנסה על שכירות לטווח קצר
- אמנת מס ישראל-פורטוגל
- אזורים מותרים / חסומים (ליסבון, פורטו, אלגרבה)
- תשואה ממוצעת
- ויזת Golden (סטטוס 2026)

Differentiators we steal from top-3:
- חישוב תשואה נטו אחרי כל המסים והעמלות
- טבלת השוואה מול יעדים אחרים (יוון, ספרד, קפריסין) — קישור פנימי

Gap we own:
- מה קורה אם הרישיון נשלל אחרי הרכישה? (no top-10 result covered this seriously)
- איך מבטחים נכס Airbnb בפורטוגל מישראל (insurance angle)

That is the Blueprint. The article writes itself once the Blueprint is done.

---
_Created 2026-05-30 by Claude Code (claude-opus-4-7) to capture the workflow Cowork uses but forgets. Owner-approved process; this file makes it persistent._
