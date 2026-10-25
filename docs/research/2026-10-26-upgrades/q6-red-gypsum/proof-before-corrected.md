# Depth baseline, corrected recount (25.10.2026)

Same metrics as tools/depth_proof.py, computed on the raw HTML saved in `C:/Users/777/nad-lan/_private-research/2026-10-26-upgrades/raw/q6/`, with one fix: when the main or article element holds under 300 words (themes that wrap only a related-posts card), the whole body minus header, footer, nav and aside is counted. proof-before.md in this folder is the unmodified tool output.

| page | words | figures | tables | cells | tools | faq | headings | visuals | sources | schema | updated |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ours | 739 | 34 | 0 | 0 | 0 | 0 | 12 | 0 | 0 | DefinedTerm,DefinedTermSet,WebPage |  |
| mh-types | 407 | 3 | 0 | 0 | 0 | 0 | 7 | 1 | 0 | BlogPosting,BreadcrumbList,Person,WebPage | 2024-07-21 |
| my-gypsum | 1224 | 34 | 1 | 35 | 0 | 4 | 21 | 4 | 0 | BreadcrumbList,Country,FAQPage,OfferCatalog,Person,PostalAddress,Service,WebPage | 2026-09-30 |
| d4design | 284 | 3 | 0 | 0 | 0 | 1 | 3 | 7 | 0 | BreadcrumbList,ContactPoint,Country,WebPage |  |
| midrag-25353 | 278 | 30 | 0 | 0 | 0 | 1 | 2 | 40 | 0 | QAPage |  |
| golmat | 458 | 6 | 0 | 0 | 0 | 0 | 12 | 7 | 0 | Article,BreadcrumbList,CommentAction,Person,WebPage | 2026-08-09 |
| rotenberg-fire-walls | 752 | 73 | 11 | 76 | 0 | 0 | 2 | 10 | 0 |  |  |
| nor-rahamim | 492 | 7 | 1 | 10 | 0 | 3 | 11 | 0 | 0 | Article,BreadcrumbList,City,ContactPoint,Country,GeoCircle,GeoCoordinates,MerchantReturnPolicy,OpeningHoursSpecification,Place,PostalAddress,WebPage | 2026-10-17 |
| tambour-boards | 1542 | 32 | 0 | 0 | 0 | 0 | 38 | 168 | 0 | BreadcrumbList,WebPage | 2026-07-27 |
| mh-orange | 328 | 0 | 0 | 0 | 0 | 2 | 10 | 4 | 0 | BlogPosting,BreadcrumbList,Person,WebPage | 2019-09-18 |

Competitor maxima: words 1542 (tambour-boards); figures 73 (rotenberg-fire-walls); tables 11 (rotenberg-fire-walls); cells 76 (rotenberg-fire-walls); tools 0 (tambour-boards); faq 4 (my-gypsum); headings 38 (tambour-boards); visuals 168 (tambour-boards); sources 0 (tambour-boards)
