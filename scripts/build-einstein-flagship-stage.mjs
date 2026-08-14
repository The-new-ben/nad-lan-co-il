import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => fs.readFileSync(path.join(ROOT, relative), "utf8");
const readJson = (relative) => JSON.parse(read(relative));
const sha256 = (value) => crypto.createHash("sha256").update(value).digest("hex");
const fileSha = (relative) => sha256(fs.readFileSync(path.join(ROOT, relative)));
const writeJson = (relative, value) => fs.writeFileSync(path.join(ROOT, relative), `${JSON.stringify(value, null, 2)}\n`, "utf8");

function parseCsv(text) {
  const rows = [];
  let row = [];
  let cell = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') {
        cell += '"';
        index += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        cell += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(cell);
      cell = "";
    } else if (char === "\n") {
      row.push(cell.replace(/\r$/, ""));
      rows.push(row);
      row = [];
      cell = "";
    } else {
      cell += char;
    }
  }
  if (cell || row.length) {
    row.push(cell.replace(/\r$/, ""));
    rows.push(row);
  }
  const headers = rows.shift();
  return rows.filter((candidate) => candidate.some(Boolean)).map((candidate) => Object.fromEntries(headers.map((header, index) => [header, candidate[index] ?? ""])));
}

const dataPath = "data/projects/einstein-tower.json";
const modelSpecPath = "assets/projects/einstein-tower/model-spec.json";
const experienceManifestPath = "assets/projects/einstein-tower/experience/manifest.json";
const registryPath = "plugins/nadlan-config/assets/flagship-v3/contracts/registry.json";
const articlePath = "docs/wp-drafts/einstein-tower-he-content.html";
const contentContractPath = "docs/wp-drafts/einstein-tower-he-content-contract.json";
const sourceRegisterPath = "assets/projects/einstein-tower/evidence/source-register.csv";
const visualSourceRegisterPath = "assets/projects/einstein-tower/evidence/primary-source-register.csv";
const hotspotCrosswalkPath = "assets/projects/einstein-tower/evidence/hotspot-placement-crosswalk.csv";
const hotspotSummaryPath = "assets/projects/einstein-tower/evidence/hotspot-anchor-summary.csv";
const packagePath = "assets/projects/einstein-tower/contracts/flagship-project.json";
const stagePath = "docs/wp-drafts/einstein-tower-flagship-v3-private-stage.json";

const data = readJson(dataPath);
const modelSpec = readJson(modelSpecPath);
const experienceManifest = readJson(experienceManifestPath);
const registryDoc = readJson(registryPath);
const article = read(articlePath);
const contentContract = readJson(contentContractPath);
const sourceRows = parseCsv(read(sourceRegisterPath));
const visualSourceRows = parseCsv(read(visualSourceRegisterPath));
const hotspotRows = parseCsv(read(hotspotCrosswalkPath));
const contract = registryDoc.contracts.find((candidate) => candidate.project_contract_id === "einstein-tower-6885-32");
if (!contract) throw new Error("The Einstein flagship contract is absent from the trusted registry.");

const PROJECT_CONTRACT_ID = "einstein-tower-6885-32";
const PLUGIN_ASSET_BASE = "https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/flagship-v3/projects/einstein-tower/";
const EXPERIENCE_ASSET_BASE = `${PLUGIN_ASSET_BASE}experience/`;
const SOURCE_EFFECTIVE_AT = Object.freeze({
  S001: "2026-08-14", S002: "2025-12-31", S004: "2020-04-01", S006: "2026-08-13",
  S009: "2026-08-14", S010: "2026-07-16", S012: "2026-08-14", S013: "2026-08-14",
  S014: "2026-06-10", S015: "2026-07-31", S016: "2026-07-31", S017: "2021-06-28",
  S018: "2021-03-11", S020: "2026-01-20", IVS002: "2026-08-14", IVS005: "2020-04-01",
  IVS008: "2026-07-09", IVS009: "2024-03-25",
});

const sourceById = new Map([...sourceRows, ...visualSourceRows].map((row) => [row.source_id, row]));
const source = (id) => {
  const row = sourceById.get(id);
  if (!row) throw new Error(`Missing governed source ${id}.`);
  return {
    id,
    label: row.title,
    effective_at: SOURCE_EFFECTIVE_AT[id],
    url: row.url,
  };
};

