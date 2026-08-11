import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const OUT = path.dirname(fileURLToPath(import.meta.url));
const projects = [
  { key: "toha2", url: "https://nad-lan.co.il/projects/toha2-tel-aviv/" },
  { key: "park", url: "https://nad-lan.co.il/projects/the-park-bnei-brak/" },
];

const browser = await chromium.launch({ headless: true });
const rows = [];
for (const viewport of [{ width: 375, height: 812 }, { width: 1280, height: 800 }]) {
  for (const project of projects) {
    const context = await browser.newContext({ viewport });
    const page = await context.newPage();
    const consoleErrors = [];
    const pageErrors = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") consoleErrors.push(msg.text());
    });
    page.on("pageerror", (error) => pageErrors.push(String(error)));
    const response = await page.goto(project.url, { waitUntil: "domcontentloaded", timeout: 120000 });
    await page.waitForTimeout(2500);
    const before = await page.evaluate(() => {
      const root = document.querySelector("#nl-root");
      if (root) root.scrollIntoView({ block: "start", behavior: "instant" });
      return {
        title: document.title,
        lang: document.documentElement.lang,
        dir: document.documentElement.dir,
        root: !!root,
        hotCount: document.querySelectorAll(".nl-hot[data-act='select']").length,
        cardCount: document.querySelectorAll(".nl-ucard").length,
        stickyText: document.querySelector("#nl-sticky")?.innerText?.trim() || "",
        rootText: root?.innerText?.slice(0, 3000) || "",
        assetVersions: [...document.scripts]
          .map((s) => s.src)
          .filter((src) => src.includes("showroom-engine")),
      };
    });
    await page.waitForTimeout(800);
    const hots = page.locator(".nl-hot[data-act='select']");
    let clicked = false;
    if (await hots.count()) {
      const candidate = hots.nth(Math.min(19, (await hots.count()) - 1));
      await candidate.scrollIntoViewIfNeeded().catch(() => {});
      await candidate.click({ force: true }).catch(() => {});
      clicked = true;
      await page.waitForTimeout(1500);
    }
    const after = await page.evaluate(() => {
      const selectors = [
        "#nl-root", ".nl-theater", ".nl-stagewrap", ".nl-stage", ".nl-panel",
        ".nl-unit-screen", ".nl-unit-summary__head", ".nl-unit-beam",
        ".nl-unit-beam__map", ".nl-unit-beam figcaption", ".nl-unit-facts",
        ".nl-unit-doors", ".nl-unit-quick", ".nl-unit-offer",
      ];
      const rect = (el) => {
        if (!el) return null;
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        return {
          x: +r.x.toFixed(1), y: +r.y.toFixed(1), width: +r.width.toFixed(1), height: +r.height.toFixed(1),
          display: cs.display, visibility: cs.visibility, overflowX: cs.overflowX, overflowY: cs.overflowY,
          client: [el.clientWidth, el.clientHeight], scroll: [el.scrollWidth, el.scrollHeight],
        };
      };
      const geometry = Object.fromEntries(selectors.map((s) => [s, rect(document.querySelector(s))]));
      const toolButtons = [...document.querySelectorAll("[data-tool]")].map((el) => ({
        tool: el.getAttribute("data-tool"), text: el.textContent.trim(), rect: rect(el),
      }));
      const focusables = [...document.querySelectorAll("a[href],button,input,select,textarea,[tabindex]")]
        .filter((el) => {
          const r = el.getBoundingClientRect();
          const cs = getComputedStyle(el);
          return r.width && r.height && cs.display !== "none" && cs.visibility !== "hidden";
        });
      return {
        url: location.href,
        selectedId: new URL(location.href).searchParams.get("unit"),
        selectedTitle: document.querySelector("#nl-selected-unit-title")?.textContent?.trim() || "",
        selectedText: document.querySelector(".nl-unit-screen,.nl-unit-summary")?.innerText?.slice(0, 5000) || "",
        geometry,
        toolButtons,
        liveDialogs: [...document.querySelectorAll("dialog,[role='dialog']")].map((el) => ({
          id: el.id, open: el.open ?? null, text: el.innerText.slice(0, 1000), rect: rect(el),
        })),
        focusableCount: focusables.length,
        undersizedTargets: focusables.map((el) => {
          const r = el.getBoundingClientRect();
          return { tag: el.tagName, text: (el.textContent || el.getAttribute("aria-label") || "").trim().slice(0, 100), width: +r.width.toFixed(1), height: +r.height.toFixed(1) };
        }).filter((x) => x.width < 44 || x.height < 44).slice(0, 200),
        bodyText: document.body.innerText.slice(0, 12000),
      };
    });
    const shot = path.join(OUT, `current-${project.key}-${viewport.width}x${viewport.height}.png`);
    await page.screenshot({ path: shot, fullPage: false });
    rows.push({
      project: project.key,
      viewport,
      status: response?.status() ?? null,
      before,
      clicked,
      after,
      consoleErrors,
      pageErrors,
      screenshot: shot,
    });
    await context.close();
  }
}
await browser.close();
fs.writeFileSync(path.join(OUT, "live-dom-probe.json"), JSON.stringify({ generatedAt: new Date().toISOString(), rows }, null, 2));
console.log(JSON.stringify(rows.map((r) => ({
  project: r.project,
  viewport: r.viewport,
  status: r.status,
  hotCount: r.before.hotCount,
  selectedId: r.after.selectedId,
  selectedTitle: r.after.selectedTitle,
  toolCount: r.after.toolButtons.length,
  consoleErrors: r.consoleErrors.length,
  pageErrors: r.pageErrors.length,
  screenshot: r.screenshot,
})), null, 2));
