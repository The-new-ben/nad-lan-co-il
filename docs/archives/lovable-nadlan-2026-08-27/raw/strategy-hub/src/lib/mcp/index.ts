import { defineMcp } from "@lovable.dev/mcp-js";
import listProjectsTool from "./tools/list-projects";
import getProjectTool from "./tools/get-project";
import searchUnitsTool from "./tools/search-units";

export default defineMcp({
  name: "nadlan3d-mcp",
  title: "NadLan3D Real Estate MCP",
  version: "0.1.0",
  instructions:
    "Tools for browsing NadLan3D real-estate projects and apartment units. Use `list_projects` to browse ranked projects (optionally filtered by city or status), `get_project` to fetch a single project by slug, and `search_units` to find available apartments by rooms, price, or city.",
  tools: [listProjectsTool, getProjectTool, searchUnitsTool],
});

