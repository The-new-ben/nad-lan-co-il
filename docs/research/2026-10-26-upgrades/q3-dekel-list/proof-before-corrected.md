# Depth baseline, corrected recount (25.10.2026)

Same metrics as tools/depth_proof.py, computed on the raw HTML saved in `C:/Users/777/nad-lan/_private-research/2026-10-26-upgrades/raw/q3/`, with one fix: when the main or article element holds under 300 words (themes that wrap only a related-posts card), the whole body minus header, footer, nav and aside is counted. proof-before.md in this folder is the unmodified tool output.

| page | words | figures | tables | cells | tools | faq | headings | visuals | sources | schema | updated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ours | 785 | 24 | 0 | 0 | 0 | 6 | 11 | 0 | 0 | BreadcrumbList,DefinedTerm,DefinedTermSet,FAQPage,WebPage |  |
| dekel-bniya | 596 | 4 | 0 | 0 | 0 | 5 | 18 | 3 | 0 | ContactPoint,OfferCatalog,PostalAddress,Service |  |
| wikipedia | 318 | 23 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | Article | 2026-02-04 |
| purenadlan | 1763 | 0 | 3 | 48 | 1 | 6 | 26 | 28 | 0 | BlogPosting,FAQPage,Person,WebPage | 2026-08-05 |
| sharonbenzvi | 1884 | 4 | 2 | 33 | 0 | 12 | 36 | 34 | 0 | Article,BreadcrumbList,Person,WebPage | 2026-01-07 |
| civileng | 542 | 57 | 0 | 0 | 0 | 0 | 2 | 9 | 1 |  |  |
| top-renovations-harisa | 698 | 47 | 3 | 34 | 2 | 0 | 8 | 0 | 0 | AggregateRating,ContactPoint,LocalBusiness,Person,Rating,Review |  |
| hdekel | 403 | 48 | 1 | 75 | 0 | 0 | 2 | 1 | 0 | BreadcrumbList,WebPage | 2024-10-29 |

Competitor maxima: words 1884 (sharonbenzvi); figures 57 (civileng); tables 3 (top-renovations-harisa); cells 75 (hdekel); tools 2 (top-renovations-harisa); faq 12 (sharonbenzvi); headings 36 (sharonbenzvi); visuals 34 (sharonbenzvi); sources 1 (civileng)
