# Anti-Stack Release Rules

These rules are mandatory for the rebuild.

## 1. One Renderer Per Surface

For a project page:

- exactly one project showroom root,
- no old `.nlv2-showroom` static block,
- no old `.nlp3d` procedural module rendered beside the new engine,
- no duplicate selected-apartment cards,
- no duplicate language switchers.

Each PR must include a browser or script proof for the target page:

- `.nlv2-showroom = 0`
- `.nlp3d = 0` unless intentionally keeping the old module on a legacy page
- `#nl-root = 1` for the current showroom engine page

## 2. Theme Rebuild Is Side By Side

Do not overwrite the current production theme in place as the first step.

Safe sequence:

1. snapshot current theme/root files,
2. build new theme/design system in a clean branch or new theme folder,
3. wire the existing plugin data into new templates,
4. QA screenshots,
5. activate/swap only when green.

## 3. Remove Before Replace

When replacing a visual layer:

- identify the old renderer/CSS selector,
- disable it in the same change,
- prove the old selector is absent,
- only then accept the new visual layer.

No "temporary" double rendering on public pages.

## 4. Public Language Gate

Buyer pages must not contain:

- GLB,
- BIM,
- SVG,
- mesh,
- hotspot,
- polygon,
- funnel,
- lead,
- CRM,
- token,
- Codex,
- Lovable,
- Sponsored,
- internal implementation language.

Technical terms may appear in owner manuals and developer docs only.

## 5. Visual QA Gate

Each meaningful visual change must produce screenshots:

- desktop 1440,
- tablet around 768,
- mobile 390,
- Hebrew RTL,
- English LTR where applicable.

Screenshots must show:

- no horizontal overflow,
- no element overlap,
- article headings aligned with the text column,
- one visible H1,
- header/footer intact,
- forms/buttons not covered,
- mobile selector usable.

## 6. SEO Gate

Each important page must have:

- one H1,
- source-backed first paragraph,
- relevant H2/H3 structure,
- visible buyer content, not only a widget,
- title/meta strategy,
- schema where supported,
- internal links to area/project/tools/professional pages,
- no invented single prices.

Estimates must be ranges, dated, sourced, and labelled non-binding.

## 7. Release Gate

No release is complete until:

- files are committed,
- `git show --stat HEAD` lists the intended files,
- ZIP/manifest/version surfaces align when the plugin is touched,
- healthcheck reports the shipped plugin version when plugin changed,
- browser screenshots prove the public page changed.

## 8. No Giant Mixed PR

Do not mix:

- new theme shell,
- language routing,
- project showroom logic,
- content rewrite,
- lead flow,
- server deploy,
- asset pipeline,

all in one release. Build the rebuild in layers. The final site can be big; each release must be
small enough to verify.
