import { createServerFn } from "@tanstack/react-start";
import { notFound } from "@tanstack/react-router";

const DOCS = [
  "README.md",
  "01-live-audit.md",
  "02-canonical-showroom-pattern.md",
  "03-visual-spec.md",
  "04-public-copy-he-en.md",
  "05-branding-favicon-social.md",
  "06-replication-rule.md",
  "07-codex-build-plan.md",
  "08-wordpress-implementation-map.md",
  "source-manifest.md",
] as const;

const DATA = [
  "data/asset-contract.json",
  "data/component-map.json",
  "data/design-tokens.json",
  "data/qa-checklist.json",
] as const;

const REFERENCE = [
  "reference/showroom-reference.html",
  "reference/showroom-reference.css",
  "reference/homepage-reference.html",
  "reference/homepage-reference.css",
  "reference/projects-reference.html",
  "reference/projects-reference.css",
] as const;

const SCREENSHOTS = [
  "screenshots/showroom-desktop-he.png",
  "screenshots/showroom-mobile-he.png",
  "screenshots/showroom-desktop-en.png",
  "screenshots/showroom-mobile-en.png",
  "screenshots/homepage-desktop-he.png",
  "screenshots/homepage-mobile-he.png",
  "screenshots/projects-desktop-he.png",
  "screenshots/projects-mobile-he.png",
  "screenshots/selection-states.png",
  "screenshots/pattern-diagram.png",
  "screenshots/wordmark.png",
  "screenshots/favicon-32.png",
  "screenshots/favicon-192.png",
  "screenshots/apple-touch-icon-180.png",
  "screenshots/og-card.png",
] as const;

const ALLOWED = new Set<string>([...DOCS, ...DATA, ...REFERENCE, ...SCREENSHOTS]);

export const listHandoffFiles = createServerFn({ method: "GET" }).handler(async () => {
  return {
    docs: DOCS as readonly string[],
    data: DATA as readonly string[],
    reference: REFERENCE as readonly string[],
    screenshots: SCREENSHOTS as readonly string[],
  };
});

export const readHandoffFile = createServerFn({ method: "GET" })
  .inputValidator((input: { path: string }) => {
    if (!ALLOWED.has(input.path)) throw new Error("Not allowed");
    return input;
  })
  .handler(async ({ data }) => {
    const fs = await import("node:fs/promises");
    const path = await import("node:path");
    const abs = path.resolve("handoff/lovable/2026-06-24-premium-pattern", data.path);
    try {
      const content = await fs.readFile(abs, "utf-8");
      return { path: data.path, content };
    } catch {
      throw notFound();
    }
  });

