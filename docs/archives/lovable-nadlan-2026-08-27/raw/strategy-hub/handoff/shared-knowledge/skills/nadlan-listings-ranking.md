---
name: nadlan-listings-ranking
description: Deterministic Nadlan3D listings ranking — paid tier first, then asset completeness, engagement, freshness, locality. Paid placements must carry visible Featured/Sponsored/Promoted labels. Same algorithm runs in Lovable client-side and in WordPress.
type: feature
---

# Nadlan3D — listings ranking hierarchy

The ordering rule applied wherever projects are listed: `/listings`, `/cities/$city`, homepage featured strip, future war-room console.

## Order (highest signal wins; ties cascade)

1. **Paid tier** — `featured > promoted > standard`. Always wins ties.
2. **Asset completeness** — float `0..1`, share of `(glb, plan, photos, price, rooms)` present. Higher first.
3. **Engagement** — float `0..1`, CTR proxy (mock in prototype). Higher first.
4. **Freshness** — `updated_at` ISO timestamp, newer first.
5. **Locality boost** — float `0..1`, city affinity. Higher first.

## Reference implementation (Lovable)

`src/lib/projects.mock.ts → rankProjects()`:

```ts
const tierWeight = { featured: 3, promoted: 2, standard: 1 };

export function rankProjects(input: Project[]): Project[] {
  return [...input].sort((a, b) => {
    if (tierWeight[a.paid_tier] !== tierWeight[b.paid_tier])
      return tierWeight[b.paid_tier] - tierWeight[a.paid_tier];
    if (a.completeness !== b.completeness) return b.completeness - a.completeness;
    if (a.engagement !== b.engagement) return b.engagement - a.engagement;
    const at = new Date(a.updated_at).getTime();
    const bt = new Date(b.updated_at).getTime();
    if (at !== bt) return bt - at;
    return b.city_boost - a.city_boost;
  });
}
```

## Transparency labels (mandatory)

Every paid placement is **always** labelled. No invisible promotion.

| `paid_tier`  | Card chip          | Extra chip        | Rationale                          |
|--------------|--------------------|-------------------|------------------------------------|
| `featured`   | `Featured` (accent)| `Sponsored`       | Top-of-fold, requires double label |
| `promoted`   | `Promoted` (ink)   | `Sponsored`       | Mid-grid placement                 |
| `standard`   | `סטנדרט` (muted)   | none              | Organic position                   |

The listings page also renders a standing transparency note explaining the order — both languages — at the bottom of the grid.

## Port to WordPress

- DB field `paid_tier` (enum `featured|promoted|standard`)
- DB fields `completeness numeric(3,2)`, `engagement numeric(3,2)`, `updated_at timestamp`, `city_boost numeric(3,2)`
- Same sort runs in SQL with explicit `ORDER BY` matching the cascade above, **or** in PHP after fetching — but the labels MUST be added in markup, not optional

## Anti-patterns

- Hiding `paid_tier` from the DOM
- Pushing paid placements above the fold without the `Sponsored` chip
- Tuning a hidden engagement multiplier so a paid listing looks organic

