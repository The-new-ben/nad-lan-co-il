#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";

const SITE = "https://nad-lan.co.il";
const SLUGS = [
  "rainbow-tel-aviv",
  "rainbow-tel-aviv-en",
  "rainbow-tel-aviv-fr",
  "rainbow-tel-aviv-ru",
  "rainbow-tel-aviv-ar",
];
const META_KEYS = [
  "project_model_glb",
  "project_3d_units",
  "project_3d_drawings_json",
  "nadlan_showroom_composed_v2",
];
const BACKUP = path.resolve("docs/qa/rainbow-17268-meta-backup.json");
const ASSET_BASE = `${SITE}/wp-content/plugins/nadlan-config/assets/showroom-engine`;
const MODE = process.argv.includes("--rollback")
  ? "rollback"
  : process.argv.includes("--backup-only")
    ? "backup"
    : "apply";
const DRY_RUN = process.argv.includes("--dry-run");

const user = process.env.NADLAN_WP_USER;
const password = process.env.NADLAN_WP_APP_PASSWORD;
if (!user || !password) {
  throw new Error("Set NADLAN_WP_USER and NADLAN_WP_APP_PASSWORD before running this script.");
}
const authorization = `Basic ${Buffer.from(`${user}:${password}`).toString("base64")}`;

async function wp(url, options = {}) {
  const response = await fetch(`${SITE}${url}`, {
    ...options,
    headers: {
      Authorization: authorization,
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    throw new Error(`${options.method || "GET"} ${url} failed: ${response.status} ${await response.text()}`);
  }
  return response.json();
}

async function readProject(slug) {
  const rows = await wp(`/wp-json/wp/v2/nadlan_project?slug=${encodeURIComponent(slug)}&context=edit&per_page=1`);
  if (!rows.length) throw new Error(`Published project not found: ${slug}`);
  const row = rows[0];
  return {
    id: row.id,
    slug,
    meta: Object.fromEntries(META_KEYS.map((key) => [key, row.meta?.[key] ?? ""])),
  };
}

function repairAssetUrls(value) {
  if (value == null) return value;
  const source = typeof value === "string" ? value : JSON.stringify(value);
  return source
    .replace(
      /https:\/\/raw\.githubusercontent\.com\/The-new-ben\/nad-lan-co-il\/main\/assets\/projects\/rainbow-tel-aviv\/model\.glb/g,
      `${ASSET_BASE}/models/rainbow.glb`,
    )
    .replace(
      /https:\/\/raw\.githubusercontent\.com\/The-new-ben\/nad-lan-co-il\/main\/assets\/projects\/rainbow-tel-aviv\/plans\//g,
      `${ASSET_BASE}/plans/rainbow/`,
    );
}

async function saveBackup(projects) {
  await fs.mkdir(path.dirname(BACKUP), { recursive: true });
  const payload = {
    created_at: new Date().toISOString(),
    purpose: "Reversible backup before Rainbow composed-page and stable-media migration.",
    projects,
  };
  await fs.writeFile(BACKUP, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

async function updateProject(project, meta) {
  if (DRY_RUN) return;
  await wp(`/wp-json/wp/v2/nadlan_project/${project.id}`, {
    method: "POST",
    body: JSON.stringify({ meta }),
  });
}

const liveProjects = [];
for (const slug of SLUGS) liveProjects.push(await readProject(slug));

if (MODE === "backup") {
  await saveBackup(liveProjects);
  console.log(`Backed up ${liveProjects.length} Rainbow language pages to ${BACKUP}`);
} else if (MODE === "apply") {
  try {
    await fs.access(BACKUP);
  } catch {
    await saveBackup(liveProjects);
  }
  for (const project of liveProjects) {
    await updateProject(project, {
      project_model_glb: `${ASSET_BASE}/models/rainbow.glb`,
      project_3d_units: repairAssetUrls(project.meta.project_3d_units),
      project_3d_drawings_json: repairAssetUrls(project.meta.project_3d_drawings_json),
      nadlan_showroom_composed_v2: "1",
    });
  }
  console.log(`${DRY_RUN ? "Validated" : "Updated"} ${liveProjects.length} Rainbow language pages.`);
} else {
  const backup = JSON.parse(await fs.readFile(BACKUP, "utf8"));
  for (const stored of backup.projects) {
    const live = liveProjects.find((project) => project.slug === stored.slug);
    if (!live) throw new Error(`Cannot restore missing project: ${stored.slug}`);
    await updateProject(live, stored.meta);
  }
  console.log(`${DRY_RUN ? "Validated rollback for" : "Restored"} ${backup.projects.length} Rainbow language pages.`);
}
