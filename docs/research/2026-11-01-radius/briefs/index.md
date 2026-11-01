# Research briefs: 10 project gaps in the north-Tel-Aviv / Herzliya radius

Prepared 1.11.2026, read-only (no site, WordPress, git, Linear or Notion change). Input: `../projects.json`, `../projects.md`. Every brief follows the page research law: intents, Google as it is, competitors read in full, a sourced facts sheet, URL ownership, and how our page wins. Page copy is not written here; the articles go through ChatGPT from these briefs.

| # | Project | Brief | Proposed slug | Slug audit | AI Overview | Top competitor | Sourced facts (rows in the facts sheet with a source) |
|---|---|---|---|---|---|---|---|
| 1 | SEVEN SEAS, Sde Dov (Electra + Dan) | `seven-seas.md` | `/projects/seven-seas/` | Pass (`seven`, `seas` free) | Shown (2 of 2 queries) | electra-megurim.com (developer, #1); calcalist and nadlancenter for prices | 13 |
| 2 | EINSTEIN 2.4.6.8 (Chen & Itay Gindi + **Shbiro**) | `shbiro-2468.md` | `/projects/shbiro-2468/` | Pass. `einstein-2468` fails: `einstein` owned by 4 URLs | Shown (3 of 3) | yad2 project 17022 (#1 on price; blocked to us) | 13 |
| 3 | Einstein 15 (Gindi + Shbiro) | `levi-55.md` | `/projects/levi-55/` | Pass. `einstein-15` fails; `levi-eshkol-55` fails on `eshkol` | Shown (2 of 2) | einstein15.co.il + madlan project page (AI's first source) | 13 |
| 4 | Philharmonit, Agnon 28 (Yossi Avrahami) | `philharmonit.md` | `/projects/philharmonit/` | Pass | Absent on the name query; shown on the address query | None ranks; yav.co.il and project-tlv are what the AI cites | 12 |
| 5 | Sde Dov plot 105 (private landowners) | `landowners-105.md` | `/projects/landowners-105/` | Pass | Shown (2 of 2) | nadlancenter 14226 (AI source); sdedov.co.il organic | 10 |
| 6 | Brodetsky North (ICR) | `brodetsky-33-39.md` | `/projects/brodetsky-33-39/` | Pass. `brodetsky-north` fails: `north` owned by 15 URLs | Shown (3 of 3) | brodetskystreet.co.il (rival Brodetsky 29 outranks ICR); yad2 15256 for price | 13 |
| 7 | Amichai 5 / Stern 18 + Stern 22 | `amichai-stern.md` | `/projects/amichai-stern/` | Pass (`amichai`, `stern` free) | Shown (3 of 3) | madlan project card (blocked) + project-tlv | 11 (+2 snippet) |
| 8a | RAMATA, Reading 22-24 (Metropolis) | `ramata.md` | `/projects/ramata/` | Pass | Shown (2 of 2) | channel22 advertorial (#1); metropolis-il.com (AI source) | 13 |
| 8b | Aviv BaReading 31-33 (Aviv Melisron) | `reading-31-33.md` | `/projects/reading-31-33/` | Pass. `aviv-bareading` fails: `aviv` held by 92 URLs | Absent on the name query; shown on the address query | magdilim (AI's first source; blocked to us); walla | 14 |
| 9 | Herzliya VILLE (Azorim) | `ville.md` | `/projects/ville/` | Pass. `herzliya-ville` fails: `herzliya` owned by 11 URLs | Shown (2 of 2) | azorim.co.il project page (AI) / yad2 15300 for price | 13 |
| 10 | Ritz-Carlton Residences, Herzliya Marina (Tidhar) | `ritz-carlton.md` | `/projects/ritz-carlton/` | Pass. Avoid `residences`, `herzliya`, `marina` | Shown (3 of 3) | Hotel booking sites dominate; israelsir listing for property | 13 |

Supporting file: `serp-log.md` holds every SERP (top 10 with titles and URLs, AI Overview citations, related searches, retrieval time UTC).

## Findings that matter across all ten
- **People Also Ask was absent in all 26 Hebrew SERPs that returned results** (Israel, Hebrew, desktop; 30 requests, 4 of them first attempts that failed and were re-run). FAQ topics in the briefs come from related searches, "people also search" boxes and the AI Overviews, and are labelled that way. None is invented.
- **AI Overviews appeared on 24 of the 26 SERPs** (absent only on the two brand-name queries `הפילהרמונית יוסי אברהמי` and `אביב ברדינג`). They mostly cite developer pages, yad2/madlan project cards and news. None of our pages is cited. Our site appeared once in the top 10 (Ashdar Einstein, query "פרויקט חדש ל' החדשה").
- **Name correction:** the Gindi partner on Einstein 2.4.6.8 and Einstein 15 is **Shbiro Group (Rami Shbiro)**, not "Shapir".
- **madlan and yad2 block reading** (HTTP 403 / Radware). Their figures appear only as snippets or inside AI Overview text and are marked as such.
- **Owner decision needed on "einstein":** the word is owned by `/ramat-aviv/einstein/`, `/projects/einstein-tower/`, `/projects/ashdar-einstein/`, `/projects/einstein-19/`. The passing slugs (`shbiro-2468`, `levi-55`) follow the URL word law; an "einstein" slug needs Ben's explicit exception.
- **Single-owner words this batch would claim:** `brodetsky`, `reading`, `amichai`, `stern`. Other radius projects on those streets would need another head word, or these pages become the street pages that hold them.
- **EcoCity:** both EcoCity rows (Manya veIsrael 9 and 11) were skipped entirely.

## DataForSEO spend
30 requests to `/v3/serp/google/organic/live/advanced` (Israel, Hebrew, desktop, async AI Overview on, PAA click depth 1): 26 succeeded on the first try; 4 returned "Internal SE Server Error" and were re-run once. Cost reported by the API: **$0.096 in total** ($0.088 for the 26 stored results + $0.008 for the 4 failed attempts). Budget was about 30 calls: kept.

## Method notes
- Competitor pages were read with WebFetch on 1.11.2026; the PDF brochure of Philharmonit was read from its text layer. Dates in the fact sheets are the source's own date; "read 1.11.2026" means the page carries no date.
- URL audit: the live sitemap (4,634 URLs) was snapshotted once at 16:15 UTC and `url_word_audit.py --csv <snapshot> --token <word>` was run per token, the same logic as the live run without fetching the sitemaps 50 times.
- Nothing was estimated. Empty cells mean no source read today published the fact.
