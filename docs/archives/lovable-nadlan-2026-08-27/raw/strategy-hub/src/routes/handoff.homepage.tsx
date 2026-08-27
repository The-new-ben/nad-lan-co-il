import { createFileRoute } from "@tanstack/react-router";
import { ReferenceFrame } from "@/components/handoff/ReferenceFrame";

export const Route = createFileRoute("/handoff/homepage")({
  component: () => (
    <ReferenceFrame
      title="Homepage reference"
      src="/handoff-assets/homepage-reference.html"
      sourcePath="reference/homepage-reference.html"
    />
  ),
});