const buyerSourceIds = [
  "S001", "S002", "S004", "S006", "S009", "S010", "S012", "S013", "S014", "S015",
  "S016", "S017", "S018", "S020", "IVS002", "IVS005", "IVS008", "IVS009",
];
const sources = buyerSourceIds.map(source);
const sourcedRow = (id, label, summary, state, source_ids, extra = {}) => ({ id, label, summary, state, source_ids, ...extra });

const identity = {
  schema: "nadlan-project-identity-contract/v1",
  project_contract_id: PROJECT_CONTRACT_ID,
  source_id: PROJECT_CONTRACT_ID,
  canonical_post_id: 4867,
  canonical_slug: "einstein-tower",
  parcel: "6885/32",
  locale: "he",
  inventory_contract: {
    state: "not_supplied",
    decision_grade: false,
    effective_at: "2026-08-14",
    source_ids: ["S001", "S002"],
    note: "אין מלאי דירות מזוהה, מתוארך ומאומת שמחובר לפרויקט; המודל אינו יוצר דירות או זמינות.",
  },
};

const representations = {
  schema: "nadlan-project-representation-registry/v1",
  project_contract_id: PROJECT_CONTRACT_ID,
  calibration: {
    calibration_id: modelSpec.calibration.calibration_id,
    north_degrees: 0,
  },
  default_orbit: data.assets_3d.default_orbit,
  default_target: data.assets_3d.default_target,
  representations: contract.authorized_representations.map((asset) => ({
    role: asset.role,
    url: `${PLUGIN_ASSET_BASE}${asset.file}`,
    sha256: asset.sha256,
    representation_kind: "owner_approved_illustration",
    decision_grade: false,
    owner_decision_id: contract.representation_owner_decision_id,
    effective_at: modelSpec.effective_at,
    expires_at: modelSpec.expires_at,
  })),
};

const visualCopy = Object.freeze({
  view: ["מבט וסביבה", "פותחים מפה חזותית ומשווים בין המקום כיום, עבודות פעילות והתשתיות המתוכננות.", "לפתיחת המבט"],
  interior: ["פנים ומרחבים", "נכנסים לארבע סצנות חזותיות: שני חללי פנים ושני מרחבים משותפים, כולל נקודות עניין selectable.", "לכניסה לחללים"],
  design: ["עיצוב הדירה", "גוררים ריהוט על תוכנית המחשה ובודקים זרימה, אחסון והעדפות לפני חיבור תוכנית מכר.", "לפתיחת שולחן העיצוב"],
  comments: ["הערות על המודל", "מסמנים נקודה ושומרים טיוטת הערה מקומית; במצב הפרטי הזה אין שליחה חיצונית.", "לפתיחת ההערות"],
});
const previewKinds = Object.freeze({ view: "schematic_live_map", interior: "first_person_door", design: "illustrative_plan_drag", comments: "visual_annotation_request" });
const visual = {
  schema: "nadlan-visual-playground/v1",
  project_contract_id: PROJECT_CONTRACT_ID,
  locale: "he",
  decision: {
    owner_decision_id: contract.visual_playground_decision_id,
    approved_by: "site_owner",
    decision_grade: false,
    effective_at: contract.visual_playground_effective_at,
    expires_at: contract.visual_playground_expires_at,
  },
  comments_delivery: "prepared_no_write",
  writes_enabled: false,
  tools: ["view", "interior", "design", "comments"].map((id) => ({
    id,
    preview_kind: previewKinds[id],
    title: visualCopy[id][0],
    description: visualCopy[id][1],
    open_label: visualCopy[id][2],
    disclosure: "המחשה מאושרת",
    decision_grade: false,
  })),
};

