/**
 * PROPOSAL/OFFLINE ASSET — deterministic Einstein 33A illustrative massing.
 * Generates compact GLB files and a poster; it does not read or infer inventory.
 */
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SPEC = JSON.parse(fs.readFileSync(path.join(HERE, "model-spec.json"), "utf8"));
const HD_PATH = path.join(HERE, SPEC.files.hd);
const LOD_PATH = path.join(HERE, SPEC.files.lod);
const POSTER_PATH = path.join(HERE, SPEC.files.poster);
const EXPERIENCE_ANCHORS = new Map(SPEC.experience_mapping.anchors.map((anchor) => [anchor.hotspot_id, anchor]));
const INTERIOR_ANCHOR = EXPERIENCE_ANCHORS.get("representative-interior-concept");
const ARRIVAL_ANCHOR = EXPERIENCE_ANCHORS.get("facility-arrival-concept");
const LANDSCAPE_ANCHOR = EXPERIENCE_ANCHORS.get("facility-landscaped-open-space-concept");
if (!INTERIOR_ANCHOR || !ARRIVAL_ANCHOR || !LANDSCAPE_ANCHOR || EXPERIENCE_ANCHORS.size !== 3) throw new Error("Exact three-anchor experience mapping is required.");

function pad4(value) { return (4 - (value % 4)) % 4; }
function rgba(hex) {
  const raw = hex.replace("#", "");
  return [0, 2, 4].map((offset) => Number.parseInt(raw.slice(offset, offset + 2), 16) / 255).concat(1);
}

const MATERIALS = [
  ["white mineral podium", "#e8e2d6", 0.01, 0.74],
  ["white mineral tower", "#eeeae1", 0.01, 0.56],
  ["clear blue-grey glass", "#789b9f", 0.12, 0.24],
  ["warm aluminium fins", "#b9a078", 0.16, 0.34],
  ["white balcony frames", "#f5f2eb", 0.01, 0.48],
  ["landscape", "#557760", 0, 0.9],
  ["north reference", "#b78432", 0, 0.6],
  ["punched window shadow", "#314e51", 0.06, 0.31],
  ["illustrative interior hotspot", "#e4b44f", 0.08, 0.28],
  ["illustrative shared-space hotspot", "#69c4b0", 0.05, 0.3]
].map(([name, color, metallic, roughness]) => ({
  name,
  pbrMetallicRoughness: { baseColorFactor: rgba(color), metallicFactor: metallic, roughnessFactor: roughness }
}));

function geometryBucket(name, material, extras = null) {
  return { name, material, extras, positions: [], normals: [], indices: [], boxes: 0 };
}

function addBox(bucket, cx, cy, cz, sx, sy, sz) {
  const x0 = cx - sx / 2, x1 = cx + sx / 2;
  const y0 = cy - sy / 2, y1 = cy + sy / 2;
  const z0 = cz - sz / 2, z1 = cz + sz / 2;
  const faces = [
    [[0, 0, 1], [[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]]],
    [[0, 0,-1], [[x1,y0,z0],[x0,y0,z0],[x0,y1,z0],[x1,y1,z0]]],
    [[1, 0, 0], [[x1,y0,z1],[x1,y0,z0],[x1,y1,z0],[x1,y1,z1]]],
    [[-1,0, 0], [[x0,y0,z0],[x0,y0,z1],[x0,y1,z1],[x0,y1,z0]]],
    [[0, 1, 0], [[x0,y1,z1],[x1,y1,z1],[x1,y1,z0],[x0,y1,z0]]],
    [[0,-1, 0], [[x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1]]]
  ];
  for (const [normal, vertices] of faces) {
    const base = bucket.positions.length / 3;
    for (const vertex of vertices) {
      bucket.positions.push(...vertex);
      bucket.normals.push(...normal);
    }
    bucket.indices.push(base, base + 1, base + 2, base, base + 2, base + 3);
  }
  bucket.boxes += 1;
}

