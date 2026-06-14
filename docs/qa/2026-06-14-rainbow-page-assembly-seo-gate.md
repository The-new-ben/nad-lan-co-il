# Rainbow Page Assembly And SEO Gate

Scope: public Rainbow project page, post id `4464`, slug `rainbow-tel-aviv`.

This gate checks the part of the flagship showroom that is not solved by the GLB alone: the page must
read as a premium, indexable project page with transactional buyer language, visible guide assembly,
schema output, FAQ output and no public rendering leaks.

## Command

```powershell
python scripts\check-rainbow-page-assembly.py
python scripts\check-rainbow-page-assembly.py --strict
```

Default mode reports without failing. `--strict` exits non-zero when the page is not ready for final
showroom release.

## Current Live Result

Checked against `https://nad-lan.co.il/projects/rainbow-tel-aviv/` on 2026-06-14.

Passing:

- One visible H1: `Rainbow Tel Aviv – ריינבו תל אביב`.
- Visible content depth: `3,783` words.
- `nadlan-guide` / `nadlan-rainbow-seo-v1610-start` block is present.
- Healthcheck reports `project_page_assembly.loaded=true`, `rainbow_seed=true`, `faq_meta=true`, `price_meta=true`.
- JSON-LD types include `ApartmentComplex`, `FAQPage` and `BreadcrumbList`.
- Apartment schema has `10` amenity features, `3` reference links and an `AggregateOffer`.
- FAQ schema has `6` questions.
- No mojibake, no raw code leak and no visible PHP/JS error text detected by this checker.

Current strict blockers:

- `למכירה` appears `2` times; target is `3+`.
- The public title is still experience-led: `Rainbow Tel Aviv - ריינבו תל אביב | בחירת דירות, מבט מהדירה ושדה דב | נדלן חכם`.
- The public meta description does not mention price.

## Required Fix Direction

Use the paste-ready title/meta direction from `docs/2026-06-12-rainbow-seo-dossier.md`:

- Title should lead with `דירות למכירה` / `מחירים` / `שדה דב`, not only the interactive experience.
- Meta description should mention price or prices with the non-binding framing.
- Add at least one natural, visible `למכירה` occurrence in the buyer-facing body or assembled guide block.

Do not add fake availability or binding prices. Keep the disclaimer that all price and availability data must be verified with the developer.

## v1.63.4 Patch Scope

The v1.63.4 SEO patch is intentionally narrow:

- Rainbow-only Yoast/document-title override now starts with `דירות למכירה` and includes `מחירים`.
- Rainbow-only meta description now mentions reported prices with a non-binding framing.
- A one-shot `nadlan_rainbow_seo_v1634` seed adds one natural visible buyer sentence with `דירות למכירה`.
- The seed also writes the Yoast title, meta description and focus phrase as editable post meta.
- Healthcheck exposes `project_page_assembly.rainbow_seo_v1634`, `title_override` and `description_override`.

Expected post-deploy result: after the owner pulls/syncs UPress Git, updates the plugin to `1.63.4`,
clears cache and hard-refreshes, `python scripts\check-rainbow-page-assembly.py --strict` should pass
for the three current blockers above.

## Final Gate

Before calling the Rainbow page SEO-ready:

```powershell
python scripts\check-rainbow-page-assembly.py --strict
```

must pass after the owner pulls/syncs UPress Git, updates the plugin/content path, clears cache and
hard-refreshes the page.

## Public-Copy Hardening

Follow-up gate on 2026-06-14 removed internal funnel wording from the public Rainbow assembly block.
The branch package now avoids `לידים`, `פאנל הלידים`, `WhatsApp`, CRM/routing/monetization language in
the rendered buyer-facing assembly text. The project page may still invite a structured inquiry, but it
must not describe the operator system behind that inquiry.

Package proof:

```powershell
tar -xOf plugin-dist\nadlan-config-1.63.4.zip nadlan-config/inc/project-page-assembly.php |
  Select-String -Pattern 'לידים|פאנל הלידים|WhatsApp|CRM|lead routing|monetization|paid placement' -CaseSensitive:$false
```

Expected result: no matches.
