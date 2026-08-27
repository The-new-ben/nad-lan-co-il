import { createFileRoute } from "@tanstack/react-router";
import { ReferenceFrame } from "@/components/handoff/ReferenceFrame";

export const Route = createFileRoute("/handoff/showroom")({
  component: () => (
    <ReferenceFrame
      title="Showroom reference"
      src="/handoff-assets/showroom-reference.html"
      sourcePath="reference/showroom-reference.html"
    />
  ),
});

