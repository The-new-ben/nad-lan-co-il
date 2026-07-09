# Rainbow 1.72.69 Live Polish Gate

## Scope

This is a three-line visual hotfix on top of the live 1.72.68 buyer showroom. It does not add a
renderer, rewrite project content, change inventory, remove the project progress tracker, or alter
the lead and RFP pipeline.

## Defects Reproduced On Live 1.72.68

- The theme heading rule overrode the showroom title color, producing black text on the dark stage.
- At 390px with an apartment selected, the first-party accessibility launcher intersected the
  apartment detail tabs.
- The composed Rainbow model was visually overexposed against the showroom background.

## Fix

- Scope an explicit cream heading color to `.nl-app .nl-theater__title h2`.
- Move the accessibility launcher to the opposite inline edge only while the mobile apartment
  drawer is open, and retain a 44 by 44 pixel target.
- Use exposure `0.82` only for composed projects; all other engine projects retain `1.02`.

## Anti-Stack Statement

- `#nl-root` must equal 1.
- `.nlv2-showroom` must equal 0.
- Project breadcrumb, H1, progress tracker, price, map, inquiry, and article must each render once.
- No old renderer, stylesheet, or duplicate public module is introduced by this release.

## Live Interaction Gate

- Model loads, rotates horizontally, and switches to the facade.
- A model apartment and an inventory apartment both select and open the same detail drawer.
- Plan, live view, tour, save, compare, RFP, studio, contact, WhatsApp, share, and brochure controls
  are present and navigable.
- The live form is exercised up to, but not through, submission to avoid creating a fake production
  lead. A labeled QA lead requires explicit confirmation before submission.
- HE, EN, FR, RU, and AR sibling pages use the correct `lang`, `dir`, and public labels.
- Desktop 1440 and mobile 390 have no horizontal overflow or control overlap.
- Healthcheck and all version surfaces must report `1.72.69`.

## Post-Deploy Evidence

- PR `#458` merged to `main` at `141f6ed`.
- WordPress installed the release with overwrite enabled and kept the plugin active.
- Public healthcheck reports `1.72.69`.
- The temporary admin-only deploy snippet was deleted; its route returns HTTP 404.
- All five Rainbow language URLs return HTTP 200 with correct server-rendered `lang`, `dir`, and
  six alternate-language links including x-default.
- Live CSS and JS are served with `ver=1.72.69` and contain all three hotfix markers.
- The packaged Rainbow model returns HTTP 200 at 851,668 bytes; sampled 3, 4, and 5 room plans
  also return HTTP 200.

The final post-deploy visual gate is not marked complete. Chrome control stopped responding after
the deploy even though the Codex Chrome Extension and native-host checks passed. The extensive
live 1.72.68 interaction pass remains valid for the unchanged buyer functions, but 1.72.69 still
needs fresh Chrome screenshots confirming title contrast, model exposure, and mobile non-overlap.
Do not represent those three visual checks as completed until that connection is restored.

## Competitive Product Gaps To Keep Visible

- Official developer BIM or apartment-level geometry is still missing. The current model is an
  illustrative prototype and must not be represented as official architecture.
- Verified live inventory, price lists, payment plans, and handover date are missing. The page must
  continue to show ranges and non-binding language rather than inventing data.
- Official plans, photography, video, and 360 tours are the largest remaining content gap versus
  leading new-construction portals.
- The repository is private, so the public raw GitHub update URL does not serve the ZIP. The current
  production deploy uses a short-lived authenticated asset URL and deletes the deploy route after
  installation. A durable private release channel remains a separate platform task.

