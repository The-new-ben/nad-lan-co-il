# Government forms on nad-lan.co.il: research (17.11.2026)

Who did what: this session (Opus 5.5) did every search itself in Ben's Chrome ("gmktec"), and read the sources, the Google help page and the gov.il terms. No sub-agents were used. Screenshots are in `screens/`.

## 1. What Google Israel shows (manual, 17.11.2026, desktop, hl=iw gl=il)
| Query | What wins |
|---|---|
| טפסים להורדה מקרקעין | gov.il x2, then lawyers' forms pages: toledano.co.il, limorarbel.com, amitvered.co.il, admit-law.co.il, taxo.co.il, myglaw.co.il, menikoren.co.il |
| טופס 7000 הצהרה על מכירת זכות במקרקעין | AI overview citing gov.il, kolzchut, easydo. Organic results: gov.il x2, calltext magazine, hmercaz.com, **shuma-atzmit.co.il hosted PDF copy (form 7000א)**, kolzchut, easydo, what2do |
| בקשה לביטול הערת אזהרה טופס | gov.il DOC, gov.il service page, **toledano.co.il hosted PDF copy (#3)**, then limorarbel, admit-law, alev-law, amitvered, and **jus-tice.co.il (Ben's own site)** |

People also search for: רשות מקרקעי ישראל טפסים להורדה · טופס בקשה לביצוע פעולה במקרקעין · טפסים לשכת רישום מקרקעין · רמ"י טפסים ושטרות · טופס 7000 מקוצר · טופס 7005 · טופס 7002 · טופס 7009 · בקשה לרישום הערת אזהרה · ביטול הערת אזהרה מקוון · אגרה לרישום הערת אזהרה · בקשה למחיקת משכנתא.

People also ask: איפה אני יכול למצוא טופס בקשה לתיקון הערת אזהרה? · איך מגישים בקשה לרישום הערת אזהרה? · איפה אני יכול למצוא טופס בקשה לרישום הורשה?

The competitor teardown that matters: amitvered.co.il "לשכת רישום מקרקעין טפסים" ranks top 5 with **321 words, 16 self-hosted PDF/DOC copies, 0 links to gov.il** and only Attorney schema. Thin pages win this SERP. The bar is low.

## 2. Ben's "the government site links to me" effect: real, documented, not controllable
- Google's own Links report help (support.google.com/webmasters/answer/9049606): the target URL shown can differ from the link URL when "Google has decided that the canonical URL for URL on linking page is the target URL." So when Google clusters byte-identical copies of the same file and picks OUR copy as canonical, links that point to the other copies (gov.il, lawyers) appear as links to us.
- Glenn Gabe, GSQi, 1.4.2024, "Shifting Signals": a real client case where the GSC Links report showed strong domains linking to a third-party site's URLs, credited to the client because those URLs were canonicalised to the client's. He warns that "Google can always reverse its decision about which url is the canonical", which produced yo-yo rankings.
- Dan Petrovic (DEJAN) named it "link inversion" in 2018: among identical documents, the highest-authority copy becomes canonical, and the others' links count toward it. He also notes it is a hypothesis, not documented Google behaviour.
- Google Search Off the Record ep. 115 (13.10.2026, Mueller + Splitt): for PDFs Google asks whether the file is "one-to-one identical as we've seen elsewhere". Publishers can set rel=canonical in the HTTP header, add a visible home link at the top of the PDF (Google keeps it when it converts the PDF), and fill the metadata.
- Conclusion: the effect exists (Ben has seen it on other sites). It requires a byte-identical file, and against gov.il it usually loses, because gov.il is the higher authority. It is more likely to happen when the gov.il URL moves or breaks (gov.il restructures often), or against copies held by small lawyers' sites. It is a bonus, not a plan. It can also flip back.

## 3. Forums
- Reddit is blocked to the Chrome extension, and site:reddit.com searches for this exact tactic returned nothing. r/TechSEO has "Canonical URLs counted as Backlinks in Search Console" (7 years old) on the same effect. BlackHatWorld threads about PDF tactics are mostly spam-link schemes, which we should not do.
- Honest gap: I did not find a practitioner thread that reports the gov-form tactic specifically with numbers. The best practitioner evidence is Gabe's case and Petrovic's post above, plus the live Israeli SERP, where hosted PDF copies by lawyers rank.

## 4. Legal: the gov.il terms (read in full on 17.11.2026, page updated 17.11.2026)
"בכפוף לדיני זכויות יוצרים, אסור למשתמש להעתיק, לפרסם ... להעמיד לרשות הציבור ... חומר מוגן, ללא הסכמה מראש ובכתב מאת המשרד". Fair use with source attribution is allowed. Lawyers do host copies widely in practice, but on paper hosting a copy needs written consent. Contact: moked@mail.gov.il; removal requests go to Egov-Lishka@cio.gov.il. data.gov.il datasets are under a separate open licence. This is not legal advice; a lawyer should confirm. Practical paths: (a) link to the official file plus our own HTML guide (zero risk); (b) ask gov.il for written consent to mirror specific forms (safest way to host); (c) host copies like the lawyers do (low practical risk, formally not allowed).

## 5. nad-lan's own Search Console (17.8-15.11.2026)
123 form, document and download style queries; 1,337 impressions; 5 clicks. Demand already seen: "מחירון דקל pdf / להורדה / להורדה חינם" (~250 impressions on the glossary page), "נסח טאבו" family (owner page /tabu-extract-check/), "בדיקת חוזה / עורך דין חוזה מקרקעין" (/real-estate-lawyer/). A forms hub must link to these owners and never retarget their head words.
URL word audit (tools/gsc/url_word_audit.py, 4,667 URLs): "forms" owned by 0 URLs, "download" by 0, "documents" by 1 (/real-estate-lawyer/condo-documents/).
