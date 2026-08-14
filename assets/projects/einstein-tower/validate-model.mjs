/** Standalone structural/truth validator for the generated Einstein GLBs. */
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const HERE=path.dirname(fileURLToPath(import.meta.url));
const spec=JSON.parse(fs.readFileSync(path.join(HERE,"model-spec.json"),"utf8"));
function invariant(condition,message){if(!condition)throw new Error(message);}
function sha256(bytes){return crypto.createHash("sha256").update(bytes).digest("hex");}
function parseGlb(file){
  const bytes=fs.readFileSync(file),view=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength);
  invariant(view.getUint32(0,true)===0x46546c67,"invalid GLB magic: "+file);
  invariant(view.getUint32(4,true)===2,"GLB must be version 2: "+file);
  invariant(view.getUint32(8,true)===bytes.length,"GLB length mismatch: "+file);
  let offset=12,json=null,binLength=0;
  while(offset<bytes.length){const length=view.getUint32(offset,true),type=view.getUint32(offset+4,true);invariant(offset+8+length<=bytes.length,"chunk outside GLB");if(type===0x4e4f534a)json=JSON.parse(bytes.subarray(offset+8,offset+8+length).toString("utf8").trim());if(type===0x004e4942)binLength=length;offset+=8+length;}
  invariant(json&&binLength>0,"GLB requires JSON and BIN chunks");
  let triangles=0,vertices=0;
  for(const mesh of json.meshes||[])for(const primitive of mesh.primitives||[]){invariant((primitive.mode??4)===4,"only triangle primitives are allowed");const position=json.accessors[primitive.attributes.POSITION];invariant(position&&position.type==="VEC3","POSITION accessor missing");vertices+=position.count;const indices=json.accessors[primitive.indices];invariant(indices&&indices.type==="SCALAR"&&indices.count%3===0,"indexed triangle accessor invalid");triangles+=indices.count/3;}
  return {file:path.basename(file),bytes:bytes.length,sha256:crypto.createHash("sha256").update(bytes).digest("hex"),triangles,vertices,meshes:(json.meshes||[]).map((mesh)=>mesh.name),meshRecords:(json.meshes||[]).map((mesh)=>{const positionAccessor=json.accessors?.[mesh.primitives?.[0]?.attributes?.POSITION];return{name:mesh.name,extras:mesh.extras||{},bounds:positionAccessor&&Array.isArray(positionAccessor.min)&&Array.isArray(positionAccessor.max)?{min:positionAccessor.min,max:positionAccessor.max}:null};}),assetExtras:json.asset.extras||{},sceneExtras:(json.scenes||[])[json.scene||0]?.extras||{}};
}
const hd=parseGlb(path.join(HERE,spec.files.hd));
const lod=parseGlb(path.join(HERE,spec.files.lod));
const poster=fs.readFileSync(path.join(HERE,spec.files.poster));
const experienceManifestPath=path.join(HERE,spec.files.experience_manifest||"");
invariant(spec.files.experience_manifest==="experience/manifest.json","experience manifest path must be canonical");
const experience=JSON.parse(fs.readFileSync(experienceManifestPath,"utf8"));
invariant(hd.triangles>=spec.acceptance.minimum_hd_triangles,`HD triangles ${hd.triangles} below ${spec.acceptance.minimum_hd_triangles}`);
invariant(hd.bytes<=spec.acceptance.maximum_hd_bytes,"HD exceeds compact size gate");
invariant(lod.triangles>0&&lod.triangles<hd.triangles,"LOD must be nonempty and simpler than HD");
invariant(lod.bytes<=spec.acceptance.maximum_lod_bytes,"LOD exceeds compact size gate");
invariant(poster.length<=spec.acceptance.maximum_poster_bytes,"poster exceeds compact size gate");
for(const model of [hd,lod]){
  invariant(model.assetExtras.project_contract_id===spec.project_contract_id,"project identity mismatch");
  invariant(model.assetExtras.owner_decision_id===spec.owner_decision_id,"massing decision mismatch");
  invariant(model.assetExtras.representation_kind==="owner_approved_illustration"&&model.assetExtras.decision_grade===false,"truth metadata mismatch");
  invariant(model.assetExtras.owner_publication_permission===true&&model.assetExtras.release_gate_state==="private_stage","owner permission/release gate mismatch");
  invariant(model.assetExtras.effective_at===spec.effective_at&&model.assetExtras.expires_at===spec.expires_at,"representation dates mismatch");
  invariant(model.sceneExtras.north_degrees===0&&model.sceneExtras.north_axis==="+Z"&&model.sceneExtras.up_axis==="+Y","north/up calibration mismatch");
  invariant(model.sceneExtras.placement_calibration_state==="not_municipally_crosswalked","site placement must remain uncalibrated");
  invariant(Array.isArray(model.sceneExtras.concept_hotspots)&&model.sceneExtras.concept_hotspots.length===3,"exact three interior/facility concept hotspots required");
  for(const hotspot of model.sceneExtras.concept_hotspots){
    invariant(hotspot.mapping_state===spec.experience_mapping.active_state&&hotspot.decision_grade===false,"concept hotspot illustrative mapping mismatch");
    invariant(hotspot.open_surface_tool_id==="interior","every experience hotspot must open the single Interior surface");
    invariant(hotspot.future_verified_state===spec.experience_mapping.future_verified_state&&hotspot.source_cited===false,"illustrative and future source-cited mapping lanes must remain distinct");
    invariant(hotspot.coordinate_space===spec.experience_mapping.coordinate_space&&Array.isArray(hotspot.position)&&hotspot.position.length===3&&hotspot.position.every(Number.isFinite),"concept hotspot position contract invalid");
    invariant(Array.isArray(hotspot.surface_normal)&&hotspot.surface_normal.length===3&&hotspot.surface_normal.every(Number.isFinite)&&Math.abs(Math.hypot(...hotspot.surface_normal)-1)<0.0001,"concept hotspot surface normal invalid");
    invariant(Number.isFinite(hotspot.visual_offset_along_normal_m)&&hotspot.visual_offset_along_normal_m>=0&&hotspot.visual_offset_along_normal_m<=1,"concept hotspot visual offset invalid");
    invariant(hotspot.real_world_orientation_calibrated===false&&hotspot.confidence==="model_zone_fit_high__source_spatial_confidence_none","concept hotspot confidence/orientation mismatch");
    invariant(Array.isArray(hotspot.scene_ids)&&hotspot.scene_ids.length>0&&Array.isArray(hotspot.model_component_ids)&&hotspot.model_component_ids.length>0&&typeof hotspot.illustrative_zone_id==="string"&&hotspot.illustrative_zone_id,"concept hotspot binding incomplete");
    invariant(Array.isArray(hotspot.evidence_basis?.primary_reference_ids)&&hotspot.evidence_basis.primary_reference_ids.length>0&&typeof hotspot.evidence_basis.supports==="string"&&typeof hotspot.ambiguity==="string"&&Array.isArray(hotspot.prohibited_inferences)&&hotspot.prohibited_inferences.length>0,"concept hotspot evidence/ambiguity incomplete");
    invariant(hotspot.owner_decision_id===spec.experience_owner_decision_id,"concept hotspot owner decision mismatch");
    invariant(hotspot.representation_kind==="owner_approved_illustration"&&hotspot.version===spec.experience_version,"concept hotspot illustration/version mismatch");
    invariant(hotspot.effective_at===spec.experience_effective_at&&hotspot.expires_at===spec.experience_expires_at,"concept hotspot decision dates mismatch");
  }
}
const hotspotKinds=new Map(hd.sceneExtras.concept_hotspots.map((hotspot)=>[hotspot.hotspot_id,hotspot.experience_kind]));
invariant(hotspotKinds.get("representative-interior-concept")==="representative_concept"&&hotspotKinds.get("facility-arrival-concept")==="selectable_concept_gallery"&&hotspotKinds.get("facility-landscaped-open-space-concept")==="selectable_concept_gallery","concept hotspot experience kinds mismatch");
const expectedAnchors=new Map(spec.experience_mapping.anchors.map((anchor)=>[anchor.hotspot_id,anchor]));
const expectedAnchorConfidence=new Map([
  ["representative-interior-concept",{zone:0.68,exact_point:0.18}],
  ["facility-arrival-concept",{zone:0.63,exact_point:0.20}],
  ["facility-landscaped-open-space-concept",{zone:0.86,exact_point:0.24}]
]);
invariant(expectedAnchors.size===3&&spec.experience_mapping.source_cited===false&&spec.experience_mapping.decision_grade===false&&spec.experience_mapping.real_world_orientation_calibrated===false,"experience mapping spec invalid");
for(const [hotspotId,anchor] of expectedAnchors){
  invariant(anchor.confidence==="model_zone_fit_high__source_spatial_confidence_none"&&JSON.stringify(anchor.placement_confidence)===JSON.stringify(expectedAnchorConfidence.get(hotspotId)),"experience mapping confidence mismatch");
}
for(const model of [hd,lod]){
  for(const hotspot of model.sceneExtras.concept_hotspots){
    const expected=expectedAnchors.get(hotspot.hotspot_id);
    invariant(expected&&hotspot.tool_id===expected.tool_id&&hotspot.open_surface_tool_id===expected.open_surface_tool_id&&expected.open_surface_tool_id==="interior"&&JSON.stringify(hotspot.position)===JSON.stringify(expected.position)&&JSON.stringify(hotspot.surface_normal)===JSON.stringify(expected.surface_normal)&&JSON.stringify(hotspot.scene_ids)===JSON.stringify(expected.scene_ids)&&JSON.stringify(hotspot.placement_confidence)===JSON.stringify(expected.placement_confidence),"concept hotspot anchor mismatch");
  }
  const markerRecords=model.meshRecords.filter((mesh)=>/^Experience_Hotspot_/.test(mesh.name));
  invariant(markerRecords.length===3,"exactly three illustrative hotspot meshes required");
  for(const marker of markerRecords){
    const expected=expectedAnchors.get(marker.extras.hotspot_id);
    invariant(expected&&marker.extras.tool_id===expected.tool_id&&marker.extras.open_surface_tool_id===expected.open_surface_tool_id,"hotspot mesh identity mismatch");
    invariant(marker.extras.mapping_state===spec.experience_mapping.active_state&&marker.extras.source_cited===false&&marker.extras.decision_grade===false,"hotspot mesh truth metadata mismatch");
    invariant(marker.bounds&&marker.bounds.min.length===3&&marker.bounds.max.length===3,"hotspot mesh bounds missing");
    const centre=marker.bounds.min.map((minimum,index)=>(minimum+marker.bounds.max[index])/2);
    const displayPosition=expected.position.map((value,index)=>value+expected.surface_normal[index]*expected.visual_offset_along_normal_m);
    invariant(centre.every((value,index)=>Math.abs(value-displayPosition[index])<0.0001),"hotspot mesh geometry and declared display position differ");
    invariant(marker.bounds.max.every((maximum,index)=>maximum-marker.bounds.min[index]>=0.4),"hotspot mesh is not visibly hit-testable");
  }
}
for(const required of ["Podium_Double_Level","Tower_28_Level_Massing","Boutique_A_13_Level","Boutique_B_13_Level","North_Reference","Experience_Hotspot_Interior_Illustrative","Experience_Hotspot_Arrival_Illustrative","Experience_Hotspot_Landscaped_Open_Space_Illustrative"])invariant(hd.meshes.includes(required),"missing meaningful component: "+required);
invariant(![...hd.meshes,...lod.meshes].some((name)=>/(?:North|South|East|West).*Boutique|Boutique.*(?:North|South|East|West)/i.test(name)),"uncalibrated boutique mesh names may not imply cardinal placement");
invariant(poster.subarray(0,4).toString("ascii")==="RIFF"&&poster.subarray(8,12).toString("ascii")==="WEBP","poster.webp signature invalid");
invariant(experience.schema_version==="nadlan-owner-approved-experience-v1","experience schema mismatch");
invariant(experience.project_contract_id===spec.project_contract_id,"experience project identity mismatch");
invariant(experience.owner_decision_id===spec.experience_owner_decision_id,"experience owner decision mismatch");
invariant(experience.approved_by==="site_owner"&&experience.representation_kind==="owner_approved_illustration"&&experience.decision_grade===false,"experience truth metadata mismatch");
invariant(experience.version===spec.experience_version,"experience version mismatch");
invariant(experience.owner_publication_permission===true&&experience.release_gate_state==="private_stage","experience permission/release gate mismatch");
invariant(experience.global_visible_disclosure_required===true&&experience.external_network_required===false,"experience disclosure/network policy mismatch");
invariant(experience.mapping_policy?.active_state===spec.experience_mapping.active_state&&experience.mapping_policy.future_verified_state===spec.experience_mapping.future_verified_state&&experience.mapping_policy.coordinate_space===spec.experience_mapping.coordinate_space&&experience.mapping_policy.source_cited===false&&experience.mapping_policy.decision_grade===false&&experience.mapping_policy.real_world_orientation_calibrated===false,"experience mapping policy mismatch");
invariant(JSON.stringify(experience.mapping_policy.allowed_mapping_states)==='["owner_approved_illustrative_mapping","source_cited_mapping"]'&&JSON.stringify(experience.mapping_policy.confidence_vocabulary)==='["model_zone_fit_high__source_spatial_confidence_none"]',"experience mapping/confidence vocabulary mismatch");
invariant(JSON.stringify(experience.mapping_policy.anchors.map((anchor)=>({hotspot_id:anchor.hotspot_id,tool_id:anchor.tool_id,open_surface_tool_id:anchor.open_surface_tool_id,scene_ids:anchor.scene_ids,model_component_ids:anchor.model_component_ids,illustrative_zone_id:anchor.illustrative_zone_id,position:anchor.position,surface_normal:anchor.surface_normal,visual_offset_along_normal_m:anchor.visual_offset_along_normal_m,confidence:anchor.confidence,placement_confidence:anchor.placement_confidence})))===JSON.stringify(spec.experience_mapping.anchors.map((anchor)=>({hotspot_id:anchor.hotspot_id,tool_id:anchor.tool_id,open_surface_tool_id:anchor.open_surface_tool_id,scene_ids:anchor.scene_ids,model_component_ids:anchor.model_component_ids,illustrative_zone_id:anchor.illustrative_zone_id,position:anchor.position,surface_normal:anchor.surface_normal,visual_offset_along_normal_m:anchor.visual_offset_along_normal_m,confidence:anchor.confidence,placement_confidence:anchor.placement_confidence}))),"experience manifest/model anchor crosswalk mismatch");
invariant(experience.generation?.method==="built_in_image_generation"&&experience.generation?.source_pixels_or_textures_reused===false,"experience generation provenance mismatch");
invariant(Array.isArray(experience.generation?.visual_language_reference_ids)&&experience.generation.visual_language_reference_ids.join("|")==="MR001|MR003","experience visual-language references mismatch");
invariant(experience.generation?.local_delivery_conversion?.tool==="ImageMagick"&&experience.generation.local_delivery_conversion.format==="WebP"&&experience.generation.local_delivery_conversion.quality===82&&experience.generation.local_delivery_conversion.metadata==="stripped","experience delivery conversion mismatch");
invariant(experience.effective_at===spec.experience_effective_at&&experience.expires_at===spec.experience_expires_at&&Number.isFinite(Date.parse(experience.effective_at))&&Number.isFinite(Date.parse(experience.expires_at))&&Date.parse(experience.expires_at)>Date.parse(experience.effective_at),"experience dates invalid");
invariant(Array.isArray(experience.assets)&&experience.assets.length===4,"exact interior/facility experience assets required");
const expectedExperience=new Map([
  ["representative-apartment-living-v1",{file:"representative-apartment-living-v1.webp",tool:"interior",scene:"living",preview:"first_person_door",kind:"representative_concept",width:1536,height:1024}],
  ["representative-apartment-bedroom-v1",{file:"representative-apartment-bedroom-v1.webp",tool:"interior",scene:"bedroom",preview:"first_person_door",kind:"representative_concept",width:1523,height:1024}],
  ["facility-arrival-gallery-v1",{file:"facility-arrival-gallery-v1.webp",tool:"facilities",scene:"arrival",preview:"facility_concept_gallery",kind:"selectable_concept_gallery",width:1524,height:1024}],
  ["facility-landscaped-terrace-v1",{file:"facility-landscaped-terrace-v1.webp",tool:"facilities",scene:"open-frame",preview:"facility_concept_gallery",kind:"selectable_concept_gallery",width:1518,height:1024}]
]);
const experienceAssets=[];
for(const record of experience.assets){
  const expected=expectedExperience.get(record.asset_id);
  invariant(expected,"unknown experience asset");
  invariant(record.file===expected.file&&!record.file.includes("/")&&!record.file.includes("\\"),"experience asset file must be a local canonical basename");
  invariant(record.mime_type==="image/webp"&&record.tool_id===expected.tool&&record.open_surface_tool_id==="interior"&&record.scene_id===expected.scene&&record.preview_kind===expected.preview&&record.experience_kind===expected.kind,"experience asset semantic contract mismatch");
  const expectedAnchor=expectedAnchors.get(record.hotspot_id);
  invariant(record.mapping_state===spec.experience_mapping.active_state&&record.decision_grade===false&&expectedAnchor&&expectedAnchor.tool_id===record.tool_id&&JSON.stringify(record.illustrative_position)===JSON.stringify(expectedAnchor.position)&&JSON.stringify(record.placement_confidence)===JSON.stringify(expectedAnchor.placement_confidence),"experience asset illustrative mapping mismatch");
  invariant(record.width===expected.width&&record.height===expected.height,"experience dimensions mismatch");
  invariant(Array.isArray(record.prohibited_claims)&&record.prohibited_claims.length>0&&typeof record.public_scope==="string"&&record.public_scope.length>0&&typeof record.prompt_intent==="string"&&record.prompt_intent.length>40,"experience truth/prompt scope missing");
  const bytes=fs.readFileSync(path.join(path.dirname(experienceManifestPath),record.file));
  const digest=sha256(bytes);
  invariant(bytes.length===record.bytes&&digest===record.sha256,"experience asset bytes/hash mismatch");
  invariant(bytes.subarray(0,4).toString("ascii")==="RIFF"&&bytes.subarray(8,12).toString("ascii")==="WEBP","experience asset must be WebP");
  invariant(expectedAnchor.scene_ids.includes(record.scene_id),"experience asset scene/hotspot crosswalk mismatch");
  experienceAssets.push({asset_id:record.asset_id,file:record.file,bytes:bytes.length,sha256:digest,width:record.width,height:record.height,tool_id:record.tool_id,open_surface_tool_id:record.open_surface_tool_id,scene_id:record.scene_id,experience_kind:record.experience_kind,mapping_state:record.mapping_state,hotspot_id:record.hotspot_id,illustrative_position:record.illustrative_position,decision_grade:record.decision_grade});
  expectedExperience.delete(record.asset_id);
}
invariant(expectedExperience.size===0,"required experience asset missing");
const declaredExperienceFiles=new Set(experience.assets.map((record)=>record.file));
const actualExperienceFiles=fs.readdirSync(path.dirname(experienceManifestPath)).filter((file)=>file.toLowerCase().endsWith(".webp"));
invariant(actualExperienceFiles.length===declaredExperienceFiles.size&&actualExperienceFiles.every((file)=>declaredExperienceFiles.has(file)),"undeclared or missing experience WebP");
const result={ok:true,project_contract_id:spec.project_contract_id,calibration:spec.calibration,hd,lod,poster:{file:spec.files.poster,bytes:poster.length,sha256:sha256(poster)},experience:{owner_decision_id:experience.owner_decision_id,expires_at:experience.expires_at,assets:experienceAssets}};
console.log(JSON.stringify(result,null,2));
