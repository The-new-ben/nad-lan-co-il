# Product-Grade 3D Model Generation Research

Date: 2026-06-26
Scope: NadLan project showrooms, starting with Ashira and using Rainbow as the local quality reference.

## Honest Finding

The current Ashira prototype GLB is not yet a product-grade model. It is a technical proof that a
model can load, rotate and sit beside a facade picker. The Rainbow package is much stronger because
it has richer geometry, many materials, a site landscape, a poster, plans, environment data and a
full payload.

The old "Nike/product configurator" research was not lost. It exists at:

- `docs/2026-06-12-3d-configurator-research.md`

I did not find a local file named `Vango`, `Vango GMB` or `Vango GLB`. Web search suggests the
possibly related term may be `Vagon`, which is a pixel-streaming/cloud-rendering platform for
Unreal/Unity experiences. That is a future premium path, not the first WordPress page path.

## What Product-Grade Means

For NadLan, "like Nike shoes" means:

1. The object is framed close, like a product, not a distant city map.
2. Rotation is horizontal and controlled. The buyer should not see the underside of the building.
3. The model has recognizable architecture: tower mass, podium, facade rhythm, floor plates,
   balconies, shadows and material contrast.
4. The model has local context: sea, promenade, nearby projects, Reading/Namal or local anchors.
5. The apartment choice is not a floating marker. Until we have segmented BIM, exact selection
   happens on a fixed facade/elevation beside the model.
6. Mobile uses the same product hierarchy: model first, facade immediately next, selected apartment
   card below, no overflow.

## External Sources Checked

### 3D Commerce / GLB Standards

- Khronos 3D Commerce explains glTF as the web-commerce standard for highly realistic 3D
  visualization, configurators and AR/VR commerce experiences.
  Source: https://www.khronos.org/gltf/3dcommerce/
- Khronos Real-Time Asset Creation Guidelines are specifically for high-quality real-time 3D models
  for web, apps, games and XR.
  Source: https://github.com/KhronosGroup/3DC-Asset-Creation/blob/main/asset-creation-guidelines/RealtimeAssetCreationGuidelines.md
- Khronos 2025 Asset Creation Guidelines 2.0 confirms the modern target is still glTF, with
  photorealistic asset creation, animation and compression best practices.
  Source: https://www.khronos.org/blog/introducing-asset-creation-guidelines-2.0-siggraph-2025

### Product Viewer / Shoe-Like Behavior

- Fittingbox Footwear describes the shoe viewer standard: zoom, rotation, all angles, inside and
  sole views, true-to-life textures.
  Source: https://footwear.fittingbox.com/en/3d-viewer-of-shoes
- Cloudimage 360 View is a product-viewer pattern for any object: 360 rotation, zoom, autoplay,
  hotspots and fullscreen.
  Source: https://scaleflex.github.io/cloudimage-360-view/
- Cloudimage documentation describes the 360 viewer as a lightweight high-performance product
  showcase with responsive images.
  Source: https://docs.cloudimage.io/interactive-experience-builders/360-view-plugin
- Sketchfab/Nike Air Max 270 coverage shows real-time customization and a 3D sneaker demo as the
  retail reference pattern.
  Source: https://wwd.com/footwear-news/shoe-industry-news/sketchfab-nike-3d-airmax-1238732615/

### Real Estate Viewer Patterns

- DIGBY's apartment selector uses active areas marked in perspective on a 3D rendered property
  image; each apartment can expose floor plans, images and sales data.
  Source: https://digby.hu/apartment-selector
- UFO Engineering describes the same product pattern as a website widget with architecture project
  images, building/apartment masks, availability and booking flow.
  Source: https://ufo-engineering.com/cases/apartment-selector
- Render Vision's apartment viewer frames the goal directly: buyers orbit the building, check window
  views and compare units across floors.
  Source: https://render-vision.com/services/3d-apartment-viewer-services/
- Zillow 3D Home and interactive floor plans combine tours and floor plans so buyers understand
  layout and imagine living there.
  Sources:
  - https://www.zillow.com/3d-home/
  - https://www.zillow.com/3d-home/floor-plans/
  - https://zillow.mediaroom.com/2021-02-17-Zillow-Launches-Next-Generation-3D-Tours
- Homes.com + Matterport positions the tour as a 24/7 open house with floor plans and room revisits.
  Source: https://www.homes.com/solutions/matterport

### Web Runtime Choices

- `model-viewer` supports camera controls, camera orbit, field of view, auto-rotate, poster/reveal
  behavior and hotspots aligned to model coordinates.
  Sources:
  - https://modelviewer.dev/docs/
  - https://modelviewer.dev/examples/stagingandcameras/
- model-viewer hotspot discussions show that accurate hotspot work requires real model coordinates,
  vertex groups or generated coordinate data. It is not something to fake with random dots.
  Sources:
  - https://github.com/google/model-viewer/discussions/4116
  - https://github.com/google/model-viewer/discussions/4788
- three.js forum guidance favors glTF over OBJ for web delivery and stresses model optimization for
  load speed.
  Source: https://discourse.threejs.org/t/threejs-configurator-gltf-vs-obj-performance/3747
