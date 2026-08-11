/**
 * Finalizes the self-contained report produced by the shared report builder.
 *
 * Chromium builds with non-overlay scrollbars expose a shared-builder edge:
 * the sticky header uses 100vw, which includes the vertical scrollbar and
 * creates a 15px horizontal scroll. The report content itself does not
 * overflow. The shared reader also formats its freshness timestamp with the
 * device locale, which can mix Hebrew into this English handoff. This wrapper
 * applies only those two deterministic portable-output corrections.
 */
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const pluginRoot = process.env.DATA_ANALYTICS_PLUGIN_ROOT;
if (!pluginRoot) throw new Error("DATA_ANALYTICS_PLUGIN_ROOT is required");

const here = path.dirname(fileURLToPath(import.meta.url));
const scripts = path.join(pluginRoot, "skills", "build-report", "scripts");
const { buildPortableArtifact } = await import(
  pathToFileURL(path.join(scripts, "build_portable_artifact.mjs"))
);
const { extractPortableChartSvgs } = await import(
  pathToFileURL(path.join(scripts, "extract_portable_chart_svgs.mjs"))
);

const artifactPath = path.join(here, "artifact.json");
const basePath = path.join(here, ".report-base.tmp.html");
const outputPath = path.join(here, "report.html");
const artifact = JSON.parse(await fs.readFile(artifactPath, "utf8"));

try {
  const baseHtml = buildPortableArtifact(artifact);
  await fs.writeFile(basePath, baseHtml, "utf8");
  const staticCharts = await extractPortableChartSvgs({
    htmlPath: basePath,
    readyTimeoutMs: 20_000,
    actionTimeoutMs: 10_000,
  });
  const generated = buildPortableArtifact(artifact, { staticCharts });
  const target =
    "width:100vw;height:48px;min-height:48px;margin-right:calc(50% - 50vw);margin-left:calc(50% - 50vw)";
  const replacement =
    "width:100%;height:48px;min-height:48px;margin-right:0;margin-left:0";
  const occurrences = generated.split(target).length - 1;
  if (occurrences !== 1) {
    throw new Error(`Expected one shared-builder viewport-width rule; found ${occurrences}`);
  }
  const viewportSafeGenerated = generated.replace(target, replacement);
  const viewportSafetyStyle =
    '<style data-nadlan-report-viewport-fix="true">html,body{overflow-x:clip!important}.portable-page-header{width:100%!important;margin-right:0!important;margin-left:0!important}</style>';
  const readerLocaleFix = `<script data-nadlan-report-reader-locale-fix="true">(()=>{const text="10 Aug 2026, 23:30 IDT";let attempts=0;function apply(){const node=document.querySelector(".top-bar-refresh-text");if(node){node.textContent=text;const wrapper=node.closest(".analytics-top-bar-freshness");if(wrapper)wrapper.setAttribute("aria-label","Last updated "+text);return}attempts+=1;if(attempts<240)requestAnimationFrame(apply)}if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",apply,{once:true});else apply()})();</script>`;
  if (!viewportSafeGenerated.includes("</head>")) {
    throw new Error("Generated report has no closing head element");
  }
  const finalized = viewportSafeGenerated
    .replace("</head>", `${viewportSafetyStyle}</head>`)
    .replace("</body>", `${readerLocaleFix}</body>`);
  await fs.writeFile(outputPath, finalized, "utf8");
  process.stdout.write(
    `${JSON.stringify({ output: outputPath, bytes: Buffer.byteLength(finalized), charts: Object.keys(staticCharts) })}\n`,
  );
} finally {
  await fs.rm(basePath, { force: true });
}
