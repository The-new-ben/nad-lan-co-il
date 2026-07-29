#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { chromium } from "playwright";

const root = process.cwd();
const phaseArg = process.argv.find((arg) => arg.startsWith("--phase="));
const phase = phaseArg ? phaseArg.split("=")[1] : "before";
if (!["before", "after"].includes(phase)) {
  throw new Error("Use --phase=before or --phase=after");
}

const pages = [
  { key: "duo-tel-aviv", label: "DUO Tel Aviv", url: "https://nad-lan.co.il/projects/duo-tel-aviv/" },
  { key: "rainbow-tel-aviv", label: "Rainbow Tel Aviv", url: "https://nad-lan.co.il/projects/rainbow-tel-aviv/" },
  { key: "dimri-yama-sde-dov", label: "Dimri Yama Sde Dov", url: "https://nad-lan.co.il/projects/dimri-yama-sde-dov/" },
  { key: "ashira-sde-dov", label: "Ashira Sde Dov", url: "https://nad-lan.co.il/projects/ashira-sde-dov/" }
];
if (phase === "after") {
  pages.unshift({ key: "utopia-sde-dov", label: "UTOPIA Sde Dov", url: "https://nad-lan.co.il/projects/utopia-sde-dov/" });
}

const outDir = path.join(
  root,
  "docs",
  "qa",
  "screenshots",
  `utopia-comparison-${phase}-2026-07-29`
);
await fs.mkdir(outDir, { recursive: true });

const browser = await chromium.launch({ channel: "chrome", headless: true });
const report = {
  schema: "nadlan-utopia-live-comparison-screenshots/v1",
  generated_at: new Date().toISOString(),
  phase,
  viewport: { width: 1440, height: 1000 },
  pages: []
};

try {
  for (const target of pages) {
    const context = await browser.newContext({ viewport: report.viewport, locale: "he-IL" });
    const page = await context.newPage();
    const errors = [];
    page.on("console", (message) => {
      if (message.type() === "error") errors.push(`console: ${message.text()}`);
    });
    page.on("pageerror", (error) => errors.push(`page: ${error.message}`));
    const response = await page.goto(target.url, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(2500);

    const topPath = path.join(outDir, `${target.key}-top.png`);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(250);
    await page.screenshot({ path: topPath, fullPage: false });

    const model = page.locator("#nl-mv, model-viewer").first();
    let modelPath = null;
    if (await model.count()) {
      await model.scrollIntoViewIfNeeded();
      await page.waitForTimeout(1200);
      modelPath = path.join(outDir, `${target.key}-model.png`);
      await page.screenshot({ path: modelPath, fullPage: false });
    }

    const state = await page.evaluate(() => ({
      title: document.title,
      lang: document.documentElement.lang,
      dir: document.documentElement.dir,
      h1Texts: [...document.querySelectorAll("h1")].map((node) => node.textContent.replace(/\s+/g, " ").trim()),
      h2Count: document.querySelectorAll("h2").length,
      emptyHeadings: [...document.querySelectorAll("h1,h2,h3,h4,h5,h6")]
        .filter((node) => !node.textContent.replace(/\s+/g, " ").trim())
        .map((node) => node.outerHTML.slice(0, 180)),
      engineRoots: document.querySelectorAll("#nl-root").length,
      modelViewers: document.querySelectorAll("model-viewer").length,
      unitHotspots: document.querySelectorAll("[data-act=\"select\"]").length,
      buildingHotspots: document.querySelectorAll("[data-act=\"building\"]").length,
      legacyBlocks: document.querySelectorAll(".nlpf,.nlpjx-nav,.nlpjx-intro,.nlpjx-price,.nlpjx,.nlcard,.nlms,.nlpe").length,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth
    }));
    report.pages.push({
      ...target,
      http_status: response?.status() || 0,
      ...state,
      horizontal_overflow_px: Math.max(0, state.scrollWidth - state.clientWidth),
      errors,
      screenshots: {
        top: path.relative(root, topPath).replaceAll("\\", "/"),
        model: modelPath ? path.relative(root, modelPath).replaceAll("\\", "/") : null
      }
    });
    await context.close();
    console.log(`${target.key}: ${response?.status() || 0}, h1=${state.h1Texts.length}, engine=${state.engineRoots}`);
  }
} finally {
  await browser.close();
}

const reportPath = path.join(outDir, "report.json");
await fs.writeFile(reportPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
console.log(reportPath);
