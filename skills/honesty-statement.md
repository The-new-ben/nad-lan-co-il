# Honesty Statement — what's real, what's inferred, what's unknown

> **Notice to all agents:** This is the single most important file for trust. Never let the strategy docs drift into fake-precision. If you add a number, add a source. If you can't source it, flag it as inferred.

_Authored 2026-05-28 by Claude Code (model id: `claude-opus-4-7`) during research-only brief task._

## What I (Claude Code) verified live during this session

I ran four live Google searches on 2026-05-28 and read the result snippets. Sources captured in `../docs/research/serp-snapshots-2026-05.md`.

1. **SERP for "מחשבון משכנתא"** is dominated by banks (Mizrahi-Tefahot, Hapoalim, Leumi, Jerusalem) + insurer (Clal) + niche finance sites (fc-israel, moti.org.il, mashcantaman, loan-israel). **No Yad2 / Madlan / general property platforms in top 10.** This is the wedge keyword — verified live, not inferred.
2. **SERP for "נדלן להשקעה"** in top 10 contains nadlanmaster (positions 1 + 2 + 4), Ynet (3 + 5), I Know First, beta-estate, Madlan (10), and finance bloggers. **No dominant authority.** Confirmed entry opportunity.
3. **SERP for "מס רכישה 2026"** is **dominated by law firms**: doron-aharoni.com, israel-law.co, prlaw.co.il, avocat-en-israel.com, magdilim.co.il. Government simulator at #10. **This is the strongest finding for the owner: as a practicing lawyer, the owner can rank on legal SERPs with native E-E-A-T that content sites cannot replicate.**
4. **SERP for "דירות למכירה בתל אביב"** is occupied by Yad2 + Madlan at the top with very large inventory counts (Yad2: thousands daily, Madlan: 9,527 specific to TA-Jaffa). **Confirmed: this keyword cluster is not winnable head-on.**
5. **Purchase tax 2026 brackets verified**:
   - First apartment (דירה יחידה): 0% up to 1,978,745 ₪, then 3.5% to 2,347,040 ₪, then 5% to 6,055,070 ₪, then 8% to 20,183,565 ₪, then 10%.
   - Investor / second+: 8% from first shekel up to 6,055,070 ₪, then 10%.
   - Brackets are **frozen** until 2028-01-15 (Arrangements Law).

## What was carried in from the user-supplied strategy doc (Semrush, May 2026)

The 2026-05 brief uploaded by the owner cites Semrush IL data: keyword volumes, KD, CPC, organic traffic for Madlan (~192K/mo), Yad2 (~3.21M/mo whole-site). I did not independently verify those Semrush numbers in this session. They are reasonable and consistent with my SERP observations, but treat them as **second-hand verified** rather than primary.

## What is inferred — reasonable but unverified

- **Israeli mortgage broker per-lead price (150-400 ₪/qualified lead)** — inferred from general market knowledge of the Israeli lead market. Needs validation by contacting 2-3 actual brokers.
- **Real estate lawyer fee 0.5-1% of deal value** — typical Israeli market rate, but varies by firm and deal size. The owner can confirm directly.
- **Israeli broker commission 2% per side** — common rate but not universal; sometimes 1.5% or 2.5%. Confirm in writing if used in marketing.
- **Foreign-investor lead value 500-2,000 ₪** — market estimate. No firm source. Don't publish.
- **Yad2 / Madlan project-marketing fees (20K-80K ₪/month)** — directional. Real numbers require a sales conversation with Yad2/Madlan as a prospective advertiser.
- **The percentage of traffic Madlan / Yad2 get from their homepage** (37% / 36% in the original brief) — Semrush estimate; varies week to week.

## What needs paid tools or first-party data to verify

- Backlink profiles of nad-lan.co.il vs competitors → Ahrefs or Semrush Backlinks API.
- True authority score and trend for the domain → Semrush DA, GSC.
- Per-keyword click-through rates → Google Search Console of the live site (not yet verified — the owner has not opened GSC as of 2026-05-28).
- Position tracking → Semrush or SERanking.
- Competitor revenue → not publicly available; estimates only.
- Whether `nadlan.gov.il` data may be re-published commercially → needs a written legal opinion. The owner is a lawyer; should make this call directly.

## What I (Claude Code) cannot do from the current environment

- I run in an ephemeral cloud Linux container. **I cannot read `C:\Users\pro\.codex\generated_images`** on the owner's Windows PC. Codex running on the owner's machine must handle that folder. Protocol for it is in `image-pipeline.md`.
- I cannot log into WordPress, GSC, GA4, Semrush, Ahrefs, or any authenticated service.
- I cannot run Lighthouse, Screaming Frog, or visual diff tools against the live site from this container.

## The trust rule

Future agents adding to strategy or content: if you add a number, add a source line beside it. If you cannot, write "(inferred, needs source)" in plain text. Numbers without sources rot the brief.

## Operational honesty rule

Do not use a missing local tool as a reason to continue with weaker workaround work. In Codex
desktop, install missing local tools when safe, verify the installation, and continue. If the
blocker is owner-only (login secret, 2FA, paid purchase, private API key, legal/business approval),
stop and ask for exactly one physical action. Be precise: "I need you to click X" or "I need the
Mapbox token pasted into Y." Do not blur this into "no access" if the browser or machine already
has access.

---
_Last reviewed: 2026-05-28 — Claude Code (claude-opus-4-7)._
