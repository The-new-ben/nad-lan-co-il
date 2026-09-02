# Nad-Lan Premium Direction v2: asset manifest

Status date: 2026-09-01

Scope: private local design review only. Nothing in this manifest grants publication, advertising, redistribution, Figma import, WordPress use, or live-site use.

## Permission classes

- `PRIVATE_REFERENCE`: may appear only in the local V2 review artifacts with a visible internal-reference label.
- `RESEARCH_REFERENCE`: third-party screen capture for composition study only. Never public-facing.
- `INTERNAL_DERIVATIVE`: internally generated derivative. It is not a canonical architectural source.
- `RUNTIME_SOURCE`: executable local source used only to create a static preview when the approved preview route is available.

## Registered visual assets

| ID | Absolute path | Source and owner | Permission | Type | Internal caption | Alt text | Desktop crop | Mobile crop |
|---|---|---|---|---|---|---|---|---|
| `V2-A01` | `C:\Users\777\Documents\Codex\2026-08-30\plate-factory-manager\work\six8-official-source-view.png` | Official SIX8 source view supplied by the owner workflow. Rights holder is not documented in the workspace. | `PRIVATE_REFERENCE`. No documented publication permission. | Official project source image, 1282 x 607 JPEG/JFIF bytes despite the `.png` extension. Treat as a project visualization unless the rights holder confirms it is photography. | `SIX8, הרברט סמואל. תמונת מקור רשמית, רפרנס פנימי בלבד.` | `מגדל SIX8 מול הים בשעת שקיעה` | Hero: fill 760 x 770 with the tower in the right third and the sea horizon visible. Card: fill 430 x 285 with tower and pool. 3D fallback: fill 360 x 220 with tower centred. | Hero: fill 350 x 360 with the tower centred and some sea retained. Card: fill 154 x 120 with the tower centred. |
| `V2-A02` | `C:\Users\777\Documents\Codex\2026-08-30\plate-factory-manager\outputs\six8-herbert-samuel-plate-capsules.jpg` | Internal plate derived from SIX8 material by the local plate workflow. | `INTERNAL_DERIVATIVE`. Texture and card reference only. Not a canonical architectural source and not approved for publication. | Internal editorial plate, 1400 x 1050 JPEG. | `פלטת SIX8. רפרנס פנימי למרקם ולקפסולה בלבד.` | `פלטת השראה פנימית של SIX8 בגוני חול` | Language-board texture sample: crop the paper texture and one information capsule. Never use as the homepage hero. | Small texture or capsule crop only. Never use as the main project image. |
| `V2-A03` | `C:\Users\777\Documents\Codex\2026-08-24\referenced-chatgpt-conversation-this-is-an\work\zip-check-master-1.0.0-rc3\aurelia-master-recipe-1.0.0-rc3\06-INPUT-BASELINE\rainbow-fullpage-1.png` | Internal baseline capture from the Aurelia project workspace. Underlying page ownership and reuse rights are not documented here. | `PRIVATE_REFERENCE`. Hierarchy and crop study only. Do not reuse its public copy, photography, plans, map, or brand. | Full-page reference capture, 3840 x 28800 PNG. | `Rainbow Tel Aviv. רפרנס פנימי להיררכיה וקרופ בלבד.` | `צילום מסך ארוך של עמוד פרויקט לצורך מחקר היררכיה` | Language-board crop only, focused on the image-led project header. | Language-board crop only, focused on the vertical rhythm. |
| `V2-A04` | `C:\Users\777\Documents\Codex\2026-09-01\nad-lan-redesign-directions\outputs\research-screenshots\12-ire-floor-plan.png` | Screenshot of an IRE Plugin demo page. Third-party source, with no reuse licence recorded. The file extension is PNG but the bytes are JPEG/JFIF. | `RESEARCH_REFERENCE`. Interface study only. Never use as a project floor plan or public asset. | Third-party interface screenshot, 1265 x 712 JPEG/JFIF. | `ממשק תוכנית קומה. צילום מחקר בלבד.` | `צילום מסך של ממשק בחירת תוכנית קומה` | Language-board UI reference crop only. | Language-board UI reference crop only. |
| `V2-A05` | `C:\Users\777\Documents\Codex\2026-09-01\nad-lan-redesign-directions\outputs\research-screenshots\08-rendexio-building.png` | Screenshot of the Rendexio building-selection demo. Third-party source, with no reuse licence recorded. The file extension is PNG but the bytes are JPEG/JFIF. | `RESEARCH_REFERENCE`. Building and floor-selection interaction study only. Never public-facing. | Third-party interface screenshot, 1272 x 716 JPEG/JFIF. | `בחירת בניין וקומה. צילום מחקר בלבד.` | `צילום מסך של ממשק בחירת קומה בבניין` | Language-board UI reference crop only. | Language-board UI reference crop only. |

## Runtime source and 3D fallback

| ID | Absolute path | Source and owner | Permission | Intended use | Current status |
|---|---|---|---|---|---|
| `V2-R01` | `C:\Users\777\Documents\Codex\2026-08-27\realtime-voice-chat\six8-designer-source.html` | Local SIX8 Three.js experience supplied in the owner brief. | `RUNTIME_SOURCE`. Local review only. | Capture a static real-engine preview after a user gesture, then use the still as the click target for `לסיור בפרויקט`. | Direct local-file browser loading is unavailable in the approved preview surface. V2 therefore uses `V2-A01` as an honest static fallback and does not claim that it is an engine capture. No WebGL is embedded in the homepage artifacts. |

## Placement rules

1. Every image in the V2 SVG sources must reference one of the IDs above.
2. `V2-A03`, `V2-A04`, and `V2-A05` may appear only on the internal language board and must carry a visible `רפרנס פנימי` or `צילום מחקר` label.
3. `V2-A02` may influence texture or one small capsule. It may not serve as architectural proof.
4. `V2-A01` is the only project source image permitted in the V2 homepage screens. It must be labelled as a private internal reference in the proof footer and must not be published.
5. No image may be described as a photograph when the source record does not establish that classification.
6. No placeholder, generic building illustration, invented map, or unregistered icon may replace a missing asset.
7. A future public version requires written rights confirmation, the rights holder name, permitted channels, territory, term, modification rights, credit line, and revocation process.

## Excluded assets

- Eco City, Cyprus, Dubai, private project assets, and anything under `rejected-geometry-drift`.
- All unsourced project photography and concept imagery presented as fact.
- Research screenshots outside the internal language board.
- Any generated building, map, plan, or 3D image used as if it were official project material.
