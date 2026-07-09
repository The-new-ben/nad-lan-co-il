#!/usr/bin/env node

import fs from "node:fs/promises";
import vm from "node:vm";

const sourcePath = "plugins/nadlan-config/assets/showroom-engine/i18n.js";
const outputPath = "plugins/nadlan-config/assets/showroom-engine/i18n-complete.js";
const source = await fs.readFile(sourcePath, "utf8");
const context = { window: {} };
vm.createContext(context);
vm.runInContext(source, context);
const langs = context.window.NADLAN_I18N.langs;

const targets = { fr: "fr", ru: "ru", ar: "ar" };
const keepEnglish = /^(brand|proj_|lang_|sqm_unit$)/;
const placeholderPattern = /\{[^}]+\}/g;

function protect(text) {
  const placeholders = [];
  const safe = String(text).replace(placeholderPattern, (value) => {
    const token = `__NLPH_${placeholders.length}__`;
    placeholders.push(value);
    return token;
  });
  return { safe, placeholders };
}

function restore(text, placeholders) {
  let result = text;
  placeholders.forEach((value, index) => {
    result = result
      .replaceAll(`__NLPH_${index}__`, value)
      .replaceAll(`__NLPH${index}__`, value)
      .replaceAll(`__\u041d\u041b\u041f\u0425_${index}__`, value)
      .replaceAll(`__\u041d\u041b\u041f\u0425${index}__`, value);
  });
  return result;
}

async function translateOne(text, language) {
  const { safe, placeholders } = protect(text);
  const url = new URL("https://translate.googleapis.com/translate_a/single");
  url.searchParams.set("client", "gtx");
  url.searchParams.set("sl", "en");
  url.searchParams.set("tl", language);
  url.searchParams.set("dt", "t");
  url.searchParams.set("q", safe);
  let lastError;
  for (let attempt = 0; attempt < 3; attempt += 1) {
    try {
      const response = await fetch(url, { headers: { "User-Agent": "NadLan-i18n-build/1.0" } });
      if (!response.ok) throw new Error(`translation HTTP ${response.status}`);
      const data = await response.json();
      const translated = (data[0] || []).map((row) => row[0] || "").join("");
      if (!translated) throw new Error("empty translation");
      return restore(translated, placeholders);
    } catch (error) {
      lastError = error;
      await new Promise((resolve) => setTimeout(resolve, 350 * (attempt + 1)));
    }
  }
  throw lastError;
}

async function translateLanguage(language) {
  const current = langs[language];
  const keys = Object.keys(langs.en).filter((key) => current[key] === langs.en[key] && !keepEnglish.test(key));
  const result = {};
  let cursor = 0;
  const workers = Array.from({ length: 6 }, async () => {
    while (cursor < keys.length) {
      const key = keys[cursor];
      cursor += 1;
      result[key] = await translateOne(langs.en[key], targets[language]);
    }
  });
  await Promise.all(workers);
  return Object.fromEntries(keys.map((key) => [key, result[key]]));
}

const translated = {};
for (const language of Object.keys(targets)) {
  translated[language] = await translateLanguage(language);
  console.log(`${language}: ${Object.keys(translated[language]).length} labels translated`);
}

const output = `/* Generated static showroom translations. Buyer-facing copy only; no runtime API.\n` +
  `   Re-run scripts/generate-showroom-i18n-overrides.mjs when English UI keys change. */\n` +
  `(function () {\n  "use strict";\n  var root = window.NADLAN_I18N && window.NADLAN_I18N.langs;\n` +
  `  if (!root) return;\n  var overrides = ${JSON.stringify(translated, null, 2)};\n` +
  `  Object.keys(overrides).forEach(function (lang) { Object.assign(root[lang], overrides[lang]); });\n}());\n`;
await fs.writeFile(outputPath, output, "utf8");
console.log(`Wrote ${outputPath}`);
