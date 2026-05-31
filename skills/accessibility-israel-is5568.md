# Skill: Web Accessibility — Israeli law (IS 5568 / WCAG AA), native not overlay

> How nad-lan.co.il complies with Israeli web-accessibility law the RIGHT way: native, code-level accessibility (which also helps SEO), a mandatory accessibility statement, and explicitly NOT a fake "overlay" widget. Grounded in verified research (sources at bottom). **Research, not legal advice — verify turnover/headcount brackets and the current IS 5568 edition before certifying.**

## The verdict in one line
Israeli law requires the **website itself** to conform to **ת"י 5568 / WCAG 2.0 AA** (build to **2.1 AA** to be safe) via **native** accessibility. **Overlays (accessiBe / Nagich / UserWay / EqualWeb) are NOT compliance** — the FTC fined accessiBe **$1M** (2025) for claiming they are, they attract lawsuits, and they hurt SEO/performance. A compliant **הצהרת נגישות** with a **רכז נגישות** is separately mandatory.

## Legal stack
- **חוק שוויון זכויות לאנשים עם מוגבלות, התשנ"ח-1998** — primary statute.
- **תקנות (התאמות נגישות לשירות), התשע"ג-2013** — operative regs; **תקנה 35** is the website clause.
- **ת"י 5568** — technical standard incorporated by reference = **WCAG 2.0 AA** (national modifications, lighter on Hebrew video captioning). Heavier captioning duties for public authorities / entities over ₪5M revenue (content after 25.10.2017).
- **Scope:** any business serving the public via a website. A real-estate/legal info site is in scope.
- **Deadlines:** all passed (general sites 25.10.2017; small biz under ₪300k by Oct 2020). Operators under ₪100k revenue are exempt from the full technical standard but **still must publish an accessibility statement**. (Verify the site's bracket.)
- **Penalties:** civil up to **₪50,000 without proof of damage** (main litigation driver); criminal up to ₪150,000; admin ~₪7,500/day. **60-day cure window** on complaint — a documented remediation process matters in court.
- **Enforcement:** נציבות שוויון זכויות לאנשים עם מוגבלות (Ministry of Justice); private plaintiffs + NGOs can sue.
- **רכז נגישות** mandatory at ≥25 employees; name a contact regardless.

## The accessibility statement (DONE — page id 647, /accessibility/)
Legally mandatory even if exempt from the technical standard. Rules: live HTML (not image/PDF), prominent + on every page (footer), treated as a binding legal document. Must contain: conformance declaration (ת"י 5568 AA), date, who performed the work, **honest known limitations**, and **רכז נגישות contact (name/phone/email)**. Our statement is HONEST: it says remediation is ongoing and that we deliberately do NOT use an overlay — never claim full compliance we haven't achieved (that's the accessiBe deception the FTC punished).
**OPEN ITEM:** the statement must be linked in the **site-wide footer** (currently a page; footer link requires a theme/menu edit — see open items).

## Overlays — the honest answer (do NOT install one)
- Do not achieve legal compliance; automated tooling fixes <half of WCAG issues. Overlay Fact Sheet signed by 800+ professionals; no overlay makes a site compliant or removes legal risk.
- WebAIM: ~67-69% of practitioners rate overlays ineffective; only ~2.4% of disabled users found them effective; blind users install extensions to BLOCK them.
- Lawsuits increasingly cite the overlay itself as evidence of "awareness without action." FTC v. accessiBe: $1M settlement + 20-yr bar on unsubstantiated claims.
- SEO harm: heavy third-party JS slows Core Web Vitals (a ranking factor); client-side DOM changes aren't crawlable → no SEO value. Often injects bad ARIA that breaks real screen readers.

## Native accessibility ↔ SEO (mostly aligned)
**[SEO+]** semantic HTML/landmarks, one H1 + correct heading order, alt text (not keyword-stuffed), `lang="he" dir="rtl"`, descriptive link text, text resize/responsive (no `user-scalable=no`).
**[SEO·]** color contrast (≥4.5:1 text, ≥3:1 large/UI), visible focus indicators, skip-to-content, keyboard nav, form labels, reduced-motion.
**[SEO-risk] avoid:** bad/excessive ARIA ("no ARIA is better than bad ARIA"), keyword-stuffed alt, `aria-hidden` on real content, hidden-text/cloaking, overlay scripts.

## WordPress (forked Twenty Twenty-Five — accessibility-ready, re-verify the fork)
Check: `lang="he" dir="rtl"` emitted; skip link ("דלג לתוכן") works; one H1/template + no heading skips in our block patterns; no `outline:none` without replacement; `theme.json` palette ≥4.5:1 (watch grey-on-white); forms have real `<label>`; viewport has no `user-scalable=no`; post-2017 PDFs tagged or HTML alternative.
Tools: axe DevTools, WAVE, Lighthouse (a11y + CWV/SEO in one run), Pa11y CI, + manual Tab pass and NVDA/VoiceOver. Automated catches only ~30-50% — manual testing is mandatory.
Plugins: helpful = "Equalize Digital Accessibility Checker", "WP Accessibility" (Joe Dolan) — auditors/fixers, NOT overlays. Avoid all overlay/toolbar plugins as a compliance crutch.

## Implementation checklist (order)
Phase 0 (done/partly): confirm scope+bracket; name רכז נגישות; publish statement in footer site-wide.
Phase 1 audit: axe+WAVE+Lighthouse on home/article/form/search; Pa11y across sitemap; manual keyboard + NVDA; log each issue with WCAG SC.
Phase 2 fixes (greppable): `lang/dir` ✓; skip link; heading hierarchy; `alt`; contrast in `theme.json`; focus outlines (grep `outline:none`); form labels; link text; ARIA audit; `prefers-reduced-motion`; resize/viewport (grep `user-scalable`); accessible PDFs.
Phase 3: re-test (target zero automated errors); update statement date+level; Pa11y CI in deploy pipeline; re-test on every theme/plugin update; keep a remediation log (legal evidence).

## Sources (verified 2026-05-31)
Regs: nevo.co.il/law_html/law01/500_865.htm · he.wikisource (תקנות התאמות נגישות לשירות) · kolzchut.org.il (הנגשת אתרי אינטרנט) · isoc.org.il/freedom-of-internet/accessibility · aisrael.org
Standard: deque.com/mena-digital-accessibility-laws/israel · accessibe.com/compliance/is-5568 · boia.org
Statement: vee.co.il/website-accessibility-statement · web-a.co.il · tabnav.com
Overlays: overlayfactsheet.com · a11y-collective.com/blog/accessibility-overlays · testparty.ai · accessibility.works · silktide.com
WordPress: cmscritic.com (WP a11y checklist 2026) · teamupdraft.com · wordpress.com/support/accessibility
A11y↔SEO: a11y-collective.com/blog/seo-and-accessibility · browserstack.com/guide/accessibility-seo · jumpfly.com
**Unverified:** whether current IS 5568 edition is formally 2.1/2.2 (legal baseline is 2.0 AA — build 2.1 AA); exact turnover/headcount bracket. nevo returned 403 to fetch — confirm תקנה 35 wording directly.

_Created 2026-05-31 by Claude Code (claude-opus-4-8). Statement page live at /accessibility/ (id 647)._