const buyer = {
  schema: "nadlan-buyer-decision-contract/v1",
  project_contract_id: PROJECT_CONTRACT_ID,
  locale: "he",
  effective_at: "2026-08-14",
  labels: {
    facts: "עובדות מפתח", context: "מה יש סביב הפרויקט", sea: "הים", education: "חינוך",
    transit: "תחבורה", construction: "בנייה ונוף", overseas_buyer: "רוכש מחו״ל", sources: "מקורות",
    current: "כיום", future: "בעתיד", source: "מקור",
  },
  sources,
  facts: [
    { id: "identity", label: "הישות המדויקת", value: "EINSTEIN TOWER / איינשטיין 33א׳", truth_state: "verified", source_ids: ["S001", "S002"] },
    { id: "parcel", label: "גוש וחלקה", value: "6885/32", truth_state: "verified", source_ids: ["S002", "S006"] },
    { id: "program", label: "תוכנית הבינוי", value: "215 דירות · מגדל 28 קומות · שני מבנים בני 13 קומות · בסיס מסחרי דו-מפלסי", truth_state: "verified", source_ids: ["S002", "IVS008"] },
    { id: "permit", label: "רישוי עירוני", value: "היתר 20241734 · 9 ביולי 2026 · שדה שלב גולמי: בתהליך היתר", truth_state: "current_snapshot", source_ids: ["IVS008"] },
    { id: "enabling-permit", label: "היתר עבודות הכנה", value: "20240229 · דיפון, חפירה, ביסוס ורצפה ראשונה", truth_state: "verified", source_ids: ["IVS009"] },
    { id: "completion", label: "הערכת החברה", value: "רבעון שלישי 2030", truth_state: "reported", source_ids: ["S002"] },
  ],
  context_map: {
    title: "המקום כיום מול התמונה העתידית",
    layers: [
      {
        id: "current", label: "כיום", items: [
          sourcedRow("current-corner", "איינשטיין–לוי אשכול", "הפרויקט מזוהה בפינת הרחובות ועל חלקה 6885/32.", "current", ["S001", "S006"], { lat: data.location.lat, lng: data.location.lng }),
          sourcedRow("current-permit", "רישוי הפרויקט", "רשומת העירייה מתעדת היתר 20241734 מתאריך 9 ביולי 2026 לצד שדה שלב גולמי בתהליך היתר.", "current", ["IVS008"]),
          sourcedRow("current-transit-works", "עבודות בצומת", "נת״ע תיעדה עבודות תשתית בצומת ב-16 ביולי 2026.", "observed", ["S010"]),
        ],
      },
      {
        id: "future", label: "בעתיד", items: [
          sourcedRow("future-green-line", "הקו הירוק", "תחנות איינשטיין ולוי אשכול מופיעות בתכנון; אין כאן מועד הפעלה למקטע הצפוני.", "planned", ["S009"]),
          sourcedRow("future-sde-dov", "רובע שדה דב", "הרובע המערבי מוסיף בנייה, רחובות, פארקים ומסחר ומשנה את סביבת ההחלטה לאורך זמן.", "planned", ["S012"]),
          sourcedRow("future-public-realm", "המרחב הציבורי במגרש", "התכנון כולל גג מסחרי פעיל ושטחים פתוחים ציבוריים; המימוש המדויק ייבדק לפי מסמכי ביצוע.", "planned", ["IVS005"]),
        ],
      },
    ],
  },
  sea: {
    label: "חוף תל ברוך", distance_m: 975, method: "straight_line_to_tel_baruch_beach_polygon",
    method_label: "קו ישר מנקודת איינשטיין 16א׳ אל פוליגון החוף העירוני", source_ids: ["S017"],
  },
  education: {
    snapshot_label: "שכבות עירוניות שנבדקו לנקודת איינשטיין 16א׳",
    school_year: "2026/27",
    schools: [
      { name: "נופי ים", distance_m: 362, method: "קו ישר מהנקודה העירונית; אזור רישום נוכחי", source_ids: ["S013", "S014", "S015"] },
    ],
    kindergartens: [
      { name: "מתחם גנים בורלא 44", distance_m: 250, method: "קו ישר מהנקודה העירונית", source_ids: ["S013", "S016"] },
      { name: "מתחם גנים זינגר 1", distance_m: 316, method: "קו ישר מהנקודה העירונית", source_ids: ["S013", "S016"] },
      { name: "מתחם גנים עמיחי 1", distance_m: 381, method: "קו ישר מהנקודה העירונית", source_ids: ["S013", "S016"] },
    ],
  },
  transit: {
    line_label: "הקו הירוק · תחנות איינשטיין ולוי אשכול",
    current_works: { state: "observed", summary: "עבודות תשתית תועדו בצומת לוי אשכול–איינשטיין ביולי 2026.", source_ids: ["S010"] },
    planned_service: { state: "planned", summary: "השירות במקטע הצפוני עתידי; המקור שנבדק אינו מספק מועד פתיחה מחייב.", operating_date: null, source_ids: ["S009"] },
  },
  construction_and_views: {
    current_state: { label: "היתר ומצב ביצוע", summary: "היתר 20241734 מתועד ביולי 2026; דיווח החברה מסוף 2025 מתעד חפירה ודיפון. אין הסקת קצב ביצוע נוכחי.", state: "current_snapshot", source_ids: ["IVS008", "IVS009", "S002"] },
    future_context: { label: "בנייה סביבתית", summary: "שדה דב, הקו הירוק והמרחב הציבורי המתוכנן משנים את הנגישות, הבינוי והפתיחות סביב הפרויקט.", state: "planned", source_ids: ["S009", "S012", "IVS005"] },
    unit_view_state: { label: "נוף מדירה", summary: "כלי המבט פתוח להמחשה סביבתית; הוא אינו מייחס נוף לדירה, קומה או חזית מסוימת.", state: "owner_approved_illustration", source_ids: ["S001", "IVS002"] },
  },
  overseas_buyer: {
    title: "מסלול החלטה לרוכש מחו״ל",
    purchase_structure: { label: "מבנה העסקה", summary: "הדוח מתאר פרויקט במסגרת קבוצת רכישה; ההחלטה צריכה להתחיל בזיהוי הזכות וההסכמים המדויקים.", source_ids: ["S002", "S020"] },
    steps: [
      { id: "identity", title: "מאמתים זהות", summary: "מצליבים את הזכות עם איינשטיין 33א׳, גוש 6885 חלקה 32 והכתובת החוזית.", source_ids: ["S002", "S006"] },
      { id: "permit", title: "קוראים את תיק הרישוי", summary: "מצרפים היתר 20241734, היתר עבודות ההכנה והתוכניות העדכניות לבדיקה מקצועית.", source_ids: ["IVS008", "IVS009"] },
      { id: "economics", title: "בונים עלות מלאה", summary: "מחברים מחיר זכות ספציפית, תשלומים עתידיים, הצמדה, מסים, מימון ועלויות מקצועיות לפני החלטה.", source_ids: ["S002", "S020"] },
      { id: "environment", title: "בודקים חיים במקום", summary: "משווים חינוך, חוף, עבודות תחבורה ובינוי עתידי מול סדר היום והאופק של הרוכש.", source_ids: ["S009", "S010", "S012", "S013", "S017"] },
    ],
  },
  primary_action: { label: "למסלול ההחלטה המלא", target_section: "overseas-buyer" },
};

