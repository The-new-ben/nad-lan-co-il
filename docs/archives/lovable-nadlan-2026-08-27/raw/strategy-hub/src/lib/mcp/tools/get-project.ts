import { defineTool } from "@lovable.dev/mcp-js";
import { z } from "zod";
import { projectBySlug } from "@/lib/projects.mock";

export default defineTool({
  name: "get_project",
  title: "Get real-estate project by slug",
  description:
    "Return the full NadLan3D project record for a given slug, including units, pricing, and asset state.",
  inputSchema: {
    slug: z.string().min(1).describe("Project slug, e.g. 'rainbow-tlv'."),
  },
  annotations: { readOnlyHint: true, idempotentHint: true, openWorldHint: false },
  handler: ({ slug }) => {
    const project = projectBySlug(slug);
    if (!project) {
      return {
        content: [{ type: "text", text: `No project with slug '${slug}'.` }],
        isError: true,
      };
    }
    return {
      content: [{ type: "text", text: JSON.stringify(project, null, 2) }],
      structuredContent: { project },
    };
  },
});

