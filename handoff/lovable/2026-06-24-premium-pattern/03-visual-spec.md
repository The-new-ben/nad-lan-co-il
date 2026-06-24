# 03 Visual Spec

## Direction

Cream editorial luxury. Quiet, precise, Israeli real-estate product. Not a dark dashboard. Not teal and gold. Not a listings board.

## Palette

| Name | Hex | Use |
|---|---:|---|
| Cream | #FAF7F1 | Page background |
| Ink | #1B1A17 | Text, primary buttons |
| Gold | #9C7A3C | Premium accent, selected action |
| Terracotta | #C2563A | Warm secondary accent, reserve state |
| Sage | #7A8F6A | Available state |
| Sand | #EFEAE0 | Soft surface |
| Card | #FBF9F4 | Cards and panels |
| Border | #D9D2C4 | Hairlines |
| Muted | #6B6457 | Secondary text |

## Typography

Hebrew first:

- Display: Frank Ruhl Libre, weight 500.
- Body: Heebo, weight 400 to 700.

English:

- Display: Fraunces, weight 500.
- Body: Inter Tight, weight 400 to 700.

Do not use Inter as the Hebrew primary font. Do not use Poppins.

## Type sizes

Desktop:

- Brand: 30px.
- H1: 58px, line height 1.04.
- H2: 34px, line height 1.12.
- Body: 16px, line height 1.6.
- Small: 14px.
- Chip: 13px.

Mobile 390:

- Brand: 25px.
- H1: 36px, line height 1.08.
- H2: 28px.
- Body: 16px.
- Chip: 12px to 13px.

## Spacing

Use an 8px rhythm.

- Desktop page gutter: 40px.
- Mobile page gutter: 20px.
- Header desktop: 76px.
- Header mobile: 64px.
- Section top: 36px to 58px.
- Main grid gap: 18px.
- Card padding: 14px to 22px.

## Borders and radius

- Standard radius: 4px.
- Large radius: 8px only for large visual containers if needed.
- Pills: 999px.
- Borders: 1px solid #D9D2C4.

## Buttons

Primary button:

```css
.nl3d-btn {
  min-height: 44px;
  border-radius: 4px;
  padding: 11px 18px;
  background: #1B1A17;
  color: #FAF7F1;
  font-weight: 700;
}
```

Gold action:

```css
.nl3d-btn.gold {
  background: #9C7A3C;
  border-color: #9C7A3C;
  color: #fffaf0;
}
```

Mobile rule:

```css
@media (max-width: 760px) {
  .nl3d-btn { width: 100%; }
}
```

## Showroom stage

Desktop:

```css
.nl3d-stage {
  min-height: 642px;
  border: 1px solid var(--border);
  background: #fbf4e7;
  position: relative;
  overflow: hidden;
}
```

Mobile:

```css
@media (max-width: 760px) {
  .nl3d-stage { min-height: 466px; }
}
```

## Unit pins

- Desktop width: 74px.
- Mobile width: 46px.
- Selected state uses ink background and cream text.
- Sold state uses opacity, not red warning language.

## Missing asset state

Use a dignified panel. Do not show fake project visuals.

Buyer copy:

- HE: ממתינים לחומר חזותי מהיזם
- EN: Awaiting project visuals

## Favicon and social usage

- Favicon 32: dark ink tile, cream N, small gold 3D dot or superscript.
- Favicon 192: same composition with more breathing room.
- Apple touch 180: cream background, ink word fragment, gold 3D.
- OG card: cream background, building silhouette, project showroom sentence.
