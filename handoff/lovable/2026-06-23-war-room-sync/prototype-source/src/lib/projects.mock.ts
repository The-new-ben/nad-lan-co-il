// Nadlan3D demo project data. Keep this as the source of truth for this run.
// Schema is intentionally portable so Codex can mirror it into the WordPress
// `nadlan/v1/projects` endpoint without renaming fields.

export type PaidTier = "featured" | "promoted" | "standard";
export type AssetState = "real-glb" | "facade-svg" | "empty";
export type ProjectStatus = "pre-sale" | "selling" | "sold-out" | "planning";

export interface Unit {
  id: string;
  floor: number;
  rooms: number;
  sqm: number;
  priceILS: number;
  status: "available" | "reserved" | "sold";
}

export interface Project {
  id: string;
  slug: string;
  name_he: string;
  name_en: string;
  city_he: string;
  city_en: string;
  developer: string;
  status: ProjectStatus;
  paid_tier: PaidTier;
  priceFromILS: number;
  rooms: number[];
  // Visual asset status
  asset_state: AssetState;
  model_url?: string;             // production model file
  facade_svg?: string;            // inline facade id
  hero_image: string;             // public image URL
  plan_image: string;             // floor plan or AI watermark placeholder
  // Ranking signals
  completeness: number;           // 0..1 share of model, plan, photos, price, rooms
  engagement: number;             // 0..1 engagement proxy
  updated_at: string;             // ISO
  city_boost: number;             // 0..1 affinity
  units: Unit[];
  tagline_he: string;
  tagline_en: string;
}

const placeholderHero = (seed: string) =>
  `https://images.unsplash.com/photo-${seed}?auto=format&fit=crop&w=1600&q=70`;

