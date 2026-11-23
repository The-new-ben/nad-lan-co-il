// HAD-803 climate lab, real-materials pass v1 (23.11.2026, LOCAL ONLY, not on the live site).
// Loads the furnished E-4A living room, kitchen and balcony made in Blender (scripts/climate-lab/furnish_e4a_v1.py) and puts it in
// place of the lab's own grey walls and floors in the walk view. The sky light is BAKED into one lightmap (it travels in the GLB
// as the occlusion texture on the second UV set and is moved here to material.lightMap); the SUN stays the lab's real-time
// DirectionalLight, so the sun patch on the floor is still the real shadow of the real sun for the chosen date and hour.
// From above (doll view) the lab keeps its own cut walls; the furnished floor and furniture are cut at the same 118 cm.
export const REPLACES = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's16', 's17']; // starter pieces this model furnishes
const WALK_ONLY = new Set(['walls', 'frames', 'doors', 'glass', 'ceiling', 'ceiling_balcony', 'ceiling_lights', 'curtains', 'slab_edges', 'balcony_rail']);
const NO_CAST = new Set(['glass', 'balcony_rail', 'curtains', 'ceiling', 'ceiling_balcony', 'rug', 'floor', 'deck']);
const GLOSSY = /^(porcelain|stone|glass|rail_glass|black_glass|steel|alu_anthracite|black_metal|lacquer_white|ceramic|opal_glass)/;
export const TUNE = { lm: 0.85, lmDoll: 1.2, env: 0.22, envGlossy: 0.9, hemi: 0.32, night: 0.42, rain: 0.62, lamps: 2.2, exposure: 1.08, low: 16, gold: 2.1 };
// the view behind the glass (round 2): an equirectangular band rendered in Blender (scripts/climate-lab/panorama_v2.py), sky transparent
export const VIEW = { url: './models/view-panorama-v2.webp.js', lo: -32, hi: 16, R: 150, u0: 0 };

