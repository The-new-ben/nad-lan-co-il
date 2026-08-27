import { defineTool } from "@lovable.dev/mcp-js";
import { z } from "zod";
import { projects } from "@/lib/projects.mock";

export default defineTool({
  name: "search_units",
  title: "Search apartment units",
  description:
    "Search available apartment units across all NadLan3D projects, with optional filters for rooms, price, and city.",
  inputSchema: {
    rooms: z.number().int().min(1).max(10).optional().describe("Exact room count."),
    maxPriceILS: z.number().int().min(0).optional().describe("Maximum price in ILS."),
    minPriceILS: z.number().int().min(0).optional().describe("Minimum price in ILS."),
    city: z.string().optional().describe("City name (Hebrew or English), substring match."),
    onlyAvailable: z
      .boolean()
      .optional()
      .describe("If true, return only units with status 'available' (default true)."),
    limit: z.number().int().min(1).max(100).optional().describe("Max results (default 30)."),
  },
  annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
  handler: ({ rooms, maxPriceILS, minPriceILS, city, onlyAvailable = true, limit = 30 }) => {
    const needle = city?.trim().toLowerCase();
    const results: Array<Record<string, unknown>> = [];
    for (const p of projects) {
      if (needle) {
        const hay = `${p.city_he} ${p.city_en}`.toLowerCase();
        if (!hay.includes(needle)) continue;
      }
      for (const u of p.units) {
        if (onlyAvailable && u.status !== "available") continue;
        if (rooms !== undefined && u.rooms !== rooms) continue;
        if (maxPriceILS !== undefined && u.priceILS > maxPriceILS) continue;
        if (minPriceILS !== undefined && u.priceILS < minPriceILS) continue;
        results.push({
          project_slug: p.slug,
          project_name_en: p.name_en,
          city_en: p.city_en,
          unit_id: u.id,
          floor: u.floor,
          rooms: u.rooms,
          sqm: u.sqm,
          priceILS: u.priceILS,
          status: u.status,
        });
        if (results.length >= limit) break;
      }
      if (results.length >= limit) break;
    }
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
      structuredContent: { units: results, total: results.length },
    };
  },
});

