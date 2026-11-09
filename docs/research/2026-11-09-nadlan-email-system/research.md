# nad-lan.co.il email system: evidence base

Prepared 9.11.2026. Every URL below was "read 9.11.2026" through a search or a page fetch. All text is paraphrased (public repository).

Evidence grades used in this file:
- **Fetched** = the page itself was opened and summarised.
- **Snippet** = only a search-result summary was seen; verify before relying on it.
- **Not seen** = tried and blocked or empty. Nothing is guessed.

---

## 1. Science and industry evidence on design and reading

### 1.1 How people read email (NN/g)
- NN/g's newsletter guidelines rest on 270 newsletters and 124 participants over four studies (lab test with 15, diary study with 30 in 6 countries, eye-tracking with 42 plus a field study with 6, and a lab study with 16 users in the US/UK including mobile). Fetched. https://www.nngroup.com/articles/e-mail-newsletters-usability/ (read 9.11.2026)
- Inboxes are busier: unread/new messages up 300% versus four years earlier, so people skim faster and have little patience for wordplay. Fetched. Same URL.
- A pun-style subject line (the hotel example "wonders of the sea") has too little "information scent"; users decide in the inbox. Fetched. Same URL.
- Message previews matter more (volume and mobile), so put the most valuable content first. Fetched. Same URL.
- Mobile: participants rated ease of reading newsletters on phones 3.3 out of 7 because many were badly formatted. NN/g suggests either very short or deliberately leisurely mail on mobile, not a middle. Fetched. Same URL.
- Secondary write-ups (not NN/g pages): average 51 seconds with a newsletter, about 200 words; eye-tracking shows readers take headlines and the first line or two of each story. Snippet. https://www.nngroup.com/articles/e-mail-newsletters-usability/ plus https://chiefmarketer.com/the-secret-of-e-zine-success-make-them-easy-to-scan (read 9.11.2026)
- The NN/g page does not itself report findings on from-line, single-column layout or length. Do not cite NN/g for those.

### 1.2 Clients and devices (Litmus)
- Litmus September 2026 report (over 1.5 billion opens): Apple 76.56%, Gmail 16.10%, Outlook desktop 3.48%, Yahoo 2.35%, Outlook.com 0.29%. Fetched. https://www.litmus.com/email-client-market-share (read 9.11.2026)
- Caveat: "opens" are tracked opens. Apple's share is inflated by Mail Privacy Protection machine opens, so open rate is not a reliable human-reading measure. Snippet. https://clean.email/blog/insights/mobile-email-statistics-report (read 9.11.2026)
- Mobile 41.6%, webmail 40.6%, desktop 16.2% of opens (2026), from a third-party report. Snippet. Same clean.email URL. Litmus itself gave no mobile/desktop split on the page.
- Israeli-specific client split: not found. Do not assume the global split.

### 1.3 Accessibility (Email Markup Consortium, WCAG)
- EMC 2026: 376,348 HTML emails (May 2025 to May 2026); 99.88% had a serious or critical issue; only 8 passed all automated checks. Fetched. https://www.emailmarkup.org/en/reports/accessibility/2026/ (read 9.11.2026)
- Most frequent failures: body missing `dir` 97.41%; body missing `lang` 95.66%; layout tables without `role="presentation"` 83.78%; no `<h1>` 74.23%; links without discernible text 71.23%; `<html>` without `lang` 62.16%; low colour contrast 58.48%; images without alt 47.88%; missing `<title>` 45.21%; non-descriptive link text 15.83%. Fetched. Same URL.
- EMC recommends accessibility checks as an equal gate to rendering tests, and accessible defaults in templates. Fetched. Same URL.
- WCAG 2.2 SC 1.4.3: 4.5:1 for normal text, 3:1 for large text (18pt, or 14pt bold). Fetched. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html (read 9.11.2026)
- No source in this round gave a WCAG-based minimum font size for email. The 16px body figure below is an inference, labelled as such.

