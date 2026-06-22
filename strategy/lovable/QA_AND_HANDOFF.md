# Lovable QA And Handoff

## What To Capture From Lovable

For every generated screen:

1. Screenshot at desktop 1440.
2. Screenshot at tablet 768.
3. Screenshot at mobile 390.
4. Notes on broken/overlapping elements.
5. Exported source/code if Lovable is connected to GitHub.
6. Prompt used and date.

Save outputs under:

`docs/design/lovable/<date-or-run>/`

or, for screenshots:

`docs/qa/screenshots/lovable-<run>/`

## QA Checklist

- [ ] no fake facade.
- [ ] no fake listing inventory.
- [ ] no silent fallback.
- [ ] no dead buttons.
- [ ] no public internal copy.
- [ ] official/concept/missing labels visible.
- [ ] no horizontal overflow at 390.
- [ ] headings above paragraphs.
- [ ] 44px tap targets on mobile.
- [ ] model and picker do not overlap.
- [ ] selected unit card is dismissible.
- [ ] map/tour missing states visible.
- [ ] design tokens match strategy.
- [ ] Heebo + IBM Plex Mono used.

## How Lovable Output Becomes Real Work

Lovable output is not production by itself. Convert it to repo work:

1. Pick one screen/component from the gallery.
2. Write a small implementation PR.
3. Declare deploy path: THEME, PLUGIN, CONTENT, or NONE.
4. Commit screenshots before/after.
5. Run relevant gates from `strategy/12-qa-gates.md`.
6. Only then merge/deploy.

## GitHub/Lovable Sync Rule

Lovable documentation says GitHub integration can back up and sync code. If used:

- connect only a safe branch, not production main directly.
- review every diff before merge.
- do not accept generated secrets/config.
- do not let Lovable overwrite plugin/theme release files without review.

## If Lovable Is Not Accessible

If Chrome/Lovable fails, do not stop:

1. Use `LOVABLE_MASTER_PROMPT.md` as the source prompt.
2. Use `SCREEN_MATRIX.csv` as the acceptance matrix.
3. Ask the owner to paste the master prompt into Lovable if manual access is needed.
4. Continue repo-side planning or implementation from the same matrix.

## Definition Of Done

The Lovable phase is done when:

- the 15-screen gallery exists or Lovable failure is documented;
- screenshots are committed;
- the best screens are mapped to implementation slices;
- no hidden Lovable-only decision remains outside the repo.
