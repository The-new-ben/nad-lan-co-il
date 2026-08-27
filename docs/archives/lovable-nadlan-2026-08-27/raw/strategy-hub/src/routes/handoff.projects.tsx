import { createFileRoute } from "@tanstack/react-router";
import { ReferenceFrame } from "@/components/handoff/ReferenceFrame";

export const Route = createFileRoute("/handoff/projects")({
  component: () => (
    <ReferenceFrame
      title="Projects archive reference"
      src="/handoff-assets/projects-reference.html"
      sourcePath="reference/projects-reference.html"
    />
  ),
});

