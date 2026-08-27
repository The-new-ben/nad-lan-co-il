# NadLan Public Language Cleanup

Status: active

Date: 2026-06-23

Use this for every NadLan public page, listing, showroom, card, CTA, menu, badge, tooltip, and owner-visible design artifact.

## Rule

Public UI must speak like a premium real-estate product, not like an agent report, implementation note, design-system note, or SEO plan.

## Banned Or Internal In Public UI

Do not expose these terms on public pages:

- GLB
- SVG
- RTL
- 390px
- Frank Ruhl Libre
- Heebo
- Fraunces
- Inter Tight
- Featured / Sponsored / Promoted as a ranking taxonomy
- asset truth
- fallback
- mock
- placeholder
- AI generated unless the user must know the asset is illustrative
- money page
- war room
- KD
- schema
- canonical
- hreflang
- implementation

## Public Replacements

Use plain product language:

- `GLB` -> `מודל תלת-ממד`, `תצוגת תלת-ממד`, or `סיור תלת-ממד`
- `Showroom` -> `סיור בפרויקט`, `תצוגת הפרויקט`, or `סיור תלת-ממד`
- `facade fallback` -> `חזית להמחשה`, only when needed
- `empty asset state` -> `ממתין להעלאת חומרים מהיזם`
- `AI plan` -> `תכנית להמחשה בלבד`
- `RTL / 390px / font names` -> remove from public UI, or say `מותאם לעברית ולמובייל` only if it helps the buyer
- `Featured / Sponsored / Promoted` -> use one public disclosure label such as `ממומן`, `מודעה`, or `מקודם`, with a short transparency note outside the card if needed

English public pages may use `3D tour`, `Project tour`, `Ad`, `Sponsored`, or `Illustrative plan`, but not internal ranking mechanics.

## Copy Style

- Avoid em dashes in new public and owner-facing copy.
- Avoid AI-sounding filler and vague slogans.
- Do not say a model, plan, image, price, or view is real unless it is backed by a real asset.
- Prefer short, concrete buyer language.
- Hebrew public UI should be Hebrew-first. Use English only where the market already expects it or where it is part of the brand.

## Required Visual QA

Whenever this rule is applied:

1. Capture HE and EN screenshots after the change.
2. Save screenshots under the active handoff screenshots folder.
3. Write a visual QA note listing removed internal terms and remaining risks.
4. Do not mark done if internal terms still appear in first-viewport copy, project cards, badges, or CTA labels.