function hotspotExtras(anchor) {
  return {
    hotspot_id: anchor.hotspot_id,
    tool_id: anchor.tool_id,
    open_surface_tool_id: anchor.open_surface_tool_id,
    scene_ids: anchor.scene_ids,
    model_component_ids: anchor.model_component_ids,
    illustrative_zone_id: anchor.illustrative_zone_id,
    mapping_state: SPEC.experience_mapping.active_state,
    future_verified_state: SPEC.experience_mapping.future_verified_state,
    coordinate_space: SPEC.experience_mapping.coordinate_space,
    position: anchor.position,
    surface_normal: anchor.surface_normal,
    visual_offset_along_normal_m: anchor.visual_offset_along_normal_m,
    confidence: anchor.confidence,
    placement_confidence: anchor.placement_confidence,
    evidence_basis: anchor.evidence_basis,
    ambiguity: anchor.ambiguity,
    prohibited_inferences: anchor.prohibited_inferences,
    real_world_orientation_calibrated: false,
    source_cited: false,
    decision_grade: false
  };
}

function addHotspotMarker(bucket, anchor) {
  const centre = anchor.position.map((value, index) => value + anchor.surface_normal[index] * anchor.visual_offset_along_normal_m);
  if (Math.abs(anchor.surface_normal[1]) > 0.5) {
    addBox(bucket, centre[0], centre[1], centre[2], 3.4, 0.42, 0.72);
    addBox(bucket, centre[0], centre[1], centre[2], 0.72, 0.42, 3.4);
  } else {
    addBox(bucket, centre[0], centre[1], centre[2], 3.4, 0.72, 0.42);
    addBox(bucket, centre[0], centre[1], centre[2], 0.72, 3.4, 0.42);
  }
}

function sceneHotspot(anchor) {
  return Object.assign({
    kind: anchor.kind,
    experience_kind: anchor.experience_kind,
    representation_kind: "owner_approved_illustration",
    owner_decision_id: SPEC.experience_owner_decision_id,
    version: SPEC.experience_version,
    effective_at: SPEC.experience_effective_at,
    expires_at: SPEC.experience_expires_at
  }, hotspotExtras(anchor));
}

function addFacadeGrid(bucket, { cx, baseY, cz, width, depth, levels, levelHeight, frontColumns, sideColumns }) {
  const panelHeight = levelHeight * 0.68;
  const frontWidth = width / frontColumns * 0.7;
  const sideWidth = depth / sideColumns * 0.7;
  for (let floor = 0; floor < levels; floor += 1) {
    const y = baseY + floor * levelHeight + levelHeight * 0.52;
    for (let column = 0; column < frontColumns; column += 1) {
      const x = cx - width / 2 + (column + 0.5) * width / frontColumns;
      addBox(bucket, x, y, cz + depth / 2 + 0.07, frontWidth, panelHeight, 0.12);
      addBox(bucket, x, y, cz - depth / 2 - 0.07, frontWidth, panelHeight, 0.12);
    }
    for (let column = 0; column < sideColumns; column += 1) {
      const z = cz - depth / 2 + (column + 0.5) * depth / sideColumns;
      addBox(bucket, cx + width / 2 + 0.07, y, z, 0.12, panelHeight, sideWidth);
      addBox(bucket, cx - width / 2 - 0.07, y, z, 0.12, panelHeight, sideWidth);
    }
  }
}

function addPunchedWindowZ(glassBucket, frameBucket, cx, cy, cz, width, height, depth) {
  const frame = 0.11;
  addBox(glassBucket, cx, cy, cz, width, height, depth);
  addBox(frameBucket, cx - width / 2 - frame / 2, cy, cz, frame, height + frame * 2, depth * 1.35);
  addBox(frameBucket, cx + width / 2 + frame / 2, cy, cz, frame, height + frame * 2, depth * 1.35);
  addBox(frameBucket, cx, cy - height / 2 - frame / 2, cz, width, frame, depth * 1.35);
  addBox(frameBucket, cx, cy + height / 2 + frame / 2, cz, width, frame, depth * 1.35);
}

function addPunchedWindowX(glassBucket, frameBucket, cx, cy, cz, width, height, depth) {
  const frame = 0.11;
  addBox(glassBucket, cx, cy, cz, depth, height, width);
  addBox(frameBucket, cx, cy, cz - width / 2 - frame / 2, depth * 1.35, height + frame * 2, frame);
  addBox(frameBucket, cx, cy, cz + width / 2 + frame / 2, depth * 1.35, height + frame * 2, frame);
  addBox(frameBucket, cx, cy - height / 2 - frame / 2, cz, depth * 1.35, frame, width);
  addBox(frameBucket, cx, cy + height / 2 + frame / 2, cz, depth * 1.35, frame, width);
}

