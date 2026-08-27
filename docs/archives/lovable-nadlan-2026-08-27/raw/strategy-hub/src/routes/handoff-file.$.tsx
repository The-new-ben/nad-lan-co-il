import { createFileRoute } from "@tanstack/react-router";

const ALLOWED_PREFIXES = ["screenshots/"];

export const Route = createFileRoute("/handoff-file/$")({
  server: {
    handlers: {
      GET: async ({ params }) => {
        const raw = (params as { _splat?: string })._splat ?? "";
        const rel = decodeURIComponent(raw);
        if (!ALLOWED_PREFIXES.some((p) => rel.startsWith(p)) || rel.includes("..")) {
          return new Response("Forbidden", { status: 403 });
        }
        const fs = await import("node:fs/promises");
        const path = await import("node:path");
        const abs = path.resolve("handoff/lovable/2026-06-24-premium-pattern", rel);
        try {
          const buf = await fs.readFile(abs);
          const ext = path.extname(abs).toLowerCase();
          const mime =
            ext === ".png" ? "image/png" :
            ext === ".jpg" || ext === ".jpeg" ? "image/jpeg" :
            ext === ".svg" ? "image/svg+xml" :
            "application/octet-stream";
          return new Response(buf, {
            headers: {
              "Content-Type": mime,
              "Cache-Control": "public, max-age=300",
            },
          });
        } catch {
          return new Response("Not found", { status: 404 });
        }
      },
    },
  },
});

