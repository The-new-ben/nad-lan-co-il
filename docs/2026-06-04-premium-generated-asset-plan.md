# Premium generated asset plan

Date: 2026-06-04
Scope: docs-only asset plan for replacing cheap icons, empty states, and missing listing media. No files are uploaded to WordPress by this PR.

## Decision

Do not generate decorative random imagery just to add "premium." For micro UI, the correct asset is usually an icon, not a bitmap. Generated bitmap assets are useful only when a listing, profile, or empty state has no legal media.

## Required asset families

| Asset family | Format | Where used | Notes |
| --- | --- | --- | --- |
| Category icon set | Inline SVG or Lucide icons | `.nldir-pill`, `.nldc-av`, metadata rows, Studio controls | 1.5px stroke, no emoji, no filled cartoon icons. |
| Project fallback hero | SVG plus optional generated WebP/PNG | Project/property cards and single heroes with no legal photos | Abstract Tel Aviv/architecture composition, paper/ink/gold palette, marked illustrative if displayed as hero. |
| Professional monogram | SVG/CSS generated | Professional card/profile when no logo/headshot | Initials, thin border, soft paper fill, no random avatar faces. |
| Sponsored placement visual | SVG/CSS | `.nldc-sponsored-spot`, advertiser upsell cards | Small spotlight/megaphone line icon plus premium editorial background. No dashed coupon look. |
| Empty search state | SVG | `.nldir-empty`, no reviews, no gallery, no owned cards | One calm line illustration plus one next action. |
| Upload/dropzone visual | SVG | `.nlst-dropzone` | Upload/cloud/image icon, supported formats and quality hint. |
| Trust icon set | SVG | verified, registry/license, paid tier, data.gov.il source, claim ownership | Must support text labels. Icon alone is not enough. |

## Generation prompts

Use these prompts only for assets that need generated fallback media. Prefer SVG for icons and simple line illustrations.

### Project fallback hero

```text
Create an original premium architectural illustration for an Israeli new-build real-estate project card. Abstract Tel Aviv coastal high-rise massing, clean facade rhythm, soft paper background, ink linework, muted gold highlights, no people, no logos, no text, no photorealistic claim, elegant editorial real-estate style, wide 16:10 composition.
```

### Professional monogram frame

```text
Create a minimal SVG-style monogram frame for a verified real-estate professional profile. White paper background, thin ink border, small gold corner rule, centered initials placeholder, no cartoon face, no emoji, luxury editorial identity system.
```

### Sponsored placement visual

```text
Create a restrained premium sponsored-placement illustration for a real-estate directory card. Thin gold spotlight line icon over warm paper, subtle architectural grid, no megaphone emoji, no loud ad style, no text, compact square composition.
```

### Empty search state

```text
Create a calm premium empty-state line illustration for a real-estate search directory. Minimal map pin, building outline, and search lens, ink and muted gold on paper, no cartoon, no text, no characters, simple SVG-friendly composition.
```

## Legal and quality rules

- Do not copy photos from Madlan, Yad2, Israel Canada, developers, brokerages, or portals.
- Generated listing media must be labelled illustrative where a user could confuse it for a real render/photo.
- If a real advertiser uploads legal images, real media overrides generated fallback.
- Avoid stock-like dark/blurred city photos. If using licensed imagery, show actual place/context clearly.
- Keep fallbacks visually quiet so real paid photography still feels like an upgrade.

## Implementation notes for Claude

- Put icon assets in one reusable layer rather than inline one-offs in every PHP renderer.
- Replace all emoji instances in public card/filter/studio UI with the icon layer.
- Preserve accessibility labels. Icons are decorative unless they communicate state, in which case text must accompany them.
- Confirm every generated or fallback asset is responsive: no layout shift, no crop of important visual content, and no accidental text inside images.