### 1.4 Hebrew and RTL
- Set `lang="he" dir="rtl"` as attributes on the html element, not only in CSS; use `text-align: start` rather than `left`; avoid mixing RTL and LTR in one line. Snippet, vendor guidance. https://skills.sh/skills-il/localization/hebrew-rtl-best-practices (read 9.11.2026) and https://www.w3.org/International/geo/html-tech/tech-bidi.html (read 9.11.2026)
- Gmail is reported (secondary blog) to ignore some RTL directives, so test it. Snippet. https://tempmail.us.com/en/rtl/resolving-rtl-text-alignment-issues-in-gmail-html-emails (read 9.11.2026)
- Hebrew needs more line spacing (about 1.7 suggested by one guide) and a Hebrew-capable stack such as Heebo, Assistant, Noto Sans Hebrew, but web fonts are not reliable. Snippet. skills.sh URL above.
- Subject lines in Hebrew: RTL subject handling needs a test per client. Snippet. https://support.remarkety.com/hc/en-us/articles/360019082031-RTL-Subject-Lines-Hebrew-Arabic (read 9.11.2026)

### 1.5 Web fonts, clipping, dark mode, images
- `@font-face`: works in Apple Mail, Yahoo, Gmail mobile apps; not in Gmail desktop webmail (only Roboto and Google Sans); Outlook for Windows is partial or buggy and may fall back to Times New Roman. Last tested 19.12.2023. Fetched. https://www.caniemail.com/features/css-at-font-face/ (read 9.11.2026)
- Gmail clips the HTML above about 102KB (images hosted externally do not count; base64 images do). One vendor advises staying under about 90KB. Snippet. https://help.blueshift.com/hc/en-us/articles/42292160006675-Understanding-Gmail-email-clipping and https://www.beehiiv.com/support/article/4413255394583-ways-to-manage-email-weight-and-avoid-gmail-clipping (read 9.11.2026)
- Dark mode: guides agree on `color-scheme` meta tags, transparent PNG logos, avoiding pure #fff/#000, and testing; client behaviour is described inconsistently (Gmail especially). Snippet. https://sendlayer.com/blog/designing-emails-dark-mode-best-practices/ and https://www.litmus.com/blog/optimize-imagery-for-dark-mode (read 9.11.2026)

### 1.6 Single CTA, personal sender
- The claim "single CTA gives 371% more clicks" is repeated widely but attributed inconsistently (Wordstream, Campaign Monitor) with no primary data. Treat as unverified. Snippet. https://mailjet.com/email-playbook/click-rates/call-to-action-emails (read 9.11.2026)
- Personal-name versus brand sender: no usable evidence found. Needs our own A/B test.
- Eye-tracking or controlled evidence on single-column layout and button versus link: not found in this round. Honest gap.

---

## 2. World examples

Important limit: Really Good Emails shows each email as one image. The page text gives sender, subject and sending stack (Zillow mails show "Sent with Amazon SES") but not the layout, so structural claims below come from the archive's own editorial text or third-party write-ups and are labelled. Milled.com returned 403 for Zillow, Redfin and Compass. Searches found no archive pages for Redfin, Compass, Sotheby's International Realty, Rightmove, Knight Frank or Linear.

Real-estate category listing, 163 emails, Zillow most common: https://reallygoodemails.com/categories/real-estate (fetched, read 9.11.2026).

See the "Examples" section below for the ten chosen.

---

## 3. Israeli competitors

What I could see: almost nothing public about their emails.
- Madlan: searches found only the app-store listing (map search, new projects) and no word about email alerts or newsletters. Privacy page returned 403. https://apps.apple.com/app/id6472173076 (snippet, read 9.11.2026). No email examples: **Not seen**.
- Yad2: the App Store listing says users can create search alerts delivered by email and searches are saved automatically. No sample email found. https://apps.apple.com/il/app/%D7%99%D7%932-yad2/id406318295 (snippet, read 9.11.2026). **Not seen**.
- Homeless: search returned nothing relevant. **Not seen**.
- OnMap: company descriptions only (Rishon LeZion startup, 2016, filters by price/rooms etc.), nothing on email. https://slimpages.startupim.com/neo_company_page/onmap (snippet, read 9.11.2026). **Not seen**.
- Developers and brokerages (Azorim, Tidhar, Shikun & Binui, Africa Israel, Dimri, Gindi, RE/MAX Israel, Anglo-Saxon): search returned only news items about them on nadlancenter.co.il and Anglo-Saxon's About page with no newsletter sign-up. No archive of their campaigns found (no campaign-archive or mailchi.mp pages). **Not seen**. https://www.anglo-saxon.co.il/en/about_us/ (snippet, read 9.11.2026)
- Consequence: any "we beat the Israeli competitors" claim cannot be made from public data. The only legitimate way is a controlled test: create alerts and subscriptions from a clearly labelled test mailbox, which needs the owner's decision (this research did not sign up anywhere).