export async function mountRealRoom(space, C, url, view = VIEW) {
  const L = space.lab, { THREE, scene, renderer } = L;
  const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
  const gltf = await new GLTFLoader().loadAsync(url);
  const root = gltf.scene, ex = (gltf.parser.json.asset && gltf.parser.json.asset.extras) || {};
  const scale = ex.lightmapScale || 4;
  const cut = new THREE.Plane(new THREE.Vector3(0, -1, 0), 1.18); // keep below 118 cm, the lab's plan cut
  const mats = new Set(), walkOnly = [], lamps = [];
  for (const top of root.children) {
    const name = top.name || '';
    if (WALK_ONLY.has(name)) walkOnly.push(top);
    top.traverse((o) => {
      if (!o.isMesh) return;
      o.castShadow = !NO_CAST.has(name); o.receiveShadow = true;
      const m = o.material; mats.add(m);
      if (m.aoMap) { m.lightMap = m.aoMap; m.aoMap = null; m.lightMap.colorSpace = THREE.SRGBColorSpace; m.lightMap.needsUpdate = true; }
      m.userData.glossy = GLOSSY.test(m.name || '');
      if (/^(leaves|grass)/.test(m.name)) { m.transparent = false; m.alphaTest = 0.5; m.side = THREE.DoubleSide; }
      if (/^(glass|rail_glass)/.test(m.name)) { m.depthWrite = false; m.side = THREE.DoubleSide; o.renderOrder = 2; }
      if (/^sheer/.test(m.name)) { m.depthWrite = false; m.side = THREE.DoubleSide; o.renderOrder = 3; }
      if (/^(downlight|opal_glass)/.test(m.name)) { m.emissive = new THREE.Color(0xFFE2BC); lamps.push(m); }
      if (name === 'ceiling_lights' && /^opal_glass/.test(m.name)) o.position.y += 0.3; // the pendant globes hang 30 cm higher than baked: clear of the standing eye line
      if (/^lemon/.test(m.name)) o.visible = false; // two lemons in the v2 bake read as yellow balls, and yellow belongs to the sun only
    });
  }
  scene.add(root);
  renderer.localClippingEnabled = true;
  // the lab's own pieces this model replaces
  const hideLab = (walk) => {
    L.gFloor.visible = false; L.ceiling.visible = false;
    L.gWall.visible = !walk; L.gGlass.visible = !walk;
    for (const g of scene.children) if (g.isGroup && g.children.some((c) => c.userData && c.userData.point)) g.visible = false; // service points
  };
  L.hemi.color.multiplyScalar(TUNE.hemi); L.hemi.groundColor.multiplyScalar(TUNE.hemi);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  // ---- the view: a band on a cylinder around the apartment; elevation is linear in the picture, so each ring sits at R·tan(angle) ----
  let band = null;
  try {
    const tex = await new THREE.TextureLoader().loadAsync(view.url); tex.colorSpace = THREE.SRGBColorSpace; tex.wrapS = THREE.RepeatWrapping; tex.anisotropy = 4;
    const SEG = 160, RINGS = 24, pos = [], uv = [], idx = [], R = view.R;
    for (let j = 0; j <= RINGS; j++) {
      const th = THREE.MathUtils.degToRad(view.lo + ((view.hi - view.lo) * j) / RINGS), y = R * Math.tan(th);
      for (let i = 0; i <= SEG; i++) { const ph = (i / SEG) * Math.PI * 2; pos.push(R * Math.cos(ph), y, R * Math.sin(ph)); uv.push(view.u0 + 0.5 + ph / (Math.PI * 2), j / RINGS); }
    }
    for (let j = 0; j < RINGS; j++) for (let i = 0; i < SEG; i++) { const a = j * (SEG + 1) + i, b = a + SEG + 1; idx.push(a, b, a + 1, b, b + 1, a + 1); }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new THREE.Float32BufferAttribute(uv, 2)); g.setIndex(idx);
    band = new THREE.Mesh(g, new THREE.MeshBasicMaterial({ map: tex, transparent: true, alphaTest: 0.02, side: THREE.DoubleSide, depthWrite: false, fog: false, toneMapped: false }));
    band.position.set(L.mid.x, 1.6, L.mid.z); band.renderOrder = -2; band.frustumCulled = false; L.outside.add(band);
    for (const o of L.outside.children) { if (o === band || (o.material && o.material.uniforms && o.material.uniforms.sunPosition)) continue; if (o.isGroup) o.visible = false; } // the lab's box city goes; its live sea and land stay under the skyline
  } catch (e) { console.warn('view band not loaded', e); }
  // ---- a soft glow around the sun disc (the board's halo), drawn behind the glass ----
  const glowTex = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'), gr = x.createRadialGradient(128, 128, 0, 128, 128, 128);
    gr.addColorStop(0, 'rgba(255,236,190,1)'); gr.addColorStop(0.12, 'rgba(255,214,140,.65)'); gr.addColorStop(0.4, 'rgba(255,190,110,.18)'); gr.addColorStop(1, 'rgba(255,180,100,0)'); x.fillStyle = gr; x.fillRect(0, 0, 256, 256);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
  const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, fog: false, toneMapped: false }));
  glow.scale.setScalar(70); glow.renderOrder = 1; scene.add(glow);
  const disc = scene.children.find((o) => o.isMesh && o.geometry && o.geometry.parameters && o.geometry.parameters.radius === 3.2);
  const warm = new THREE.Color(0xFF9A40), noon = new THREE.Color(0xFFF1DC), tint = new THREE.Color();
  const sunSet = { i: -1, c: new THREE.Color(), bi: 0, bc: new THREE.Color() };
  let last = '', envSeen = null, wasWalk = null;
  function update(force) {
    const walk = space.mode === 'walk', st = C.st, alt = st.sun ? st.sun.alt : 30;
    const day = Math.min(1, Math.max(0, (alt + 2) / 14));
    const key = [walk, st.mode, Math.round(alt * 10), scene.environment && scene.environment.uuid, L.sun.intensity.toFixed(3)].join('|');
    if (key === last && !force) return; last = key;
    hideLab(walk);
    for (const o of walkOnly) o.visible = walk;
    const k = (walk ? TUNE.lm : TUNE.lmDoll) * (TUNE.night + (1 - TUNE.night) * day) * (st.mode === 'rain' ? TUNE.rain : 1);
    const env = scene.environment, ei = scene.environmentIntensity || 0.3;
    for (const m of mats) {
      if (m.lightMap) m.lightMapIntensity = scale * Math.PI * k;
      if (env !== envSeen) m.envMap = env;
      m.envMapIntensity = (m.userData.glossy ? TUNE.envGlossy : TUNE.env) * ei / 0.5;
      if (walk !== wasWalk) { m.clippingPlanes = walk ? null : [cut]; m.needsUpdate = true; }
    }
    envSeen = env; wasWalk = walk;
    for (const m of lamps) m.emissiveIntensity = TUNE.lamps * (1 - day) * (st.mode === 'rain' ? 0.6 : 1);
    // a golden low sun: a stronger, warmer beam when the sun is low, so the patch on the floor reads warm at sunset
    if (L.sun.intensity !== sunSet.i || !L.sun.color.equals(sunSet.c)) { sunSet.bi = L.sun.intensity; sunSet.bc.copy(L.sun.color); } // the climate set a new sun
    L.sun.intensity = sunSet.bi; L.sun.color.copy(sunSet.bc);
    if (st.mode !== 'rain' && alt > 0 && alt < TUNE.low) { const f = 1 - alt / TUNE.low; L.sun.color.lerp(warm, 0.55 * f); L.sun.intensity = sunSet.bi * (1 + (TUNE.gold - 1) * f); }
    sunSet.i = L.sun.intensity; sunSet.c.copy(L.sun.color);
    renderer.toneMappingExposure = TUNE.exposure;
    if (disc) { glow.position.copy(disc.position); glow.visible = disc.visible && walk; glow.material.opacity = Math.min(1, 0.35 + Math.max(0, 1 - alt / 30)); }
    if (band) { // the view follows the light of the hour: darker at night, warmer at sunset, grey in a storm
      const f = Math.max(0, 1 - Math.max(alt, 0) / TUNE.low) * (alt > -2 ? 1 : 0);
      tint.copy(noon).lerp(warm, 0.35 * f).multiplyScalar(0.25 + 0.75 * day); if (st.mode === 'rain') tint.setRGB(0.55, 0.6, 0.66);
      band.material.color.copy(tint); band.visible = walk;
    }
    L.touch(true);
  }
  (function tick() { update(); requestAnimationFrame(tick); })();
  update();
  return { root, extras: ex, update, TUNE };
}
