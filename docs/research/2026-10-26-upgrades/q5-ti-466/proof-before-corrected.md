# Depth baseline, corrected recount (25.10.2026)

Same metrics as tools/depth_proof.py, computed on the raw HTML saved in `C:/Users/777/nad-lan/_private-research/2026-10-26-upgrades/raw/q5/`, with one fix: when the main or article element holds under 300 words (themes that wrap only a related-posts card), the whole body minus header, footer, nav and aside is counted. proof-before.md in this folder is the unmodified tool output.

| page | words | figures | tables | cells | tools | faq | headings | visuals | sources | schema | updated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ours | 823 | 39 | 0 | 0 | 0 | 6 | 11 | 0 | 0 | BreadcrumbList,DefinedTerm,DefinedTermSet,FAQPage,WebPage |  |
| sii-466-2 | 330 | 30 | 7 | 45 | 0 | 0 | 7 | 0 | 0 |  |  |
| civileng-revision | 555 | 50 | 0 | 0 | 1 | 0 | 2 | 21 | 0 |  |  |
| konstruktor-466-2 | 248 | 6 | 0 | 0 | 0 | 2 | 8 | 9 | 0 | Article,BreadcrumbList,FAQPage,WebPage | 2026-10-05 |
| yam-binyan | 1261 | 69 | 1 | 28 | 0 | 8 | 27 | 1 | 0 | Article,BreadcrumbList,ContactPoint,Country,FAQPage,GeoCoordinates,LocalBusiness,OfferCatalog,OpeningHoursSpecification,PostalAddress,SpeakableSpecification,Thing,WebPage | 2026-07-17 |
| shlomi-atun | 1891 | 26 | 0 | 0 | 0 | 5 | 9 | 1 | 0 | Article,BreadcrumbList,CommentAction,Country,FAQPage,Person,PostalAddress,WebPage | 2026-09-10 |
| aace | 1533 | 116 | 1 | 36 | 0 | 4 | 25 | 0 | 0 | Article,BreadcrumbList,Person,WebPage | 2026-07-11 |
| barzel-kisuy | 514 | 29 | 1 | 36 | 0 | 5 | 11 | 14 | 0 | Article,BreadcrumbList,FAQPage,Person,WebPage | 2026-05-04 |

Competitor maxima: words 1891 (shlomi-atun); figures 116 (aace); tables 7 (sii-466-2); cells 45 (sii-466-2); tools 1 (civileng-revision); faq 8 (yam-binyan); headings 27 (yam-binyan); visuals 21 (civileng-revision); sources 0 (yam-binyan)