function buildHd() {
  const groups = [
    geometryBucket("Podium_Double_Level", 0),
    geometryBucket("Tower_28_Level_Massing", 1),
    geometryBucket("Boutique_A_13_Level", 1),
    geometryBucket("Boutique_B_13_Level", 1),
    geometryBucket("Glass_Terrace_Strips", 2),
    geometryBucket("Champagne_Fins", 3),
    geometryBucket("Balcony_Bands", 4),
    geometryBucket("Landscape_Terraces", 5),
    geometryBucket("North_Reference", 6),
    geometryBucket("Punched_Window_Shadow", 7),
    geometryBucket("Experience_Hotspot_Interior_Illustrative", 8, hotspotExtras(INTERIOR_ANCHOR)),
    geometryBucket("Experience_Hotspot_Arrival_Illustrative", 9, hotspotExtras(ARRIVAL_ANCHOR)),
    geometryBucket("Experience_Hotspot_Landscaped_Open_Space_Illustrative", 9, hotspotExtras(LANDSCAPE_ANCHOR))
  ];
  const [podium, tower, boutiqueA, boutiqueB, panels, fins, bands, landscape, north, windows, interiorHotspot, arrivalHotspot, landscapeHotspot] = groups;
  addBox(podium, 0, 4.2, 0, 70, 8.4, 46);
  addBox(podium, 0, 8.7, 0, 64, 0.6, 40);
  // The official project renders support a slender white tower with a
  // punched-window solid side, one stacked glass/terrace facade, and a
  // stepped crown. Exact dimensions remain illustrative.
  addBox(tower, 12, 45.2, -4, 18, 72, 18);
  addBox(tower, 11, 85.0, -4, 16, 12, 17);
  addBox(tower, 8.8, 92.0, -4, 11.5, 2, 15.5);
  // Paired boutique blocks are kept visibly separate and receive recessed
  // roof terraces rather than reading as one slab.
  addBox(boutiqueA, -19, 27.0, 8.5, 18, 36, 15);
  addBox(boutiqueA, -20.2, 46.4, 8.5, 14.5, 2.8, 13);
  addBox(boutiqueB, -18, 27.0, -10.5, 18, 36, 15);
  addBox(boutiqueB, -19.2, 46.4, -10.5, 14.5, 2.8, 13);

  // Tower glass/terrace strip: a single vertical stack on the supported
  // facade family, with a solid punched-window field elsewhere.
  for (let floor=0; floor<28; floor+=1) {
    const y=9.2+floor*3+1.52;
    addBox(panels, 16.0, y, 5.08, 7.2, 2.3, 0.18);
    if (floor<24 || floor>25) addBox(bands, 16.0, 9.2+floor*3+2.88, 5.65, 8.4, 0.18, 1.28);
    for(let column=0;column<5;column+=1){
      const x=4.5+column*2.55;
      addPunchedWindowZ(windows,bands,x,y,5.10,1.08,1.65,0.14);
      addPunchedWindowZ(windows,bands,x,y,-13.10,1.08,1.65,0.14);
    }
    for(let column=0;column<4;column+=1){
      const z=-10.8+column*4.45;
      addPunchedWindowX(windows,bands,3.0,y,z,1.18,1.65,0.14);
    }
  }

  for (const building of [{cx:-19,cz:8.5,w:18,d:15},{cx:-18,cz:-10.5,w:18,d:15}]) {
    for (let floor=0;floor<13;floor+=1) {
      const y=8.8+floor*3+1.5;
      // glass balcony stacks toward the shared frontage
      addBox(panels,building.cx+3.5,y,building.cz+building.d/2+0.08,7.2,2.25,0.16);
      addBox(bands,building.cx+3.5,8.8+floor*3+2.87,building.cz+building.d/2+0.62,8.2,0.16,1.12);
      // narrow vertical slots on the mineral facade
      for(let column=0;column<5;column+=1){
        const x=building.cx-building.w*.42+column*2.25;
        addPunchedWindowZ(windows,bands,x,y,building.cz-building.d/2-0.08,.72,1.74,.14);
      }
      for(let column=0;column<3;column+=1){
        const z=building.cz-building.d*.3+column*building.d*.3;
        addPunchedWindowX(windows,bands,building.cx-building.w/2-.08,y,z,.72,1.74,.14);
      }
    }
  }

  // Warm recessed fins articulate the glass stacks only; they are not a
  // claim about the final cladding specification.
  for(let fin=0;fin<5;fin+=1)addBox(fins,12.8+fin*1.6,50.5,5.72,.13,82,.62);
  for(const building of [{cx:-19,cz:8.5},{cx:-18,cz:-10.5}])for(let fin=0;fin<4;fin+=1)addBox(fins,building.cx+1+fin*1.7,28.2,building.cz+8.12,.12,38,.48);
  for (let level = 0; level < 2; level += 1) {
    const y = 1.25 + level * 3.8;
    for (let i = 0; i < 24; i += 1) {
      const x = -33.5 + i * 67 / 23;
      addBox(panels, x, y, 23.08, 1.9, 2.6, 0.14);
      addBox(panels, x, y, -23.08, 1.9, 2.6, 0.14);
    }
    for (let i = 0; i < 16; i += 1) {
      const z = -21.5 + i * 43 / 15;
      addBox(panels, 35.08, y, z, 0.14, 2.6, 1.8);
      addBox(panels, -35.08, y, z, 0.14, 2.6, 1.8);
    }
  }
  for (const terrace of [[-29,9.1,17,14,1,8],[-30,9.1,-15,12,1,7],[27,9.1,14,12,1,8],[27,9.1,-15,11,1,8]]) addBox(landscape, ...terrace);
  for (let planter = 0; planter < 24; planter += 1) {
    const angle = planter / 24 * Math.PI * 2;
    addBox(landscape, Math.cos(angle) * 28, 9.9, Math.sin(angle) * 17, 1.6, 1.2, 1.6);
  }
  addBox(north, 0, 0.12, 31, 1.2, 0.24, 13);
  addBox(north, 0, 0.22, 38, 5.5, 0.25, 1.1);
  addBox(north, -2.2, 0.22, 35.9, 1.1, 0.25, 5.2);
  addBox(north, 2.2, 0.22, 35.9, 1.1, 0.25, 5.2);
  // These crosses are explicit owner-approved illustrative activation anchors.
  // Their visible marker offset only clears authored surfaces; it is not a
  // source-cited room/facility location and never unlocks inventory.
  addHotspotMarker(interiorHotspot, INTERIOR_ANCHOR);
  addHotspotMarker(arrivalHotspot, ARRIVAL_ANCHOR);
  addHotspotMarker(landscapeHotspot, LANDSCAPE_ANCHOR);
  return groups;
}

