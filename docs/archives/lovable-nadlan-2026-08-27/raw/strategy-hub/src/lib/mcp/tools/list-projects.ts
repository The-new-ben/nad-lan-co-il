import { defineTool } from "@lovable.dev/mcp-js";
import { z } from "zod";
import { projects, rankProjects } from "@/lib/projects.mock";

export default defineTool({
  name: "list_projects",
  title: "List real-estate projects",
  description:
    "List NadLan3D real-estate projects, ranked by paid tier, completeness, engagement, freshness, and city affinity. Optionally filter by city (Hebrew or English) or status.",
  inputSchema: {
    city: z
      .string()
      .optional()
      .describe("Filter by city name (Hebrew or English), case-insensitive substring match."),
    status: z
      .enum(["pre-sale", "selling", "sold-out", "planning"])
      .optional()
      .describe("Filter by project status."),
    limit: z.number().int().min(1).max(50).optional().describe("Max results (default 20)."),
  },
  annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
  handler: ({ city, status, limit }) => {
    const needle = city?.trim().toLowerCase();
    const filtered = projects.filter((p) => {
      if (status && p.status !== status) return false;
      if (needle) {
        const hay = `${p.city_he} ${p.city_en}`.toLowerCase();
        if (!hay.includes(needle)) return false;
      }
      return true;
    });
    const ranked = rankProjects(filtered).slice(0, limit ?? 20);
    const rows = ranked.map((p) => ({
      slug: p.slug,
      name_he: p.name_he,
      name_en: p.name_en,
      city_he: p.city_he,
      city_en: p.city_en,
      developer: p.developer,
      status: p.status,
      paid_tier: p.paid_tier,
      priceFromILS: p.priceFromILS,
      rooms: p.rooms,
      asset_state: p.asset_state,
    }));
    return {
      content: [{ type: "text", text: JSON.stringify(rows, null, 2) }],
      structuredContent: { projects: rows, total: ranked.length },
    };
  },
});