export const projects: Project[] = [
  {
    id: "rainbow-tlv",
    slug: "rainbow-tlv",
    name_he: "מגדל הקשת",
    name_en: "Rainbow Tower",
    city_he: "תל אביב",
    city_en: "Tel Aviv",
    developer: "Rainbow Real Estate",
    status: "selling",
    paid_tier: "featured",
    priceFromILS: 3_950_000,
    rooms: [3, 4, 5],
    asset_state: "real-glb",
    model_url: "/models/rainbow.glb",
    hero_image: placeholderHero("1545324418-cc1a3fa10c00"),
    plan_image: "/plans/rainbow-floor.svg",
    completeness: 0.95,
    engagement: 0.82,
    updated_at: "2026-06-20T10:00:00Z",
    city_boost: 0.9,
    tagline_he: "47 קומות מעל רוטשילד. דירות בוטיק עם מודל תלת-ממד.",
    tagline_en: "47 floors above Rothschild. Boutique residences with a 3D model.",
    units: [
      { id: "r-12-a", floor: 12, rooms: 3, sqm: 78, priceILS: 3_950_000, status: "available" },
      { id: "r-12-b", floor: 12, rooms: 4, sqm: 104, priceILS: 5_200_000, status: "available" },
      { id: "r-22-a", floor: 22, rooms: 4, sqm: 108, priceILS: 5_780_000, status: "reserved" },
      { id: "r-33-p", floor: 33, rooms: 5, sqm: 162, priceILS: 9_400_000, status: "available" },
    ],
  },
  {
    id: "dimri-yama",
    slug: "dimri-yama",
    name_he: "דמרי ימה",
    name_en: "Dimri Yama",
    city_he: "אשדוד",
    city_en: "Ashdod",
    developer: "Dimri",
    status: "pre-sale",
    paid_tier: "promoted",
    priceFromILS: 2_180_000,
    rooms: [3, 4, 5],
    asset_state: "facade-svg",
    facade_svg: "dimri-facade",
    hero_image: placeholderHero("1512917774080-9991f1c4c750"),
    plan_image: "/plans/dimri-floor-ai.svg",
    completeness: 0.72,
    engagement: 0.61,
    updated_at: "2026-06-18T09:00:00Z",
    city_boost: 0.65,
    tagline_he: "פרויקט חוף ים בהקמה. חזית להמחשה עד שהיזם מעלה מודל תלת-ממד.",
    tagline_en: "Seafront project under construction. Illustrative facade until the developer uploads a 3D model.",
    units: [
      { id: "d-04-a", floor: 4, rooms: 3, sqm: 82, priceILS: 2_180_000, status: "available" },
      { id: "d-08-a", floor: 8, rooms: 4, sqm: 108, priceILS: 2_790_000, status: "available" },
      { id: "d-15-a", floor: 15, rooms: 5, sqm: 138, priceILS: 3_420_000, status: "available" },
    ],
  },
  {
    id: "kiryat-yam-renewal",
    slug: "kiryat-yam-renewal",
    name_he: "התחדשות קריית ים",
    name_en: "Kiryat Yam Renewal",
    city_he: "קריית ים",
    city_en: "Kiryat Yam",
    developer: "TMA-38 Group",
    status: "planning",
    paid_tier: "standard",
    priceFromILS: 1_650_000,
    rooms: [3, 4],
    asset_state: "empty",
    hero_image: placeholderHero("1486325212027-8081e485255e"),
    plan_image: "/plans/empty-placeholder.svg",
    completeness: 0.38,
    engagement: 0.44,
    updated_at: "2026-05-30T09:00:00Z",
    city_boost: 0.5,
    tagline_he: "פיילוט פינוי-בינוי. ממתין להעלאת חומרים מהיזם.",
    tagline_en: "Urban-renewal pilot. Awaiting developer assets.",
    units: [
      { id: "ky-1", floor: 3, rooms: 3, sqm: 76, priceILS: 1_650_000, status: "available" },
      { id: "ky-2", floor: 6, rooms: 4, sqm: 98, priceILS: 2_080_000, status: "available" },
    ],
  },
  {
    id: "carmel-heights",
    slug: "carmel-heights",
    name_he: "מרומי הכרמל",
    name_en: "Carmel Heights",
    city_he: "חיפה",
    city_en: "Haifa",
    developer: "Avgad Properties",
    status: "selling",
    paid_tier: "standard",
    priceFromILS: 2_450_000,
    rooms: [4, 5, 6],
    asset_state: "facade-svg",
    facade_svg: "carmel-facade",
    hero_image: placeholderHero("1502672260266-1c1ef2d93688"),
    plan_image: "/plans/carmel-floor.svg",
    completeness: 0.78,
    engagement: 0.55,
    updated_at: "2026-06-15T09:00:00Z",
    city_boost: 0.6,
    tagline_he: "20 קומות מעל המפרץ. נוף 270 מעלות.",
    tagline_en: "20 floors above the bay. 270 degree panorama.",
    units: [
      { id: "ch-7-a", floor: 7, rooms: 4, sqm: 112, priceILS: 2_450_000, status: "available" },
      { id: "ch-14-a", floor: 14, rooms: 5, sqm: 142, priceILS: 3_180_000, status: "available" },
    ],
  },
  {
    id: "jerusalem-talbiya",
    slug: "jerusalem-talbiya",
    name_he: "טלביה בוטיק",
    name_en: "Talbiya Boutique",
    city_he: "ירושלים",
    city_en: "Jerusalem",
    developer: "Yerushalayim Estates",
    status: "selling",
    paid_tier: "promoted",
    priceFromILS: 4_850_000,
    rooms: [4, 5],
    asset_state: "facade-svg",
    facade_svg: "talbiya-facade",
    hero_image: placeholderHero("1493809842364-78817add7ffb"),
    plan_image: "/plans/talbiya-floor.svg",
    completeness: 0.82,
    engagement: 0.68,
    updated_at: "2026-06-12T09:00:00Z",
    city_boost: 0.7,
    tagline_he: "אבן ירושלמית מקורית, 12 דירות בלבד.",
    tagline_en: "Original Jerusalem stone, 12 residences only.",
    units: [
      { id: "jt-2-a", floor: 2, rooms: 4, sqm: 118, priceILS: 4_850_000, status: "available" },
      { id: "jt-5-p", floor: 5, rooms: 5, sqm: 184, priceILS: 8_200_000, status: "reserved" },
    ],
  },
  {
    id: "netanya-marina",
    slug: "netanya-marina",
    name_he: "מרינה נתניה",
    name_en: "Netanya Marina",
    city_he: "נתניה",
    city_en: "Netanya",
    developer: "Marina Group",
    status: "pre-sale",
    paid_tier: "standard",
    priceFromILS: 2_980_000,
    rooms: [3, 4, 5],
    asset_state: "facade-svg",
    facade_svg: "marina-facade",
    hero_image: placeholderHero("1564013799919-ab600027ffc6"),
    plan_image: "/plans/marina-floor-ai.svg",
    completeness: 0.66,
    engagement: 0.49,
    updated_at: "2026-06-08T09:00:00Z",
    city_boost: 0.55,
    tagline_he: "מול הים, קרוב לטיילת ולמרינה.",
    tagline_en: "On the seafront, close to the promenade and marina.",
    units: [
      { id: "nm-3-a", floor: 3, rooms: 3, sqm: 88, priceILS: 2_980_000, status: "available" },
      { id: "nm-9-a", floor: 9, rooms: 4, sqm: 118, priceILS: 3_780_000, status: "available" },
    ],
  },
];

export const projectBySlug = (slug: string) =>
  projects.find((p) => p.slug === slug);

// Ranking hierarchy, deterministic client-side sort.
// 1. Paid tier  2. Completeness  3. Engagement  4. Freshness  5. City boost.
const tierWeight: Record<PaidTier, number> = {
  featured: 3,
  promoted: 2,
  standard: 1,
};

export function rankProjects(input: Project[]): Project[] {
  return [...input].sort((a, b) => {
    if (tierWeight[a.paid_tier] !== tierWeight[b.paid_tier]) {
      return tierWeight[b.paid_tier] - tierWeight[a.paid_tier];
    }
    if (a.completeness !== b.completeness) return b.completeness - a.completeness;
    if (a.engagement !== b.engagement) return b.engagement - a.engagement;
    const aDate = new Date(a.updated_at).getTime();
    const bDate = new Date(b.updated_at).getTime();
    if (aDate !== bDate) return bDate - aDate;
    return b.city_boost - a.city_boost;
  });
}