- Babylon.js forum confirms product configurators are viable, but they require a real application
  architecture rather than just a static asset.
  Source: https://forum.babylonjs.com/t/what-is-the-easiest-way-to-make-a-scalable-product-configurator-using-babylon/48656

### BIM / Real Estate Asset Pipeline

- xeokit BIM Viewer is a browser BIM viewer for IFC, BIM, CAD and point clouds.
  Source: https://github.com/xeokit/xeokit-bim-viewer
- xeokit-convert converts IFC, GLB and CityJSON into XKT for fast BIM viewing.
  Source: https://github.com/xeokit/xeokit-convert
- xeokit's IFC workflow confirms that a BIM pipeline can exist, but it is a separate viewer/data
  pipeline from a simple model-viewer GLB.
  Source: https://xeokit.io/blog/viewing-federated-ifc-models/

### Cloud / Pixel Streaming

- Vagon Streams is a no-code pixel streaming solution for Unreal/Unity applications with cloud GPUs.
  Source: https://vagon.io/streams
- Vagon explains pixel streaming as sending the user a live video of the 3D application while the
  actual heavy rendering runs in the cloud.
  Source: https://vagon.io/streams/glossary/pixel-streaming
- This is relevant for future ultra-premium showrooms, but it adds operating cost and complexity.
  It is not the first production path for WordPress project pages.

## Technical Decision For NadLan

### Path A: WordPress Product Viewer, Now

Use `model-viewer` with optimized GLB for the rotating context model and a fixed facade/elevation
selector beside it.

This is the right path for Ashira/Rainbow now because:

- it loads inside WordPress;
- it is cheaper than cloud streaming;
- it supports poster, camera orbit, field of view, auto-rotate and hotspots;
- it works with our current CMS payload;
- it can use official GLB later by replacing a URL.

Minimum model standard:

- GLB under 8 MB for prototype, under 15 MB only when quality justifies it;
- multiple materials;
- correct local context;
- camera polar locked to a narrow range, no underside view;
- close initial radius and narrow field of view;
- no apartment picking in GLB unless the GLB has named apartment meshes or reviewed hotspots.

### Facade Selector Standard, Now

The facade is not a fallback decoration. It is the exact apartment-picking surface until the GLB is
segmented.

Research pattern:

- DIGBY: clickable active areas on a rendered property image, with uploaded floor plans, images and
  sales data.
- UFO Engineering: masks over architecture/project/building/apartment imagery, with availability
  and booking.
- Zillow/Homes.com/Matterport: after selection, the buyer needs interior tour/floor-plan context,
  not only a marker.

NadLan rule:

1. Do not stack a new facade on top of an old facade. There must be one active selector surface in
   the page at a time.
2. If a rebuild is needed, remove or disable the old selector first and ask the owner before making
   a destructive facade replacement.
3. Apartment cells should be real polygons/masks or aligned rectangles on the building image, not
   floating dots.
4. Each cell needs visible availability state, a comfortable hit area, keyboard/focus access and a
   selected state.
5. The selected card must be dismissible and must not permanently cover the facade on mobile or
   desktop.
6. The facade image/masks should come from official elevation/render material when available. If
   generated, label it illustrative and make the URL replaceable in CMS.
7. The selected unit must carry through to drawings, interior tour, view-from-apartment and contact.

### Path B: 360 Image Sequence, Optional Premium Fallback

Use a 24-48 frame sprite/image-sequence when a contractor has high-quality renders but no web-ready
GLB. This is the Nike/shoe-style pattern.

Good for:

- photorealistic marketing hero;
- fast perceived quality;
- controlled angle, no underside.

Bad for:

- true 3D picking;
- per-apartment geometry;
- heavy storage if not hosted on R2/CDN.

### Path C: Segmented GLB / BIM, Future Premium

Use Three.js or xeokit only when we receive or create a real segmented model:

- each apartment/floor is a named mesh;
- mesh names map to CMS unit ids;
- click uses raycasting;
- BIM/IFC conversion includes a manual mesh-map review.

This is the only honest path to "click the apartment on the rotating building."

### Path D: Vagon / Pixel Streaming, Later

Use cloud streaming only for a very high-ticket showroom, where Unreal/Unity quality matters more
than cost and startup time.

This is not the default NadLan factory path.

## Immediate Correction To Ashira

The Ashira GLB should be upgraded before PR:

1. Compare against Rainbow's richer GLB package.
2. Replace the tiny cube-only GLB with a richer multi-material generated model.
3. Lock camera to product-like horizontal orbit:
   - no underside;
   - gentle auto-rotate;
   - closer default radius;
   - narrower field of view.
4. Keep apartment selection on the fixed facade beside the model.
5. Screenshot desktop/tablet/mobile after the model change.

## Factory Rule

Do not ship another project with a one-material cube massing and call it a showroom. A minimum
prototype model must have:

- recognizable tower shape;
- floor rhythm;
- podium;
- surrounding buildings or site context;
- sea/park/road/landmark orientation when relevant;
- separate materials;
- validated GLB;
- screenshot proof.
