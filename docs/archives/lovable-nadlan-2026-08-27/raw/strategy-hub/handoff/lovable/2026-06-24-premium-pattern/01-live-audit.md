# 01 Live Audit

## Truth that cannot be hidden

The live WordPress site is on plugin version 1.69.32 for the showroom selection behavior. The accepted proof says:

- Desktop marker taps select the matching authored unit.
- Mobile 390 marker taps select the matching authored unit.
- Raw surface tap near unit 16 now selects unit 16.
- Mobile scroll width remains 390.
- The proof does not prove exact per-window geometry picking.

## What was made wrong

### 1. The team patched behavior before locking the product pattern

The release history from 1.69.2 to 1.69.32 shows repeated changes around the same question: how does tapping the building select the right apartment? That means the interaction model was not specified clearly enough before implementation.

Correct product rule:

- If the project has only authored unit data, the UI must present apartment selection as an authored selection experience.
- If the project has exact apartment geometry, the UI may support exact building picking.
- The buyer-facing copy stays the same in both cases.

### 2. Visual skin was layered instead of replaced

The project archive and showroom gained cream styling, but the old active design still leaks through as a patched WordPress feeling. A premium system cannot be built by stacking more CSS over old CSS.

Correct engineering rule:

- Stop loading old active showroom skin on the target template.
- Emit new semantic classes.
- Load one premium stylesheet.
- Keep the working selection handler from 1.69.32 only as behavior.

### 3. The showroom is not visually centered as the product

A buyer or investor must immediately understand:

- What project this is.
- Where the building is.
- Which apartment is selected.
- What facts matter.
- How to inquire.

The live direction has improved behavior, but the selected apartment experience still reads as a technical patch instead of a sales product.

### 4. Mobile 390 must be designed, not compressed

A mobile buyer should not receive a mini desktop page. At 390px:

- Building first.
- Unit rail scrolls horizontally.
- Selected panel appears below with full-width actions.
- No horizontal page scroll.
- No overlapping fixed CTA.

### 5. Public language must stay clean

Buyer-facing UI must never expose implementation terms. The public interface should say:

- Building view.
- Select apartment.
- Apartment selected.
- Get details.
- View from apartment.

It must not say internal source, model format, code framework, ranking mechanics, or proof terms.

## What is good today

- The 1.69.32 proof is finally honest about the behavior.
- Mobile 390 containment passed.
- Public leak scan in the tested state passed for the banned terms scanned there.
- The plugin already has the right place to implement the showroom template.

## What is not good enough today

- The visual hierarchy is not investor-grade.
- The selected apartment panel is not strong enough as a sales object.
- The project archive is not yet a premium product shelf.
- The brand mark is weak as a first-viewport signal.
- The system is still Rainbow-shaped unless Codex implements the reusable asset contract.

## Verdict

1.69.32 is a bridge. It is not the premium endpoint.

