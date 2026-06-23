# Skill: Interactive Apartment Picker (Tier-1 SVG, any project site)
Proven pattern (nad-lan v1.57.0, inc/project-3d.php). What the SaaS vendors actually sell.
1. ASSET: one building elevation/render image per project (developer-supplied or AI-generated
   elevation drawing from photos).
2. DATA: units JSON per project: [{id, points:"x,y x,y ...", floor, rooms, sqm, balcony, dir,
   price, status: available|reserved|sold, plan:url}]. Sanitize: whitelist statuses, strip
   non [0-9,. -] from points (XSS), drop entries without id/points.
3. RENDER: <img> + absolutely-positioned <svg viewBox> overlay; one <polygon points data-unit
   tabindex=0 role=button aria-label> per unit; CSS fill by status; keyboard Enter/Space support.
4. PANEL: click -> RTL side panel with facts grid + lead mini-form POSTing to the EXISTING lead
   endpoint with source=project_3d + unit id -> the click enters the same AI-qualification funnel.
5. ADMIN: metabox to paste image URL + viewBox + units JSON + demo-mode checkbox (engine renders
   demo grid before real assets exist - label it clearly as demo).
6. TRACING WORKFLOW: draw polygons over the render in image-map.net or Figma -> export coordinates
   -> paste as JSON. 30-60 min per building.
7. NEXT TIERS: Mapbox GL fly-in intro (city -> project), per-floor stacking plans, vendor 3D twin
   (Smplrspace JS SDK) when the developer funds assets.

2026 Rainbow clarification: when a GLB/model-viewer massing exists, do not replace the facade
picker with floating dots. Keep the GLB as the rotating context model and place the fixed facade
picker beside it. Apartment cells should be embedded in the facade/elevation plane, show status and
basic unit facts, and open the existing selected-unit card. Only move picking into the GLB when the
asset contains real per-apartment meshes/BIM IDs.
