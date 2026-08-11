/** Local QA helper for the generated self-contained report. */
import { chromium } from "playwright";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const filename = process.argv[2] || "report.html";
const settleMs = Number(process.argv[3] ?? 3000);
const browser = await chromium.launch({ headless: true });
const results = [];
const expectedFreshness = "10 Aug 2026, 23:30 IDT";

for (const viewport of [{ width: 1440, height: 900, name: "desktop" }, { width: 390, height: 844, name: "mobile" }]) {
  const page = await browser.newPage({ viewport });
  const errors = [];
  const requests = [];
  page.on("pageerror", (error) => errors.push(String(error)));
  page.on("request", (request) => {
    if (!request.url().startsWith("file:") && !request.url().startsWith("data:")) requests.push(request.url());
  });
  await page.goto(pathToFileURL(path.join(here, filename)).href, { waitUntil: "load" });
  if (settleMs > 0) await page.waitForTimeout(settleMs);
  const geometry = await page.evaluate(() => {
    const width = document.documentElement.clientWidth;
    const offenders = [...document.querySelectorAll("body *")].map((node) => {
      const rect = node.getBoundingClientRect();
      return { node, rect };
    }).filter(({ rect }) => rect.right > width + 1 || rect.left < -1).map(({ node, rect }) => ({
      tag: node.tagName,
      id: node.id,
      className: String(node.className).slice(0, 160),
      left: Math.round(rect.left * 10) / 10,
      right: Math.round(rect.right * 10) / 10,
      width: Math.round(rect.width * 10) / 10,
      text: (node.textContent || "").trim().replace(/\s+/g, " ").slice(0, 100)
    })).slice(0, 40);
    return {
      clientWidth: width,
      scrollWidth: document.documentElement.scrollWidth,
      bodyClientWidth: document.body.clientWidth,
      bodyScrollWidth: document.body.scrollWidth,
      readerState: document.documentElement.dataset.dataAnalyticsPortableReader || "unset",
      topBarFreshness: (document.querySelector(".top-bar-refresh-text")?.textContent || "").trim(),
      topBarFreshnessAria: document.querySelector(".analytics-top-bar-freshness")?.getAttribute("aria-label") || "",
      offenders
    };
  });
  if (geometry.readerState === "ready") {
    if (geometry.topBarFreshness !== expectedFreshness) {
      throw new Error(`${viewport.name}: freshness locale drift: ${geometry.topBarFreshness}`);
    }
    if (geometry.topBarFreshnessAria !== `Last updated ${expectedFreshness}`) {
      throw new Error(`${viewport.name}: freshness accessible label drift: ${geometry.topBarFreshnessAria}`);
    }
  }
  await page.screenshot({ path: path.join(here, `report-${viewport.name}.png`), fullPage: false });
  results.push({ viewport, geometry, errors, externalRequests: requests });
  await page.close();
}

await browser.close();
await fs.writeFile(path.join(here, "report-inspection.json"), JSON.stringify({ generatedAt: new Date().toISOString(), filename, results }, null, 2) + "\n");
console.log(JSON.stringify(results.map((row) => ({ viewport: row.viewport.name, geometry: row.geometry, errors: row.errors.length, externalRequests: row.externalRequests.length })), null, 2));
