# Rainbow Showroom — Page Layout Contract (v1.67.3)

> **Audience:** every agent (Claude, Codex, future) touching `nadlan_project` pages.
> **Source of truth.** Patches must respect this diagram or update it first.
> **References used:** Zillow 3D Home / interactive floor-plan pattern · Homes.com + Matterport (tour + plan = buyer confidence) · `<model-viewer>` hotspots docs (Google ARCore team) · NN/g progressive disclosure · WCAG 2.5.5 / Apple HIG ≥44 px tap targets · `skills/design-page-patterns.md`, `skills/design-rtl-hebrew.md` §54, `skills/luxury-design-system.md`, `skills/article-guide-design-pattern.md`, `skills/honesty-statement.md`, `skills/skill-release-discipline-and-mistakes.md`.

---

## 1. Desktop (≥761 px) — flow

```mermaid
flowchart TB
  classDef heroMedia fill:#dbe9e3,stroke:#1b3a32,color:#0e1f1a,stroke-width:2px
  classDef intro fill:#fff7e6,stroke:#b99043,color:#3a2a09
  classDef showroom fill:#0d2026,stroke:#ead8a3,color:#fff7df
  classDef facade fill:#143038,stroke:#3ddc84,color:#dff8e9
  classDef card fill:#0a1718,stroke:#ead8a3,color:#fff7df
  classDef article fill:#fafaf7,stroke:#7a8a82,color:#142020
  classDef forms fill:#fff,stroke:#b99043,color:#1a2620

  N[Site nav · RTL]:::intro --> H

  subgraph H["A · Project Hero Media  (Zillow-style high-impact)"]
    direction LR
    H1[Eyebrow:<br/>פרויקט חדש בשדה דב]:::intro
    H2[h2 · 28-44px serif · centered above paragraph]:::intro
    H3[Lead paragraph · 16-17px · 60-72 ch]:::intro
    H4[CTA → #nlp3d-stage]:::intro
    H5[Hero IMG poster · 16:9<br/>visible BEFORE the showroom<br/>uses meta.poster / OG image]:::heroMedia
    H1 --> H2 --> H3 --> H4
    H2 -. above .- H5
  end

  H --> S

  subgraph S["B · Showroom (alignfull, dark, dominant)"]
    direction TB
    S0[Toolbar · רחב/סובב/קרב/הרחק]:::showroom
    S1[3D context: spinning GLB tower<br/>NO clickable squares here<br/>spins 360 for orientation only]:::showroom
    S2[Facade picker · always visible<br/>cells = apartments<br/>green/amber/grey · 44px tap]:::facade
    S0 --> S1
    S0 --> S2
    S1 -. inset 0 .- S2
  end

  S --> C

  subgraph C["C · Selected-Apartment Card  (BELOW the scene · never overlaps)"]
    direction TB
    C1[Title · קומה · סטטוס chip]:::card
    C2[layout · m² · view · est. price]:::card
    C3[CTA row: details · floorplan · WhatsApp]:::card
    C1 --> C2 --> C3
  end

  C --> F

  subgraph F["D · Lead/Inquiry Form  (sticky on desktop right rail)"]
    direction TB
    F1[Name · phone · email]:::forms
    F2[Goal · timeline]:::forms
    F3[Submit · אומדן לא מחייב]:::forms
    F1 --> F2 --> F3
  end

  F --> A

  subgraph A["E · Article Body  (RTL guide pattern)"]
    direction TB
    A1[H2 · centered ABOVE its paragraph<br/>NOT side-floated<br/>same 720-820px reading column]:::article
    A2[Paragraphs · 1.7 line-height]:::article
    A3[H3 · same column · above its paragraph]:::article
    A4[Tables · facts grid]:::article
    A5[FAQ accordions  · progressive disclosure]:::article
    A1 --> A2 --> A3 --> A2 --> A4 --> A5
  end

  A --> Foot[Footer · 4-col RTL]:::intro
```

