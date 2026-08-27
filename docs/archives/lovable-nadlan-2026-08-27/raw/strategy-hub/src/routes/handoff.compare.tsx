import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import liveShot from "@/assets/live-screenshot.png.asset.json";

export const Route = createFileRoute("/handoff/compare")({
  component: ComparePage,
});

type Note = { top: string; text: string };

const LIVE_NOTES: Note[] = [
  { top: "8%", text: "1. Column is too narrow — content feels cramped" },
  { top: "20%", text: "2. The 3D showroom is small and not dominant" },
  { top: "32%", text: "3. Price tables stacked with no hierarchy" },
  { top: "55%", text: "4. Long body text in one block, no editorial rhythm" },
  { top: "85%", text: "5. No persistent 'selected apartment' panel" },
];

const TARGET_NOTES: Note[] = [
  { top: "10%", text: "1. Stage 642px — building is the visual center" },
  { top: "28%", text: "2. 6 unit pins, selected state with ink fill" },
  { top: "46%", text: "3. Selected-apartment panel pinned at right" },
  { top: "60%", text: "4. Facts grid: rooms · sqm · floor" },
  { top: "78%", text: "5. Gold primary CTA + WhatsApp secondary" },
];

const DECISIONS = [
  "Replace dark teal showroom skin with cream editorial shell (#FAF7F1).",
  "Frank Ruhl Libre 500 for display, Heebo 400-700 for body. Drop Inter for HE.",
  "Stage min-height 642px desktop, 466px mobile. Unit pin 74px desktop, 46px mobile.",
  "Selected panel is persistent (right column desktop, bottom sheet mobile).",
  "Gold #9C7A3C only for the primary buyer action. Sage for available, terracotta for reserve.",
  "No fake unit picking copy. Missing visuals → 'ממתינים לחומר חזותי מהיזם' panel.",
];

function ComparePage() {
  const [viewport, setViewport] = useState<"desktop" | "mobile">("desktop");
  const iframeWidth = viewport === "desktop" ? 1280 : 390;

  return (
    <div className="space-y-6">
      <header className="rounded-lg border border-neutral-200 bg-white p-5">
        <h1 className="text-xl font-semibold">Showroom: before vs after</h1>
        <p className="mt-1 text-sm text-neutral-600">
          Left: live nadlan3d.co.il (1.69.32) as uploaded.
          Right: the premium reference rendered live from <code>showroom-reference.html</code>.
        </p>
        <div className="mt-3 inline-flex rounded-sm border border-neutral-300 text-xs">
          <button
            onClick={() => setViewport("desktop")}
            className={`px-3 py-1.5 ${viewport === "desktop" ? "bg-neutral-900 text-white" : "hover:bg-neutral-50"}`}
          >
            Desktop 1280
          </button>
          <button
            onClick={() => setViewport("mobile")}
            className={`border-l border-neutral-300 px-3 py-1.5 ${viewport === "mobile" ? "bg-neutral-900 text-white" : "hover:bg-neutral-50"}`}
          >
            Mobile 390
          </button>
        </div>
      </header>

      <div className="grid gap-5 lg:grid-cols-2">
        {/* LIVE NOW */}
        <Panel
          tone="red"
          label="LIVE NOW · nadlan3d.co.il (1.69.32)"
          notes={LIVE_NOTES}
        >
          <div className="bg-neutral-100 p-2">
            <img
              src={liveShot.url}
              alt="Current live site screenshot"
              className="mx-auto block max-h-[900px] w-auto"
            />
          </div>
        </Panel>

        {/* PREMIUM TARGET */}
        <Panel
          tone="gold"
          label="PREMIUM TARGET · showroom-reference.html"
          notes={TARGET_NOTES}
        >
          <div className="overflow-auto bg-neutral-100 p-2">
            <iframe
              key={viewport}
              src="/handoff-assets/showroom-reference.html"
              title="Showroom reference"
              style={{
                width: iframeWidth,
                height: 900,
                border: 0,
                background: "white",
              }}
              className="mx-auto block"
            />
          </div>
        </Panel>
      </div>

      <section className="rounded-lg border border-neutral-200 bg-white p-5">
        <h2 className="text-sm font-semibold uppercase tracking-wider text-neutral-500">
          Decisions Codex must apply
        </h2>
        <ol className="mt-3 space-y-2 text-sm">
          {DECISIONS.map((d, i) => (
            <li key={i} className="flex gap-3">
              <span className="font-mono text-xs text-neutral-400">{String(i + 1).padStart(2, "0")}</span>
              <span>{d}</span>
            </li>
          ))}
        </ol>
        <p className="mt-4 text-xs text-neutral-500">
          Full plan: <code>handoff/lovable/2026-06-24-premium-pattern/07-codex-build-plan.md</code>
        </p>
      </section>
    </div>
  );
}

function Panel({
  tone,
  label,
  notes,
  children,
}: {
  tone: "red" | "gold";
  label: string;
  notes: Note[];
  children: React.ReactNode;
}) {
  const accent =
    tone === "red"
      ? { border: "border-red-300", text: "text-red-700", bg: "bg-red-50", dot: "bg-red-500" }
      : { border: "border-amber-400", text: "text-amber-800", bg: "bg-amber-50", dot: "bg-amber-500" };

  return (
    <div className={`rounded-lg border bg-white ${accent.border}`}>
      <div className={`flex items-center gap-2 border-b ${accent.border} ${accent.bg} px-3 py-2 text-xs font-semibold ${accent.text}`}>
        <span className={`inline-block h-2 w-2 rounded-full ${accent.dot}`} />
        {label}
      </div>
      <div className="relative">
        {children}
        {notes.map((n, i) => (
          <div
            key={i}
            className="pointer-events-none absolute right-2 max-w-[55%]"
            style={{ top: n.top }}
          >
            <div className={`inline-flex items-start gap-2 rounded-sm border ${accent.border} ${accent.bg} px-2 py-1 text-[11px] ${accent.text} shadow-sm`}>
              <span className={`mt-1 inline-block h-1.5 w-1.5 flex-none rounded-full ${accent.dot}`} />
              <span>{n.text}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