const sceneCopy = Object.freeze({
  living: ["חלל מגורים", "חלל מגורים ואירוח חזותי לבדיקת תנועה, אור, אחסון וקשר למרפסת.", "להיכנס לחלל", [
    ["living-flow", 38, 58, "ציר תנועה", "גררו את המבט לאורך מסלול הכניסה, האירוח והיציאה למרחב החוץ."],
    ["living-storage", 73, 47, "קיר אחסון", "סמנו מה צריך להישאר פתוח ומה דורש אחסון רציף."],
  ]],
  bedroom: ["חדר שינה ועבודה", "סצנת חדר חזותית לבדיקת פרטיות, אחסון, שולחן עבודה ותנועת בוקר.", "להיכנס לחדר", [
    ["bedroom-window", 67, 35, "חזית האור", "בדקו כיצד הייתם מאזנים אור, הצללה ופרטיות בחלל."],
    ["bedroom-work", 30, 62, "פינת עבודה", "הגדירו את עומק השולחן, מעבר הכיסא והפרדה מאזור השינה."],
  ]],
  arrival: ["כניסה ומרחב משותף", "סצנת כניסה משותפת חזותית לבדיקת הגעה, המתנה, נגישות וקצב המעבר לבניין.", "לראות את הכניסה", [
    ["arrival-path", 54, 64, "מסלול הגעה", "עקבו אחר קו הכניסה ובדקו נקודות המתנה, פנייה ומעבר."],
    ["arrival-seating", 26, 55, "אזור שהייה", "חשבו מי משתמש באזור ובאילו שעות הוא צריך לתפקד."],
  ]],
  "open-frame": ["מרחב פתוח ונטוע", "סצנה חזותית של מרחב משותף נטוע לבדיקת צל, ישיבה, תנועה ושימוש לאורך היום.", "לפתוח את המרחב", [
    ["landscape-shade", 41, 36, "שכבת צל", "בדקו את היחס בין צל, שמש, צמחייה ומקומות ישיבה."],
    ["landscape-route", 63, 70, "מסלול מעבר", "עקבו אחר התנועה בין ישיבה, שתילה ושולי המרחב."],
  ]],
});
const crosswalkByAsset = new Map(hotspotRows.map((row) => [row.asset_id, row]));
const mappingByAsset = new Map(contract.authorized_illustrative_mappings.map((row) => [row.asset_id, row]));
const authorizedAssetById = new Map(contract.authorized_experience_assets.map((row) => [row.asset_id, row]));
const experiences = {
  schema: "nadlan-project-experience-registry/v1",
  project_contract_id: PROJECT_CONTRACT_ID,
  locale: "he",
  mapping_crosswalk_sha256: contract.illustrative_mapping_crosswalk_sha256,
  mapping_anchor_summary_sha256: contract.illustrative_mapping_anchor_summary_sha256,
  heading: "נכנסים לפרויקט",
  back_label: "חזרה לפרויקט",
  previous_label: "הקודם",
  next_label: "הבא",
  decision: {
    owner_decision_id: contract.experience_decision_id,
    approved_by: "site_owner",
    representation_kind: "owner_approved_illustration",
    decision_grade: false,
    effective_at: contract.experience_effective_at,
    expires_at: contract.experience_expires_at,
  },
  scenes: experienceManifest.assets.map((asset) => {
    const trustedAsset = authorizedAssetById.get(asset.asset_id);
    const mapping = mappingByAsset.get(asset.asset_id);
    const crosswalk = crosswalkByAsset.get(asset.asset_id);
    if (!trustedAsset || !mapping || !crosswalk) throw new Error(`Missing scene binding for ${asset.asset_id}.`);
    const copy = sceneCopy[trustedAsset.scene_id];
    return {
      id: trustedAsset.scene_id,
      asset_id: asset.asset_id,
      kind: trustedAsset.kind,
      title: copy[0],
      summary: copy[1],
      open_label: copy[2],
      preview_url: `${EXPERIENCE_ASSET_BASE}${trustedAsset.preview_file}`,
      fullscreen_url: `${EXPERIENCE_ASSET_BASE}${trustedAsset.fullscreen_file}`,
      mapping_state: "owner_approved_illustrative_mapping",
      mapping_owner_decision_id: contract.illustrative_mapping_owner_decision_id,
      model_hotspot_group: mapping.model_hotspot_group,
      model_component: mapping.model_component,
      placement_source_refs: mapping.placement_source_refs,
      placement_basis: mapping.placement_basis,
      placement_confidence: mapping.placement_confidence,
      placement_ambiguity: mapping.placement_ambiguity,
      representation_kind: "owner_approved_illustration",
      decision_grade: false,
      source_ids: [],
      model_hotspot: {
        position: mapping.position,
        normal: mapping.normal,
        calibration_id: modelSpec.calibration.calibration_id,
      },
      image_hotspots: copy[3].map(([id, x_percent, y_percent, label, detail]) => ({ id, x_percent, y_percent, label, detail })),
    };
  }),
};