## 2. Mobile (≤760 px) — stack discipline (no overlap)

```mermaid
flowchart TB
  classDef heroMedia fill:#dbe9e3,stroke:#1b3a32
  classDef showroom fill:#0d2026,stroke:#ead8a3,color:#fff7df
  classDef facade fill:#143038,stroke:#3ddc84,color:#dff8e9
  classDef card fill:#0a1718,stroke:#ead8a3,color:#fff7df
  classDef article fill:#fafaf7,stroke:#7a8a82,color:#142020

  M0[Eyebrow + H2 + lead paragraph<br/>full-bleed 16px gutters]:::heroMedia
  M0 --> M1[Hero IMG · 16:9 · loading=lazy<br/>visible BEFORE the showroom]:::heroMedia
  M1 --> M2[Toolbar · sticky top of stage<br/>44px tall buttons]:::showroom
  M2 --> M3[3D context · 60-70vh<br/>OR 2.5D facade — never both stacked<br/>chosen by data-mobile-mode]:::showroom
  M3 --> M4[Facade picker · full-bleed<br/>cells ≥44×44 · big enough to tap]:::facade
  M4 --> M5[Selected card · sticky bottom sheet<br/>peek 120px collapsed · expand to 60vh<br/>NEVER position:fixed over the facade]:::card
  M5 --> M6[Inquiry form · stacked]:::card
  M6 --> M7[Article H2 above paragraph<br/>full-width column<br/>line-height 1.7]:::article
  M7 --> M8[FAQ accordions]:::article
```

## 3. Non-overlap rules (the contract you cannot break)

```mermaid
graph LR
  classDef ok fill:#e7f7ee,stroke:#1b8a4e,color:#0a3a1e
  classDef bad fill:#fde7e7,stroke:#a52121,color:#3a0a0a
  R1[Selected card ABOVE facade?]:::bad -- forbidden --> R2[Facade hidden by card]:::bad
  R3[Selected card BELOW scene · sticky bottom on mobile]:::ok -- allowed --> R4[Facade always tappable]:::ok
  R5[H2 floated to side of paragraph]:::bad -- forbidden --> R6[Reader loses heading-to-text link]:::bad
  R7[H2 centered above its paragraph]:::ok -- allowed --> R8[Reading column stays intact]:::ok
  R9[Hero IMG below 3D]:::bad -- forbidden --> R10[Buyer never sees the project image]:::bad
  R11[Hero IMG above showroom · supports OG]:::ok -- allowed --> R12[First glance = real project image]:::ok
  R13[Floating squares on spinning model]:::bad -- forbidden --> R14[Picker drifts as model rotates]:::bad
  R15[Cells on locked facade plane only]:::ok -- allowed --> R16[Cells always sit on the wall]:::ok
```

## 4. Honest scope

- This is a **2.5D** facade selector (cells on a fixed elevation plane). True 360° per-apartment picking on the rotating GLB needs a real BIM/per-apartment mesh — not available yet. The GLB stays as **spinning context**, the picker is the fixed facade. (`skills/honesty-statement.md`.)
- Article H2/H3 are normalised to the article column. Some legacy theme styles tried to "side-float" headings on RTL; we override.
- Mobile uses a **sticky bottom-sheet** for the selected card, not `position: fixed`, so the facade above is never covered.

## 5. Acceptance (gate `v1.67.3`)

- Desktop 1440: hero image visible before showroom · showroom dominant width · selected card sits **below scene**, never covers facade · H2/H3 centered above their paragraph.
- Mobile 390: 3D OR facade visible at a time (no double stack overlap) · selected-card sticky bottom sheet, peek 120 px · all tap targets ≥44 px · no horizontal scroll.
- All six version surfaces aligned at **1.67.3**.
- ZIP 0 backslash, rooted, CRC ok.
- Healthcheck reports `showroom_hierarchy_v1673: true`.