---

## 4. Law and deliverability

### 4.1 Israeli anti-spam law, Communications Law section 30A
- The law bans sending an advertisement by email (also fax, SMS, auto-dialer) without the recipient's prior consent; consent can be by writing, text, email, web confirmation or recorded call. Fetched. https://www.kolzchut.org.il/he/פיצוי_בגין_משלוח_דברי_פרסומת_ללא_הסכמה_של_הנמען_(חוק_הספאם) (read 9.11.2026)
- "Advertisement" = a message distributed commercially to encourage a purchase, service, spending, donation or propaganda. Fetched. Same URL.
- Compensation: up to 1,000 NIS per message without proof of damage, cumulative; the page also says it is a criminal offence with a fine up to 226,000 NIS (2026). Courts often award less than the maximum (examples of 350 NIS per message). Fetched (Kolzchut); court practice Snippet. Same URL and https://www.bizportal.co.il/takdin/news/article/20017396 (read 9.11.2026)
- Refusal: a message with no address or way to refuse entitles to compensation; continuing after a refusal also does. Fetched. Same Kolzchut URL.
- Existing-customer exception: details given in a purchase or negotiation can be used for ads only if all three hold: the person was told the details will be used for ads, was given a chance to refuse and did not, and the ads concern similar products or services. Fetched. Same URL. (The page does not name the subsection; commentary places it in 30A(c). Verify with counsel.)
- Marking: guidance says the word "פרסומת" must open the message and, in email, appear in the subject line; the advertiser's name and contact details and a simple way to refuse must be prominent. Snippet from Chamber of Commerce and SimpleSign summaries; the gov.il FAQ places this in 30A(e) but returned 403 and Kolzchut does not cover it. https://simplesign.co.il/learn/marketing-consent-spam-law and https://www.gov.il/he/departments/faq/17052018_7 (read 9.11.2026). **Verify the exact statute text on Nevo or the Knesset site before building templates.**
- Service versus advertisement: the legal test is whether the message is commercial promotion. Purely transactional or service messages (a confirmation of what the person asked for) are outside the definition, but mixing promotion into them risks treating the whole message as an advertisement. This is my reading of the definition above; not tested by a source. Needs counsel.

### 4.2 Privacy Protection Law amendment 13
- In force 14.8.2025; sharpened notice duty, DPO duties, new enforcement. First financial sanction reported: 256,000 NIS on a health fund (21.7.2026). Snippet. https://www.chamber.org.il/serviceslobby/legal/74023/164240/ and https://www.shibolet.com/%D7%A2%D7%93%D7%9B%D7%95%D7%9F-%D7%9C%D7%A7%D7%95%D7%97%D7%95%D7%AA-%D7%90%D7%9B%D7%99%D7%A4%D7%94-%D7%91%D7%A2%D7%A7%D7%91%D7%95%D7%AA-%D7%AA%D7%99%D7%A7%D7%95%D7%9F-13-%D7%94%D7%A8%D7%A9%D7%95/ (read 9.11.2026)
- Exact content of the notice at email collection: not found. Practical must-have to confirm with counsel: at the sign-up form say who collects, for what purposes, whether sent to third parties (Brevo as processor), and link the privacy policy.

### 4.3 Gmail and Yahoo bulk sender rules
- Google (more than 5,000 messages a day to Gmail, since 1.2.2024): SPF, DKIM and DMARC (policy may be none); From domain aligned with SPF or DKIM; DKIM key at least 1024 bit, 2048 recommended; marketing mail needs one-click unsubscribe (List-Unsubscribe and List-Unsubscribe-Post) plus a visible link in the body; spam rate under 0.30% in Postmaster Tools, under 0.10% recommended; valid Message-ID, PTR records, TLS. Fetched. https://support.google.com/a/answer/81126 (read 9.11.2026)
- The Google page does not state a 2-day opt-out window or a transactional exemption; vendor blogs add both. Snippet. https://www.bounteous.com/insights/2024/01/31/2024-gmail-and-yahoo-deliverability-changes/ (read 9.11.2026)
- Yahoo: vendor sources differ on the spam threshold; treat the 0.30% and 0.10% targets as the shared goal. Snippet. https://bird.com/docs/knowledge-base/deliverability/gmail-yahoo-requirements (read 9.11.2026)
- Brevo says it adds the List-Unsubscribe header to marketing and transactional mail; whether one-click POST is on by default must be confirmed in the account. Snippet. https://www.brevo.com/blog/list-unsubscribe-header/ (read 9.11.2026)