const componentHashes = {
  data: { path: dataPath, sha256: fileSha(dataPath) },
  model_spec: { path: modelSpecPath, sha256: fileSha(modelSpecPath) },
  experience_manifest: { path: experienceManifestPath, sha256: fileSha(experienceManifestPath) },
  trusted_registry: { path: registryPath, sha256: fileSha(registryPath) },
  article: { path: articlePath, sha256: fileSha(articlePath) },
  article_contract: { path: contentContractPath, sha256: fileSha(contentContractPath) },
  source_register: { path: sourceRegisterPath, sha256: fileSha(sourceRegisterPath) },
  visual_source_register: { path: visualSourceRegisterPath, sha256: fileSha(visualSourceRegisterPath) },
  mapping_crosswalk: { path: hotspotCrosswalkPath, sha256: fileSha(hotspotCrosswalkPath) },
  mapping_anchor_summary: { path: hotspotSummaryPath, sha256: fileSha(hotspotSummaryPath) },
};

const projectPackage = {
  schema: "nadlan-flagship-project-package/v1",
  generated_at: "2026-08-14",
  release_state: "private_stage",
  project_contract_id: PROJECT_CONTRACT_ID,
  canonical: { post_id: 4867, slug: "einstein-tower", public_release_enabled: false },
  owner_decision_ids: contract.owner_decision_ids,
  contracts: { identity, representations, visual, buyer_decision: buyer, experiences },
  asset_delivery: {
    base_url: PLUGIN_ASSET_BASE,
    allowed_evidence_reference_ids: contract.illustrative_mapping_reference_ids,
    model_files: contract.authorized_representations,
    experience_files: contract.authorized_experience_assets,
  },
  safeguards: {
    zero_inventory: true,
    top_level_tools: ["view", "interior", "design", "comments"],
    facilities_inside_interior: true,
    model_hotspot_groups: contract.required_experience_hotspot_groups,
    comments_delivery: "prepared_no_write",
    external_writes: false,
    private_stage_only: true,
    sandbox_catalog_source_id: "",
  },
  component_hashes: componentHashes,
};
writeJson(packagePath, projectPackage);

