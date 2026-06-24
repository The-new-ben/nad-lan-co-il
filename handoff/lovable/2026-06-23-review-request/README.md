# Lovable review request — showroom 1.69.1 → 1.69.32

> For Lovable. The owner asked you to review the work. This repo is public, so you
> need no special access. Everything below is verified against the live site and
> the code on `main`, not assumed.

## What to open first

Public compare link (no login needed), 59 commits since the last clean review point
(1.69.1, the #215 cream-skin merge):

`https://github.com/The-new-ben/nad-lan-co-il/compare/b25ff8a...d5306af`

## State of the deployment

- Live plugin version: **1.69.32** (healthcheck `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck`).
- The cream skin you specified IS live and correct (background, ink, gold, hairlines).
- Projects are indexable again (the thin-content noindex guard was removed for `nadlan_project`).

## The blocking defect (confirmed on live and in `main`)

**Buyers cannot select an apartment on the model.** The 6 apartment hotspot buttons
exist in the HTML and the JavaScript click handlers are wired correctly, but a CSS
rule hides them:

- File: `plugins/nadlan-config/inc/project-3d.php`
- Function: `nadlan_p3d_lovable_showroom_v1690_css()` (the cream-skin CSS block)
- Lines ~2247-2249:

```css
.nlp3d.nlp3d-premium .nlp3d-mv-hotspot{
  display:none!important;
}
```

This rule sits inside the cream-skin port. It makes every apartment hotspot invisible,
so there is nothing for a buyer to click on the model. The fix is to remove this
rule (and give the hotspots a visible, on-brand treatment), not to add a new layer
on top of it. The owner's standing rule is replace at the source, never stack.

## Important context for your review

The 59 commits from 1.69.2 to 1.69.32 were pushed straight to `main` with no PR and
no real visual QA. The screenshot "proof" committed across those releases is not
trustworthy: multiple "before" and "after" PNGs are byte-identical (same SHA256),
i.e. the same image reused, not real captures. Treat the commit messages claiming
"apartment selection works" as unverified. The live behavior is the defect above.

## What we would like from you

1. Confirm the hotspot treatment you intend for the cream skin (size, color, label,
   hover/active states) so the fix restores selectable, on-brand apartment markers
   rather than just deleting the hide rule.
2. Flag anything else in the 1.69.x range that drifted from your design system.

## Verification note (honesty)

This brief was produced without a live browser session (the environment blocks
browser traffic through the proxy). It is based on: the live page HTML pulled with
curl, the CSS rule located in both the served page and the `main` source and the
1.69.32 release ZIP, and SHA256 comparison of the committed QA screenshots. The
`display:none` rule and the duplicated screenshots are facts, not estimates.
