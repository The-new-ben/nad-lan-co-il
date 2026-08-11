import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const OUT = path.dirname(fileURLToPath(import.meta.url));
const pages = [
  ["toha2", "https://nad-lan.co.il/projects/toha2-tel-aviv/?project=toha2-tel-aviv&lang=he&unit=floor-20"],
  ["park", "https://nad-lan.co.il/projects/the-park-bnei-brak/?project=the-park-bnei-brak&lang=he&unit=floor-20"],
];
const browser = await chromium.launch({ headless: true });
const results = [];
for (const [project, url] of pages) {
  const context = await browser.newContext({ viewport: { width: 375, height: 812 } });
  const page = await context.newPage();
  await page.goto(url, { waitUntil: "domcontentloaded", timeout: 120000 });
  await page.waitForTimeout(2500);
  await page.locator("#nl-root").scrollIntoViewIfNeeded().catch(() => {});
  const area = page.locator("[data-tool='area']:visible").first();
  await area.click();
  await page.waitForTimeout(3000);
  const data = await page.evaluate(() => {
    const canvas = document.querySelector(".nl-unit-area-tool__map canvas");
    const r = canvas?.getBoundingClientRect();
    const markers = [...document.querySelectorAll(".nl-unit-area-tool__map .mapboxgl-marker")].map((marker) => {
      const mr = marker.getBoundingClientRect();
      return {
        text: marker.textContent.trim(),
        ariaLabel: marker.getAttribute("aria-label"),
        title: marker.getAttribute("title"),
        x: +mr.x.toFixed(1), y: +mr.y.toFixed(1), width: +mr.width.toFixed(1), height: +mr.height.toFixed(1),
        insideCanvas: !!r && mr.left >= r.left && mr.right <= r.right && mr.top >= r.top && mr.bottom <= r.bottom,
      };
    });
    return {
      dialogText: document.querySelector("#nl-unit-tool")?.innerText || "",
      markers,
      googleLinks: [...document.querySelectorAll("#nl-unit-tool a[href]")].map((a) => ({ text: a.innerText.trim(), href: a.href })),
      controls: [...document.querySelectorAll("#nl-unit-tool button")].map((button) => ({ text: button.innerText.trim(), ariaLabel: button.getAttribute("aria-label"), title: button.title })),
      visibleLegend: [...document.querySelectorAll("#nl-unit-tool [class*='legend'],#nl-unit-tool [class*='filter'],#nl-unit-tool [class*='chip']")].map((el) => el.innerText.trim()).filter(Boolean),
      canvas: r ? { x: +r.x.toFixed(1), y: +r.y.toFixed(1), width: +r.width.toFixed(1), height: +r.height.toFixed(1) } : null,
    };
  });
  results.push({ project, url, ...data });
  await context.close();
}
await browser.close();
const output = path.join(OUT, "map-truth-probe.json");
fs.writeFileSync(output, JSON.stringify({ generatedAt: new Date().toISOString(), results }, null, 2), "utf8");
console.log(JSON.stringify(results, null, 2));