const meta = {
  developer_name: data.identity.developer,
  contractor_name: "",
  address: data.location.address_he,
  city: data.location.city,
  neighborhood: data.location.neighborhood,
  gush: data.location.gush,
  helka: data.location.helka,
  project_type: "new",
  project_status: "construction",
  num_units: data.units.total_units,
  num_buildings: data.building_form.num_buildings,
  num_floors: data.building_form.components[0].reported_floors,
  completion_year: 2030,
  website: data.identity.urls.official,
  lat: data.location.lat,
  lng: data.location.lng,
  source: "קבוצת חג׳ג׳ ורשומות עיריית תל אביב-יפו",
  source_url: data.identity.urls.official,
  source_id: "",
  is_demo: true,
  data_quality: "enriched",
  project_surface_version: "flagship-v3",
  project_contract_id: PROJECT_CONTRACT_ID,
  _nadlan_private_unit_journey: contract.sandbox.privacy_marker,
  _nadlan_flagship_source_post_id: 4867,
  project_model_glb: `${PLUGIN_ASSET_BASE}model-hd.glb`,
  project_model_lod_glb: `${PLUGIN_ASSET_BASE}model-lod.glb`,
  project_model_poster: `${PLUGIN_ASSET_BASE}poster.webp`,
  project_3d_model_type: "gltf",
  project_3d_demo: "1",
  project_3d_units: "[]",
  project_identity_contract_json: JSON.stringify(identity),
  project_representation_registry_json: JSON.stringify(representations),
  project_visual_playground_json: JSON.stringify(visual),
  project_buyer_decision_contract_json: JSON.stringify(buyer),
  project_experience_registry_json: JSON.stringify(experiences),
};

const stage = {
  schema: "nadlan-wordpress-private-stage-request/v1",
  generated_at: "2026-08-14",
  operation: "create_or_replace_exact_private_sandbox",
  endpoint: "https://nad-lan.co.il/wp-json/wp/v2/nadlan_project",
  lookup: {
    post_type: "nadlan_project",
    exact_slug: "sandbox-einstein-tower-flagship-v3-review",
    canonical_source_post_id: 4867,
    duplicate_catalog_source_id_forbidden: true,
  },
  secret_injection: {
    post_password: { environment_variable: "SANDBOX_POST_PASSWORD", inject_at: "body.password", required: true, serialized_value_forbidden: true },
  },
  body: {
    title: "EINSTEIN TOWER תל אביב · סקירה פרטית",
    slug: "sandbox-einstein-tower-flagship-v3-review",
    status: "publish",
    content: article,
    excerpt: contentContract.editorial.excerpt,
    meta,
  },
  expected: {
    public_visibility: "password_protected_only",
    canonical_url: null,
    search_indexing: "noindex_nofollow_noarchive",
    cache_policy: "private_no_store",
    anonymous_rest_presence: false,
    collection_presence: false,
    rendered_h1: contract.page_h1.he,
    global_demo_label: "הדמיה מאושרת",
    inventory_rows: 0,
    permanent_tools: ["view", "interior", "design", "comments"],
    experience_scenes: ["living", "bedroom", "arrival", "open-frame"],
    model_hotspots: contract.required_experience_hotspot_groups,
    external_writes: 0,
  },
  contract_hashes: {
    project_package_sha256: fileSha(packagePath),
    identity_sha256: sha256(JSON.stringify(identity)),
    representations_sha256: sha256(JSON.stringify(representations)),
    visual_sha256: sha256(JSON.stringify(visual)),
    buyer_decision_sha256: sha256(JSON.stringify(buyer)),
    experiences_sha256: sha256(JSON.stringify(experiences)),
    article_sha256: fileSha(articlePath),
  },
};
writeJson(stagePath, stage);

console.log(JSON.stringify({
  ok: true,
  project_package: packagePath,
  project_package_sha256: fileSha(packagePath),
  private_stage: stagePath,
  private_stage_sha256: fileSha(stagePath),
  sources: sources.length,
  tools: visual.tools.length,
  scenes: experiences.scenes.length,
  hotspots: new Set(experiences.scenes.map((scene) => scene.model_hotspot_group)).size,
}));
