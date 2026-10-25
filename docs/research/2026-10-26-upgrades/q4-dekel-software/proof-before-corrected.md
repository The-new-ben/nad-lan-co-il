# Depth baseline, corrected recount (25.10.2026)

Same metrics as tools/depth_proof.py, computed on the raw HTML saved in `C:/Users/777/nad-lan/_private-research/2026-10-26-upgrades/raw/q4/`, with one fix: when the main or article element holds under 300 words (themes that wrap only a related-posts card), the whole body minus header, footer, nav and aside is counted. proof-before.md in this folder is the unmodified tool output.

| page | words | figures | tables | cells | tools | faq | headings | visuals | sources | schema | updated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ours | 808 | 21 | 1 | 12 | 0 | 0 | 11 | 0 | 0 | DefinedTerm,DefinedTermSet,WebPage |  |
| dekel-cloud | 1005 | 0 | 0 | 0 | 0 | 7 | 22 | 1 | 0 | ContactPoint,OfferCatalog,PostalAddress,Service |  |
| contechradar | 404 | 6 | 0 | 0 | 0 | 0 | 8 | 0 | 0 | BreadcrumbList,SoftwareApplication |  |
| dekel-faq | 815 | 10 | 0 | 0 | 0 | 22 | 23 | 0 | 0 | ContactPoint,OfferCatalog,PostalAddress,Service |  |
| dekel-bids | 487 | 15 | 0 | 0 | 0 | 0 | 9 | 15 | 0 | ContactPoint,OfferCatalog,PostalAddress,Service |  |
| civileng | 542 | 57 | 0 | 0 | 0 | 0 | 2 | 9 | 1 |  |  |
| wikipedia | 318 | 23 | 0 | 0 | 0 | 0 | 2 | 1 | 0 | Article | 2026-02-04 |

Competitor maxima: words 1005 (dekel-cloud); figures 57 (civileng); tables 0 (wikipedia); cells 0 (wikipedia); tools 0 (wikipedia); faq 22 (dekel-faq); headings 23 (dekel-faq); visuals 15 (dekel-bids); sources 1 (civileng)