function buildLod() {
  const groups = [
    geometryBucket("Podium_Double_Level_LOD", 0),
    geometryBucket("Tower_28_Level_Massing_LOD", 1),
    geometryBucket("Boutique_A_13_Level_LOD", 1),
    geometryBucket("Boutique_B_13_Level_LOD", 1),
    geometryBucket("Landscape_Terraces_LOD", 5),
    geometryBucket("North_Reference_LOD", 6),
    geometryBucket("Experience_Hotspot_Interior_Illustrative_LOD", 8, hotspotExtras(INTERIOR_ANCHOR)),
    geometryBucket("Experience_Hotspot_Arrival_Illustrative_LOD", 9, hotspotExtras(ARRIVAL_ANCHOR)),
    geometryBucket("Experience_Hotspot_Landscaped_Open_Space_Illustrative_LOD", 9, hotspotExtras(LANDSCAPE_ANCHOR))
  ];
  addBox(groups[0], 0, 4.2, 0, 70, 8.4, 46);
  addBox(groups[1], 12, 45.2, -4, 18, 72, 18);
  addBox(groups[1], 11, 85, -4, 16, 12, 17);
  addBox(groups[2], -19, 27, 8.5, 18, 36, 15);
  addBox(groups[3], -18, 27, -10.5, 18, 36, 15);
  addBox(groups[4], 0, 8.8, 0, 62, 0.8, 38);
  addBox(groups[5], 0, 0.12, 34, 1.2, 0.24, 12);
  addHotspotMarker(groups[6], INTERIOR_ANCHOR);
  addHotspotMarker(groups[7], ARRIVAL_ANCHOR);
  addHotspotMarker(groups[8], LANDSCAPE_ANCHOR);
  return groups;
}