---

## 5. Platform options with Brevo

- Create campaign: `POST https://api.brevo.com/v3/emailCampaigns`; needs `name` and `sender`; content as exactly one of `htmlContent` (under 1MB), `htmlUrl` or `templateId`; recipients by `listIds`, `segmentIds` and exclusions; optional custom unsubscribe page id (default page otherwise); `scheduledAt` in UTC; created as draft. A/B testing and send-at-best-time are plan-gated. Fetched. https://developers.brevo.com/reference/create-email-campaign (read 9.11.2026)
- Double opt-in contact: `POST /v3/contacts/doubleOptinConfirmation` with a DOI template that contains the opt-in tag. Snippet. https://developers.brevo.com/reference/create-doi-contact (read 9.11.2026)
- Plain contact `POST /v3/contacts`; list `POST /v3/contacts/lists`. Snippet. https://developers.brevo.com/docs/available-functions-in-api-clients (read 9.11.2026)
- Official WordPress plugin "Brevo" (mailin): SMTP for transactional mail with tracking, form builder, two-way list sync, built-in double opt-in; version 3.3.6, 100,000+ installs, modified 5.11.2026; free plan stated as 300 emails per day (9,000 a month). Fetched. https://wordpress.org/plugins/mailin/ (read 9.11.2026)
- Free plan: Brevo logo on emails, contacts limit reported as 100,000 by most third-party reviews, Starter from about 9 USD a month; prices move. Snippet. https://www.sender.net/reviews/brevo/pricing/free-plan (read 9.11.2026). Brevo's own pricing page gave no figures to the fetcher. Confirm in the account.
- One-to-one mail: use the transactional SMTP/API with a template (the plugin already routes WordPress mail); marketing to lists via campaigns. Whether to build a custom sender inside WordPress or use Brevo's UI is a design decision, not an evidence question. Brevo's API for one-to-one templated sends was not fetched in this round.

---

## Requirements (numbered, testable)

Source keys: N=NN/g (1.1), L=Litmus (1.2), E=EMC (1.3), W=WCAG (1.3), H=Hebrew/RTL (1.4), F=fonts (1.5), C=clipping (1.5), D=dark mode (1.5), G=Google bulk (4.3), IL=Israeli spam law (4.1), PV=privacy (4.2), B=Brevo (5), X=example archive (2).

