# Risk Register

| Risk | Severity | Evidence | Mitigation | Owner |
|---|---:|---|---|---|
| Fake facade damages trust | High | Dimri concept/fake-grid conflict history | official/concept/missing states; no fake grid | showroom |
| Silent fallback hides real failures | High | previous legacy facade/model resurrection | visible error states only | engineering |
| Plugin does too much presentation | High | repeated plugin deploy/firefights | move layout/CSS to theme when safe | architecture |
| Theme merge not live until UPress pull | High | documented M10 | label THEME deploy path | release |
| Keyword cannibalization | High | Sde Dov/project overlap | canonical registry | SEO |
| Legal/tax inaccuracies | High | purchase tax/price claims | `LEGAL_REVIEW`, source/date | legal |
| Public internal leakage | High | Woo/debug/pattern leakage history | trust QA gate | QA |
| Real inventory not available | Medium | listings not mature | draft/noindex until real | listings |
| Official BIM/facade missing | Medium | Dimri/Rainbow placeholder history | concept label or missing state | owner/contractor |
| Mapbox cost/API/token failures | Medium | recurring map failures | lazy load, visible error, token monitoring | engineering |
| I18N thin duplication | Medium | multi-language request | localized pages + hreflang | i18n |
| Performance bloat from 3D/media | Medium | GLB/image costs | posters, compression, lazy load | performance |
| Lead lost to WhatsApp | High | owner identified revenue leak | context capture and webhook | CRM |
| Lovable hidden memory | Medium | external project link | copy output into repo | agents |
| Agent drift / stale branches | High | previous incidents | COORDINATION + strategy OS | all agents |

## Escalation Rules

- Missing official asset: mark `REQUIRES_OFFICIAL_ASSET`.
- Legal/tax/pricing uncertainty: mark `LEGAL_REVIEW`.
- Search metric uncertainty: mark `NEEDS_VERIFICATION`.
- Deployment mismatch: stop new feature work and deploy/verify first.
- Product code request inside strategy branch: create new branch/slice, do not mix.