function writeGlb(target, groups, label) {
  const chunks = [];
  const views = [];
  const accessors = [];
  function pushTyped(array, Type, targetKind) {
    const typed = new Type(array);
    const buffer = Buffer.from(typed.buffer, typed.byteOffset, typed.byteLength);
    const byteOffset = chunks.reduce((sum, item) => sum + item.length, 0);
    chunks.push(buffer);
    if (pad4(buffer.length)) chunks.push(Buffer.alloc(pad4(buffer.length)));
    const viewIndex = views.push({ buffer:0, byteOffset, byteLength:buffer.length, target:targetKind }) - 1;
    return viewIndex;
  }
  const json = {
    asset: { version:"2.0", generator:"Nadlan deterministic Einstein illustrative massing v1", extras:{ project_contract_id:SPEC.project_contract_id, representation_kind:SPEC.representation_kind, decision_grade:false, owner_publication_permission:true, release_gate_state:"private_stage", owner_decision_id:SPEC.owner_decision_id, effective_at:SPEC.effective_at, expires_at:SPEC.expires_at } },
    scene: 0,
    scenes: [{ name:label, nodes:[], extras:{ north_degrees:0, north_axis:"+Z", up_axis:"+Y", units:"metres", calibration_id:SPEC.calibration.calibration_id, placement_calibration_state:"not_municipally_crosswalked", concept_hotspots:SPEC.experience_mapping.anchors.map(sceneHotspot) } }],
    nodes: [], meshes: [], materials: MATERIALS, accessors, bufferViews:views, buffers:[]
  };
  for (const group of groups.filter((item) => item.indices.length)) {
    const positionView = pushTyped(group.positions, Float32Array, 34962);
    const normalView = pushTyped(group.normals, Float32Array, 34962);
    const indexView = pushTyped(group.indices, Uint32Array, 34963);
    const xs=[],ys=[],zs=[];
    for(let i=0;i<group.positions.length;i+=3){xs.push(group.positions[i]);ys.push(group.positions[i+1]);zs.push(group.positions[i+2]);}
    const positionAccessor = accessors.push({ bufferView:positionView, componentType:5126, count:group.positions.length/3, type:"VEC3", min:[Math.min(...xs),Math.min(...ys),Math.min(...zs)], max:[Math.max(...xs),Math.max(...ys),Math.max(...zs)] }) - 1;
    const normalAccessor = accessors.push({ bufferView:normalView, componentType:5126, count:group.normals.length/3, type:"VEC3" }) - 1;
    const indexAccessor = accessors.push({ bufferView:indexView, componentType:5125, count:group.indices.length, type:"SCALAR", min:[Math.min(...group.indices)], max:[Math.max(...group.indices)] }) - 1;
    const meshExtras = Object.assign({ illustrative_component:true, generated_boxes:group.boxes }, group.extras || {});
    const meshIndex = json.meshes.push({ name:group.name, extras:meshExtras, primitives:[{ attributes:{POSITION:positionAccessor,NORMAL:normalAccessor}, indices:indexAccessor, material:group.material, mode:4 }] }) - 1;
    const nodeIndex = json.nodes.push({ name:group.name, mesh:meshIndex, extras:group.extras || undefined }) - 1;
    json.scenes[0].nodes.push(nodeIndex);
  }
  const binary = Buffer.concat(chunks);
  json.buffers.push({ byteLength:binary.length });
  let jsonChunk = Buffer.from(JSON.stringify(json), "utf8");
  if (pad4(jsonChunk.length)) jsonChunk = Buffer.concat([jsonChunk, Buffer.alloc(pad4(jsonChunk.length), 0x20)]);
  let binChunk = binary;
  if (pad4(binChunk.length)) binChunk = Buffer.concat([binChunk, Buffer.alloc(pad4(binChunk.length))]);
  const header = Buffer.alloc(12), jsonHeader=Buffer.alloc(8), binHeader=Buffer.alloc(8);
  const total=12+8+jsonChunk.length+8+binChunk.length;
  header.writeUInt32LE(0x46546c67,0);header.writeUInt32LE(2,4);header.writeUInt32LE(total,8);
  jsonHeader.writeUInt32LE(jsonChunk.length,0);jsonHeader.writeUInt32LE(0x4e4f534a,4);
  binHeader.writeUInt32LE(binChunk.length,0);binHeader.writeUInt32LE(0x004e4942,4);
  fs.writeFileSync(target,Buffer.concat([header,jsonHeader,jsonChunk,binHeader,binChunk]));
}