1. Subject lines are concrete and say what is inside; no puns or teasers. Test: 10 sample subjects read by 5 people, each can state the content in one phrase. (N)
2. The first 1-2 lines (preheader and opening) carry the single most useful fact. Test: preheader text set explicitly, under inbox truncation on iPhone and Gmail. (N)
3. One primary action per email, shown as a button; secondary links visually weaker. Test: exactly one button style used once above the fold. (N gap, X MailNinja example; the "371%" number is not to be cited)
4. Single-column layout at 600px max, readable at 375px without zoom. Test: render check on iPhone Mail and Gmail app. (N mobile 3.3/7, L Apple and Gmail dominate)
5. Body text at least 16px on mobile, line-height about 1.6-1.7 for Hebrew. Test: computed CSS. (Inference from N and H; no direct study)
6. Length is deliberate: skim version under about 200 words, or a clearly longer reading piece. Test: word count per template type. (N)
7. `<html lang="he" dir="rtl">` and `dir="rtl"` on body and main blocks; `text-align:start`. Test: Gmail web, Gmail app, Apple Mail, Outlook screenshots show correct alignment. (E, H)
8. All layout tables carry `role="presentation"`. Test: automated check. (E)
9. One `<h1>`, real heading order, a non-empty `<title>`. Test: automated check. (E)
10. Every image has alt text; logo and buttons never exist only as images. Test: remove images and read the email. (E)
11. Text contrast at least 4.5:1 (3:1 for large text), in light and dark. Test: contrast checker on every colour pair. (W, E)
12. Link text describes the destination; no "לחצו כאן". Test: list all link texts. (E)
13. Font stack: web font only as enhancement, then a Hebrew-capable system font (for example Arial, Tahoma), never Times fallback. Test: render with web font blocked in Outlook Windows and Gmail web. (F, H)
14. Rendered HTML under 102KB, aim under 90KB; no base64 images. Test: byte count of final HTML. (C)
15. Dark mode: `color-scheme` meta, transparent PNG or SVG-safe logo, no pure white or black, checked in Apple Mail dark and Gmail dark. (D)
16. Success is measured by clicks and conversions, not open rate. Test: dashboard shows clicks first. (L, clean.email)
17. Sender name is stable and recognisable; person-plus-brand versus brand-only decided by our own A/B test. (no evidence found; N gap)
18. SPF, DKIM (2048), DMARC aligned on the sending domain; Message-ID, TLS valid. Test: header analysis of a live send. (G)
19. Marketing mail carries List-Unsubscribe and List-Unsubscribe-Post (one-click) and a visible unsubscribe link; opt-out processed immediately. Test: raw header inspection and a real unsubscribe click. (G, B, IL)
20. Spam-rate monitoring in Google Postmaster Tools, alert at 0.10%, hard stop at 0.30%. (G)
21. Israeli advertisement rules: written consent record per contact (time, source, wording); the word "פרסומת" at the start of the subject and message; sender name and contact details; a working refusal route. Test: checklist on each template; statute text confirmed by counsel. (IL; marking rule from secondary sources)
22. Service and transactional messages contain no promotion, and live in a separate Brevo stream from marketing. Test: template review. (IL, G, B)
23. Sign-up form shows who collects the address, why, that Brevo processes it, and a privacy-policy link; double opt-in for newsletters. (PV, B, IL)
24. Templates are delivered as one HTML source imported through `htmlContent` or `templateId`, with merge fields for name and listing; test sends before every campaign. (B)
25. One-to-one sends use a transactional template with the same brand parts; lists and segments (buyer, renter, landlord) are kept in Brevo, not in WordPress. (B)
26. Release gate: automated accessibility check plus screenshots in Apple Mail, Gmail web and app, Outlook Windows, Outlook.com; results saved with the template. (E, L shares)

---

## Matrix

Cells come from evidence only. Y = Yes, P = Partial, N = No, U = Unknown (not seen). For the world examples the archive shows images only, so most cells are U on purpose. For Israeli competitors nothing was seen, so every cell is U.

| # | Requirement (short) | Zillow | Redfin | Airbnb | Stripe | Apple | MailNinja | Smashing | Madlan | Yad2 | Homeless | OnMap | Developers/brokers |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Clear subject | P (subjects readable in archive) | U | U | P | U | U | U | U | U | U | U | U |
| 2 | Preheader/first lines | U | U | U | U | U | U | U | U | U | U | U | U |
| 3 | One primary CTA | N (reported two listings side by side, several links) | P (reported one main button plus links) | U | U | U | Y (archive text: one CTA) | U | U | U | U | U | U |
| 4 | Single column, mobile OK | U | U | Y (archive text: mobile optimised) | U | U | U | Y (archive text: mobile optimised) | U | U | U | U | U |
| 5 | Body text 16px | U | U | U | U | U | U | U | U | U | U | U | U |
| 6 | Length deliberate | U | U | U | U | U | Y (short, skimmable) | P (long with TOC) | U | U | U | U | U |
| 7 | lang/dir correct | n/a | n/a | n/a | n/a | n/a | n/a | n/a | U | U | U | U | U |
| 8-12 | Accessibility set | U | U | U | U | U | U | U | U | U | U | U | U |
| 13 | Font stack | U | U | U | U | U | U | U | U | U | U | U | U |
| 14 | Under 102KB | U | U | U | U | U | U | U | U | U | U | U | U |
| 15 | Dark mode | U | U | U | U | U | U | U | U | U | U | U | U |
| 16 | Click-based KPI | n/a | n/a | n/a | n/a | n/a | n/a | n/a | U | U | U | U | U |
| 17 | Stable sender | Y (From: Zillow) | U | U | Y (From: Stripe) | U | U | U | U | U | U | U | U |
| 18 | SPF/DKIM/DMARC | U | U | U | U | U | U | U | U | U | U | U | U |
| 19 | One-click unsubscribe | U | U | U | U | U | U | U | U | U | U | U | U |
| 21 | Israeli ad rules | n/a | n/a | n/a | n/a | n/a | n/a | n/a | U | U | U | U | U |
| 22 | Service vs promo split | U | U | U | U | U | U | U | U | U | U | U | U |
| 23-26 | Platform/process | n/a | n/a | n/a | n/a | n/a | n/a | n/a | U | U | U | U | U |

