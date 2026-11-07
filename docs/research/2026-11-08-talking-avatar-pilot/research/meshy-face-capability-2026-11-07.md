# Meshy and the approved NadLan face

Checked 7 November 2026. **Meshy is available; a separate tool named iMesh was not identified. Meshy may provide a fuller head mesh, but it does not supply the detailed facial rig or learned lip synchronization needed here. No Meshy generation was run and no credits were consumed.**

## What is actually connected

The shared registry records Meshy Pro from 15 October and an existing script-only credential. A fresh authenticated `GET /openapi/v1/balance` returned HTTP 200 and **752 credits**, all monthly, with zero permanent credits. This proves current API access and the returned balance, not the current subscription label. The official documentation explicitly identifies balance reads as free. The sanitized receipt is in `research/primary/meshy-2026-11-07/balance-sanitized.json`. [Balance API](https://docs.meshy.ai/en/api/balance)

No Meshy/iMesh connector is enabled in this session. `agent-tools/meshy/` contains the key-saving helper, but no operational launcher. Scoped checks found no iMesh/Meshy installed Windows application or Blender add-on, and no existing Meshy-labelled asset in this project. These checks do not rule out an unrelated tool elsewhere. If Ben meant another product by “iMesh,” its name or link is the remaining clarification; the concrete available service is **Meshy**.

Existing credits are not permission to consume them under the current no-spend instruction. Current API pricing lists 20 credits for Meshy7.1 geometry, 30 with 2K/4K texture, a 5-credit higher-resolution surcharge, and 5 for automatic rigging. Web-app and API price tables differ; the old registry's monthly-plan note does not establish a free API generation. [API prices](https://docs.meshy.ai/en/api/pricing)

## Current capability, with dates

- Meshy7.1 launched on **10 September 2026**; the API added it on **18 September**. It targets geometric detail. Its vendor benchmark compares surface detail, not preservation of this woman's identity or speaking-face realism. [Launch](https://www.meshy.ai/blog/meshy-7-1-launch), [API changelog](https://docs.meshy.ai/en/api/changelog)
- The same official changelog lists **2 November** Meshy N1 texturing, **3 November** selectable texture models, and **5 November** a bas-relief API. No facial-rig or lipsync release is listed in those entries. Crawl/update dates were not treated as release dates. [Dated entries](https://docs.meshy.ai/en/api/changelog)
- Meshy's own auto-rigging FAQ says jaw, eye and mouth controls still require manual work in Blender or Maya. Its animation guide likewise sends detailed facial expression work to those applications. Its documented rigging API is a body skeleton for textured humanoids with distinct limbs, not a head-only talking rig. [Official face limitation](https://www.meshy.ai/features/ai-auto-rigging), [Animation guide](https://docs.meshy.ai/en/webapp/guides/animate), [Rigging API](https://docs.meshy.ai/en/api/rigging)
- Current model documentation offers detailed geometry and lower-poly Smart Topology candidates. Those may reduce manual shape construction, but neither the documentation nor a body rig demonstrates mouth-specific edge loops, blink shapes, teeth or valid phoneme controls for our face. [Model comparison](https://docs.meshy.ai/en/api/models)

The README's old “no face or lip features; bodies or props only” sentence is therefore too broad about **static face geometry**. Its warning against expecting an automatic talking-face rig remains supported. Generating a face-shaped mesh and animating a recognizable face are different capabilities.

## Could it improve this exact face?

**Possibly the volume and side views, not a demonstrated improvement to the approved front view.** Our current GLB is a photo-textured limited-view portrait: 953,224 bytes, 7,162 triangles across three primitives, 3,826 vertices, no skeleton, and mouthOpen/blink targets on the main surface. Blink actually uses its separate overlay. Meshy could infer a more complete head, but the unseen sides would remain generated guesses from one photo. It could also alter the eyes, nose, hairline or lip proportions that presently preserve the approved appearance.

A future candidate would need Blender cleanup, facial shape keys and the same local audio driver. Its exported GLB could play locally without a Meshy service during conversation. None of that makes its initial generation free or proves that its identity, mouth motion or browser performance is better. Under the present boundary, continue free local topology/shape-key work and preserve the approved face.

## Controlled comparison required before choosing a replacement

These are proposed measurements, not completed Meshy tests or universal scientific thresholds.

| Dimension | Fair measurement and decision rule |
|---|---|
| Identity | Same camera, crop, display size and neutral pose; compare against the approved source, not a regenerated reference. Record landmark error normalized by inter-eye distance and hair/face silhouette overlap. Use face-similarity embeddings only as supporting evidence. Ben's blinded A/B identity judgment remains necessary. |
| Geometry | Inspect neutral and the actual small yaw extrema, then wider diagnostic views separately. Count holes, stretched texture, hair halos and mouth seams. A plausible unseen side is not ground-truth reconstruction. |
| Minimal lips | Feed identical Chatterbox WAVs, timelines and gain. Measure mouth aperture relative to face width, neutral return and temporal jitter. Hand-label a small set of p/b/m closures and speech pauses before scoring closure and audio/video offset; predicted visemes are not ground truth. Reject improved activity obtained merely by exaggerating the jaw. |
| Browser cost | Same page, viewport, browser and device; compare transfer bytes, first visible frame, memory, frame-time median/p95, dropped frames and analysis delay during actual speech. Preserve the present 30-fps rendering policy and require no regression in controls or cancellation. Emulation is not a real-phone hardware benchmark. |
| Reproducibility | Keep the source image/hash, exact generation settings and credit cost, unretouched export, edited GLB, fixed test WAVs, uncut screen/audio recording and failures. A static screenshot or a vendor geometry leaderboard cannot establish talking-avatar superiority. |

Sources were downloaded read-only with timestamps and SHA256 receipts under `research/primary/meshy-2026-11-07/`. No key was printed, no model was generated, no widget/backend/model was edited, and no claim is made to have tested every avatar or found the world's best face.