function writePoster() {
  const towerWindows = Array.from({length:18},(_,row)=>Array.from({length:5},(_,column)=>{const x=590+column*22,y=158+row*15.2-column*1.9;return `<path d="M${x} ${y}l8-.7v8.6l-8 .8Z"/>`;}).join("")).join("");
  const towerTerraces = Array.from({length:15},(_,i)=>`<path d="M705 ${151+i*18.2}L795 ${143+i*17.6}"/>`).join("");
  const northWindows = Array.from({length:10},(_,row)=>Array.from({length:4},(_,column)=>{const x=150+column*25,y=320+row*16-column*1.8;return `<path d="M${x} ${y}l8-.7v9l-8 .7Z"/>`;}).join("")).join("");
  const southWindows = Array.from({length:10},(_,row)=>Array.from({length:4},(_,column)=>{const x=350+column*24,y=294+row*16-column*1.7;return `<path d="M${x} ${y}l8-.7v9l-8 .7Z"/>`;}).join("")).join("");
  const northTerraces = Array.from({length:9},(_,i)=>`<path d="M248 ${305+i*18}L325 ${298+i*17.8}"/>`).join("");
  const southTerraces = Array.from({length:9},(_,i)=>`<path d="M443 ${282+i*18}L517 ${275+i*17.8}"/>`).join("");
  const shopfronts = Array.from({length:11},(_,i)=>`<path d="M147 ${493+i*.6}L147 ${548+i*.6}M${147+i*62} 485L${147+i*62} 538"/>`).join("");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="640" viewBox="0 0 960 640">
  <defs>
    <linearGradient id="sky" x2="0" y2="1"><stop stop-color="#b9d8d5"/><stop offset=".6" stop-color="#e7e6d9"/><stop offset="1" stop-color="#d0b98b"/></linearGradient>
    <linearGradient id="tower" x2="1" y2="1"><stop stop-color="#fffdf8"/><stop offset=".58" stop-color="#e8e8e3"/><stop offset="1" stop-color="#c9d0cd"/></linearGradient>
    <linearGradient id="boutique" x2="1"><stop stop-color="#fbfaf5"/><stop offset="1" stop-color="#d7ddda"/></linearGradient>
    <linearGradient id="glass" x2="1" y2="1"><stop stop-color="#496d70"/><stop offset=".55" stop-color="#8eadae"/><stop offset="1" stop-color="#c3d2ce"/></linearGradient>
    <linearGradient id="stone" x2="0" y2="1"><stop stop-color="#eee9dd"/><stop offset="1" stop-color="#bdb5a5"/></linearGradient>
    <radialGradient id="sun"><stop stop-color="#f7dc91"/><stop offset="1" stop-color="#d9aa4e"/></radialGradient>
    <filter id="shadow" x="-30%" y="-30%" width="170%" height="180%"><feDropShadow dx="0" dy="16" stdDeviation="13" flood-color="#17312f" flood-opacity=".24"/></filter>
    <filter id="glow"><feGaussianBlur stdDeviation="9"/></filter>
  </defs>
  <rect width="960" height="640" fill="url(#sky)"/>
  <circle cx="812" cy="96" r="58" fill="#f8d985" opacity=".28" filter="url(#glow)"/><circle cx="812" cy="96" r="35" fill="url(#sun)" opacity=".86"/>
  <path d="M0 474L960 395V640H0Z" fill="#769082"/><path d="M0 520L960 445V640H0Z" fill="#4d6d61" opacity=".4"/>
  <g filter="url(#shadow)">
    <path d="M108 438L791 383L872 425L184 491Z" fill="#e2d7c2"/>
    <path d="M108 438L184 491V570L108 518Z" fill="#988a70"/>
    <path d="M184 491L872 425V510L184 570Z" fill="url(#stone)"/>
    <path d="M193 497L852 437V485L193 542Z" fill="url(#glass)" opacity=".92"/>
    <g stroke="#e6ddd0" stroke-width="3" opacity=".92">${shopfronts}</g>
    <path d="M487 463L578 454L605 466L513 477Z" fill="#e7d7b4"/><path d="M513 477L605 466V486L513 498Z" fill="#9a7641"/>

    <path d="M112 286L304 270L334 289L139 307Z" fill="#a7c1b9"/>
    <path d="M112 286L139 307V481L112 463Z" fill="#adb7b3"/>
    <path d="M139 307L334 289V474L139 493Z" fill="url(#boutique)"/>
    <path d="M334 289L304 270V455L334 474Z" fill="#9fa9a5"/>
    <path d="M240 298L327 290V469L240 478Z" fill="url(#glass)"/>
    <g fill="#4c6769" opacity=".95">${northWindows}</g>
    <g fill="none" stroke="#f8f4e9" stroke-width="5" opacity=".92">${northTerraces}</g>
    <path d="M132 307L329 288" stroke="#ffffff" stroke-width="9"/>

    <path d="M310 255L493 238L525 257L338 276Z" fill="#bad0c9"/>
    <path d="M310 255L338 276V459L310 440Z" fill="#a7b0ad"/>
    <path d="M338 276L525 257V452L338 471Z" fill="url(#boutique)"/>
    <path d="M525 257L493 238V432L525 452Z" fill="#9ba6a2"/>
    <path d="M437 267L518 259V447L437 455Z" fill="url(#glass)"/>
    <g fill="#496467" opacity=".95">${southWindows}</g>
    <g fill="none" stroke="#faf6ec" stroke-width="5" opacity=".94">${southTerraces}</g>
    <path d="M331 276L520 257" stroke="#ffffff" stroke-width="9"/>

    <path d="M535 112L758 92L809 119L579 142Z" fill="#b5d1ca"/>
    <path d="M535 112L579 142V443L535 413Z" fill="#aab4b0"/>
    <path d="M579 142L809 119V432L579 458Z" fill="url(#tower)"/>
    <path d="M809 119L758 92V399L809 432Z" fill="#929e9a"/>
    <path d="M698 131L804 120V431L698 443Z" fill="url(#glass)"/>
    <g fill="#486568" opacity=".96">${towerWindows}</g>
    <g fill="none" stroke="#fffaf0" stroke-width="5" opacity=".94">${towerTerraces}</g>
    <path d="M571 142L804 118" stroke="#ffffff" stroke-width="11"/>
    <path d="M565 130L753 112L753 92L535 112Z" fill="#f7f4eb" opacity=".95"/>
  </g>
  <path d="M63 560C222 541 329 554 467 535C628 513 746 482 916 487" fill="none" stroke="#f5efe1" stroke-width="10" stroke-linecap="round"/>
  <path d="M83 602C210 571 329 588 442 563" fill="none" stroke="#b7d1c4" stroke-width="18" stroke-linecap="round" opacity=".62"/>
  <g fill="#2f6254">${[92,125,667,705,858,891].map((x,i)=>`<circle cx="${x}" cy="${510+(i%2)*28}" r="${13+(i%3)*3}"/><rect x="${x-2}" y="${520+(i%2)*28}" width="4" height="24" fill="#7f6748"/>`).join("")}</g>
  <g fill="#d7b768"><circle cx="474" cy="520" r="6"/><circle cx="489" cy="518" r="6"/><circle cx="504" cy="516" r="6"/></g>
  </svg>`;
  const temp = path.join(HERE, ".poster-source.svg");
  fs.writeFileSync(temp, svg, "utf8");
  const candidates = process.platform === "win32" ? ["magick.exe", "C:\\Program Files\\ImageMagick-7.1.2-Q16-HDRI\\magick.exe"] : ["magick"];
  let converted = false;
  for (const executable of candidates) {
    const result = spawnSync(executable, [temp, "-strip", "-quality", "78", "-define", "webp:method=5", POSTER_PATH], { stdio:"pipe" });
    if (result.status === 0 && fs.existsSync(POSTER_PATH)) { converted = true; break; }
  }
  fs.rmSync(temp, { force:true });
  if (!converted) throw new Error("ImageMagick is required to create poster.webp without adding a dependency.");
}

fs.mkdirSync(HERE,{recursive:true});
writeGlb(HD_PATH,buildHd(),"Einstein_33A_HD_Illustrative_Massing");
writeGlb(LOD_PATH,buildLod(),"Einstein_33A_LOD_Illustrative_Massing");
writePoster();
console.log(JSON.stringify({ok:true,files:[SPEC.files.hd,SPEC.files.lod,SPEC.files.poster].map((file)=>({file,bytes:fs.statSync(path.join(HERE,file)).size}))},null,2));
