# Source Manifest

## Run identity

| Field | Value |
| --- | --- |
| Date | 2026-07-21 |
| Agent | Codex |
| Repository | `https://github.com/The-new-ben/nad-lan-co-il` |
| Base branch | `origin/main` |
| Base commit | `f16ca096b67a2e2077c7479c4e2e8ef33819b8eb` |
| Review branch | `agent/portal-homepage-recipe-2026-07-21` |
| Public site | `https://nad-lan.co.il/` |
| Languages in scope | Hebrew and English; future-ready for French/Russian/Arabic |
| Mutation scope | Documentation, review HTML and screenshot evidence only |
| Explicitly excluded | WordPress edits, REST writes, application passwords, theme/plugin/templates, deploy, merge |

## Read order used

1. Repository root instructions: `AGENTS.md`, `COORDINATION.md`, `BACKLOG.md`, `skills/MAP.md`.
2. Current site state and access/deploy guidance under `skills/`.
3. Honesty, copywriting, RTL, luxury design, screenshot QA and 3D showroom rules.
4. Latest Lovable design source and reports under `handoff/lovable/` and `docs/`.
5. Existing WordPress block theme, `theme.json`, `templates/`, `parts/`, `patterns/`.
6. `plugins/nadlan-config/` CPT, taxonomy, REST, directory, media, compare, favorites, saved search, lead and showroom contracts.
7. Existing project asset packages and `source-notes.md` files.
8. Paid Semrush research dated 2026-06-22, treated as dated directional evidence rather than live fact.
9. Live competitor pages listed in `research/sources.md`, observed on 2026-07-21.
10. Official WordPress, W3C and web.dev guidance listed in `research/sources.md`.

## Existing repository capabilities that the specification reuses

| Capability | Existing owner |
| --- | --- |
| Projects/properties/professionals | `nadlan_project`, `nadlan_property`, `nadlan_professional` CPTs |
| Geography | `nadlan_city`, `nadlan_compound`; `lat`/`lng` meta |
| Project catalog | `/wp-json/nadlan/v1/projects` and directory renderer |
| Map and nearby | `/map`, `/near`, `/project-map` endpoints |
| Save/compare | `/favorite`, `/saved-search`, `/compare` |
| Leads and concierge | `/lead`, `/concierge`, `/concierge-lead`, WhatsApp ingestion |
| Developer ownership | claim flow, `claim_status`, `owner_user_id`, Studio routes |
| Media | featured media, `photos_csv`, video/tour/floorplan fields, Studio upload/reorder |
| 3D | `project_3d_*` fields and protected project-showroom REST route |
| Internationalization | i18n endpoint plus language-linked content conventions |
| Search | `/suggest`, `/nl-search`, directory facets |
| Trust/provenance | `source`, `source_url`, `source_id`, `verified_at`, `data_quality`, `is_demo` |

## Research coverage

- 39 named portal/brand benchmarks.
- Israeli consumer portals, Israeli foreign-buyer specialists and Israeli developer acquisition products.
- Global mass-market, new-development, regional off-plan and luxury portals.
- Homepage, results/card, map/filter, project/detail, mobile and advertiser/developer patterns.
- Official platform guidance for WordPress data exposure/revisions, accessibility and performance.

This is a pattern corpus, not a statistically representative market study. Counts and freshness labels on third-party sites change continuously; observations are dated.

## Asset inventory used in review previews

| Review asset | Repository source | State | Public-use rule |
| --- | --- | --- | --- |
| Coastal skyline | `assets/premium-site/tel-aviv-coast-skyline.jpg` | Generated concept | Review only; label illustrative |
| Architectural model | `assets/premium-site/architectural-model.jpg` | Generated concept | Review only; never imply official model |
| Sea-view interior | `assets/premium-site/sea-view-interior.jpg` | Generated concept | Review only; never imply actual unit |
| Ashira hero | `assets/projects/ashira-sde-dov/ashira-hero-concept.jpg` | Original generated project concept | Review only; source notes explicitly say not official |
| Rainbow showroom hero | `assets/projects/rainbow-tel-aviv/rainbow-showroom-hero-v1664.jpg` | Prototype/generative showroom image | Review only; not official Rainbow BIM/render/inventory |
| Dimri poster | `assets/projects/dimri-yama/poster-prototype.png` | Prototype poster | Review only; not official media or sale facts |
| Interior living room | `assets/showroom-assets/interior_living_room_1782908165373.jpg` | Generated showroom concept | Review only; label illustrative |

The preview copies these files into its own `assets/` folder for portability. Their origin and status remain governed by the original `source-notes.md` files.

## Missing owner/developer inputs

- Written permission for each official photo, rendering, logo, plan and brochure.
- Project-by-project approved hero and gallery set.
- Current unit types, availability policy, price wording and verification cadence.
- Approved developer identity, project sales contact and escalation owner.
- English commercial/legal review; French/Russian/Arabic priorities if included.
- Official BIM/GLB/IFC or facade/unit geometry for exact window-level selection.
- Approved floor/site plans and document visibility policy.
- Consent, lead routing, response-time and retention policy.
- Confirmed public badges and the evidence that makes each badge true.

## Output contract

The package contains research, decisions, specifications, five static review pages and screenshot QA. It deliberately contains no edits to production WordPress code or data.
