# International And I18N Strategy

Purpose: make NadLan useful for foreign buyers without creating low-quality machine-translated duplicates.

## Target Languages

1. Hebrew - canonical market language.
2. English - broad foreign buyer/investor language.
3. French - important for French-speaking buyers and lawyers.
4. Russian - important for Russian-speaking buyers/investors.
5. Arabic - regional/local accessibility and possible future markets.

## URL Strategy

Preferred:
- `/en/...`
- `/fr/...`
- `/ru/...`
- `/ar/...`

Each translated page needs:
- hreflang.
- self-canonical in that language.
- language-specific title/meta.
- local currency/legal notes.
- native CTA copy.

Do not publish raw automatic translations as indexable pages.

## Foreign Buyer Page Types

| Page | Language priority | Notes |
|---|---|---|
| Israel real estate guide | EN/FR/RU/AR | broad entry |
| Tel Aviv new developments | EN/FR/RU | high commercial value |
| Sde Dov district | EN/FR/RU | project/investor |
| Rainbow project | EN/FR/RU | project page |
| Dimri Yama project | EN/FR/RU | project page |
| Purchase tax foreign buyer | EN/FR/RU/AR | legal review required |
| Lawyer services | EN/FR/RU/AR | owner E-E-A-T |

## Content Differences By Language

English:
- explain Israel purchase process, tax, escrow, lawyer, financing.

French:
- emphasize French-speaking legal support and tax clarity.

Russian:
- practical transaction, banking, residency/tax disclaimers.

Arabic:
- accessibility, local navigation, legal clarity.

## Translation Workflow

1. Hebrew source page approved.
2. Extract facts table and source citations.
3. Create language-specific outline.
4. Translate/adapt.
5. Native QA where possible.
6. Add hreflang.
7. Visual screenshot in RTL/LTR.

## Risks

- Duplicate content if pages are direct translations with no localized value.
- Legal inaccuracies.
- Wrong currency/tax assumptions.
- Broken RTL/LTR layout.

## Acceptance Criteria

- No page goes live without hreflang/canonical.
- No legal/tax page goes live without `LEGAL_REVIEW`.
- CTAs route to language-aware contact path.
- Screenshots at 390/768/1440 for both RTL and LTR layouts.
