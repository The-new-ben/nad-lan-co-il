# Nadlan ChatGPT SERP Blueprint Workflow - 2026-06-02

Codex stamp: 2026-06-02. Purpose: keep Codex focused on research orchestration, quality control, WordPress publishing, verification, scripts, and architecture, while ChatGPT produces the heavy Hebrew article drafts.

This is the workflow to use for every new pillar, spoke, glossary batch, city page, or professional/service page that needs more than a small paragraph.

## Boundary

Codex should not write full 1,000-4,000 word Hebrew articles unless the owner explicitly authorizes it. Codex may write:

- SERP research briefs.
- ChatGPT prompts.
- Outline corrections.
- Small Hebrew corrections or additions.
- QA notes.
- WordPress publishing scripts.
- Internal linking and metadata.
- Verification reports.

ChatGPT should write the long Hebrew article body.

## Step 1 - Choose One Query

One URL gets one primary query. Do not write one article for several money keywords.

Examples:

- Good: `מחשבון משכנתא`, `מס רכישה דירה ראשונה`, `שמאי מקרקעין לפני קניית דירה`.
- Bad: `נדלן`, `השקעות ומס רכישה ומשכנתא`, or keyword strings no human would type.

Record:

- Target URL.
- Primary query.
- Secondary terms.
- Searcher stage: information, comparison, transaction, tool, directory, professional.
- Revenue path: tool use, inquiry, professional comparison, claim/upgrade, project inquiry, or paid product.

## Step 2 - SERP Blueprint Research

Do a manual Google search from Israel, Hebrew interface if possible. Record:

- Top 10 organic results: URL, title, meta snippet.
- Page type: law firm, bank, portal, government, blog, calculator, directory, news.
- H1 and H2 structure where accessible.
- Estimated word count.
- Visible tools, tables, calculators, images, videos, forms.
- People Also Ask questions.
- Related searches.
- Featured snippet or AI Overview style answer if visible.
- Ads or map pack presence.

The goal is not copying. The goal is understanding the answer Google already rewards.

## Step 3 - Intent Model

Write one sentence:

`Google appears to rank pages that answer [exact user need] with [format], [trust proof], and [decision support].`

Example:

`Google appears to rank purchase-tax pages that combine current brackets, calculator-style explanation, first-home versus investor scenarios, legal caveats, and official Tax Authority references.`

## Step 4 - Competitor DNA

Create a brief, not copied text:

- Shared backbone: subtopics 7+ of top 10 cover.
- Top-3 differentiators: what the strongest pages do better.
- Gaps: what none of them answer clearly.
- Tone: legal, financial, portal, conversational, data-heavy, checklist.
- Visuals: calculators, tables, screenshots, property photos, maps, professional portraits.
- CTA style: contact form, calculator, phone, guide download, advisor matching.

## Step 5 - Required Sources and Numbers

Numbers need primary or official sources. Prefer:

- Bank of Israel.
- Israel Tax Authority.
- nadlan.gov.il.
- gov.il.
- CBS.
- Planning Administration.
- Knesset/court/official laws where relevant.
- Foreign official tax/tourism/statistical sources for international investment topics.

Do not source claims from competitor articles. Competitors are for structure and gaps only.

## Step 6 - ChatGPT Prompt Template

Use this prompt in ChatGPT for the heavy Hebrew body.

```text
You are writing a public Hebrew article for nad-lan.co.il, a consumer-facing Israeli real estate decision site.

Task:
Write an original Hebrew article for the query: [PRIMARY QUERY].

Searcher intent:
[INTENT MODEL]

Target URL:
[TARGET URL]

Article role:
[pillar/spoke/tool landing/directory guide/glossary term/city page]

Required H1:
[H1]

Required sections in this order:
[SERP SHARED BACKBONE]

Differentiator sections to add:
[TOP-3 DIFFERENTIATORS]

Gap sections to answer:
[PAA/GAP QUESTIONS]

Facts and source data to use:
[OFFICIAL SOURCE FACTS WITH DATES]

Internal links to include naturally:
[PILLAR, SPOKES, TOOLS, DIRECTORY LINKS]

Public voice rules:
- Write only for people who need real estate help, not for the site owner.
- Do not mention SEO, search intent, money pages, leads, CRM, suppliers, monetization, prompts, ChatGPT, Lovable, or internal workflow.
- Do not copy competitors. Use the research only as structure and intent understanding.
- No em dash, no en dash, no AI-like repetition.
- Avoid generic phrases such as "חשוב להבין", "בעידן", "לסיכום", "במילים אחרות" unless truly necessary.
- Be practical, specific, informative, and calm.
- Use Hebrew consumer language, not internal marketing language.

Output format:
- Raw HTML only.
- No markdown.
- No <h1>.
- Use only <h2>, <h3>, <p>, <ul>, <ol>, <li>, <strong>, <table>, <thead>, <tbody>, <tr>, <th>, <td>.
- Add dir="rtl" to block elements.
- No <style>, no <script>, no <html>, no <head>, no <body>.
- No preamble before the article.
- No footnote citation tokens. Convert sources to clean inline Hebrew, for example: (מקור: בנק ישראל, מרץ 2026).

Length:
[1,800-2,500 words for spoke, 2,500-4,000 words for pillar, 250-450 words for glossary term unless otherwise specified]
```

## Step 7 - Codex QA Before Publishing

Before publishing any ChatGPT output, Codex should scan:

- No internal terms.
- No ChatGPT preamble.
- No escaped HTML such as `&lt;h2&gt;`.
- No em dash or en dash.
- No duplicate H1.
- Correct target keyword in title/H1/opening.
- All required SERP sections included.
- Official sources included where numbers appear.
- Link count appropriate, with descriptive anchors.
- No cannibalization with existing pages.
- Word count meets coverage floor.

If it fails, send a short correction prompt back to ChatGPT. Do not patch a bad long article manually unless the edit is small.

## Step 8 - Publishing Protocol

After QA:

- Convert to Gutenberg blocks where required.
- Set title, slug, parent, Yoast title, meta description, focus keyword, and canonical.
- Add Article schema or appropriate structured data if available.
- Add internal links up to the parent hub, sideways to siblings, and down to relevant tools/directories.
- Add public disclaimer for legal/tax/finance pages.
- Publish, do not leave as draft unless owner requests.
- Verify live URL: HTTP 200, one H1, canonical, viewport, no internal terms, no broken layout.
- Record the page in the report and skill/site-state docs.

## Step 9 - Glossary Variant

Glossary terms use the same process but shorter.

Decision before writing:

- If intent is the same as a money page, create an H2 anchor inside the money page instead of a new glossary URL.
- If intent is definitional and distinct, create a standalone `nadlan_term`.
- If the term is an English Wikipedia gap with no serious Hebrew page, prioritize it.

Each standalone term needs:

- Definition-first lead.
- Practical meaning.
- When it appears in a real transaction.
- Common mistake.
- Related terms.
- Link up to one parent pillar/spoke.
- Official source where relevant.

## Step 10 - What Codex Should Report

Every batch report should include:

- Keywords researched.
- Competitor URLs and what was learned from them.
- ChatGPT prompts used.
- Article URLs published.
- QA failures and fixes.
- Internal links added.
- Revenue path for each page.
- Remaining gaps.
- Screenshots or live verifier output.

## Honesty Rule

If a page is not published and live-verified, do not call it done. If a plugin or theme code path blocks the fix, state the blocker and the exact next technical step. If an article was generated by ChatGPT, say that ChatGPT generated the long body and Codex did QA, publishing, and verification.