Matrix evidence: Redfin and Zillow cells from https://mailbakery.com/blog/real-estate-email-newsletter-examples/ and https://emailmonks.com/blog/?p=13113 (secondary, snippets); Airbnb, Smashing, MailNinja from https://reallygoodemails.com/school/blog/newsletter-examples (fetched); Zillow and Stripe sender from the archive pages below (fetched). The honest conclusion: to fill the U cells, someone must open the real emails in real clients (Litmus or Email on Acid previews, or saved .eml files), and a controlled test inbox is needed for the Israeli competitors.

---

## Examples (ten, with archive URLs)

1. Zillow, "The most affordable markets, ranked", newsletter: https://reallygoodemails.com/emails/zillow-affordable-markets-newsletter (fetched). Learn: a ranked-list subject with a clear promise; sent through Amazon SES; archive shows only an image, so check structure by rendering. Third-party notes praise Zillow's side-by-side listing cards (mailbakery URL above, snippet).
2. Zillow, "Introducing Plan: Your personalized moving hub", product launch: https://reallygoodemails.com/emails/zillow-plan-moving-hub-launch (fetched). Learn: one new feature per email with a descriptive alt text on the hero.
3. Zillow, welcome email: https://reallygoodemails.com/emails/welcome-to-zillow (listed, not opened). Learn: the onboarding message is a real-estate example worth rendering for our own welcome flow.
4. Zillow, "Test your knowledge of common home-buying myths" quiz: https://reallygoodemails.com/emails/zillow-home-buying-myths-quiz (listed). Learn: interactive or quiz content as a way to earn attention.
5. AirDNA, October 2026 market newsletter, "Top 10 markets to buy a lake house": https://reallygoodemails.com/emails/airdna-october-2026-market-newsletter (fetched). Learn: data-led ranking subject; useful model for our price-index mail.
6. Cotality welcome newsletter: https://reallygoodemails.com/emails/cotality-newsletter-welcome (listed). Learn: a welcome that sets expectations for a property-data audience.
7. Stripe, transactional email design: https://reallygoodemails.com/emails/transactional-email-design-from-stripe (fetched, image only). Learn: strict, minimal transactional look; verify details by rendering.
8. Airbnb newsletter (Melbourne guide): https://reallygoodemails.com/airbnb/ (archive blog says strong opening image, informative content, on-brand, works on mobile). Learn: photo-led story with a mobile-first build.
9. MailNinja: https://reallygoodemails.com/mailninjauk/ (archive blog: short, conversational, one CTA, minimal imagery). Learn: the single-CTA discipline in a skimmable email.
10. Smashing Magazine newsletter: https://reallygoodemails.com/smashing-magazine/ (archive blog: table of contents, mix of text, images and links, mobile optimised). Learn: a contents block helps long mail.

Also found but not usable: Apple appears under the app and subscription categories (https://reallygoodemails.com/categories/app); no direct email page was opened. Redfin, Compass, Sotheby's International Realty, Rightmove, Knight Frank and Linear: no archive pages found. Milled blocked automated access (403).

---

## Open gaps (to say plainly)
- No real Israeli competitor emails seen; no published evidence of their consent or unsubscribe practice.
- Exact statute wording for the "פרסומת" marking was not read from the statute itself.
- No controlled evidence found for personal-versus-brand sender name, button-versus-link, or single-column layout.
- Brevo's current prices and one-click default were not confirmed from Brevo's own pages.
