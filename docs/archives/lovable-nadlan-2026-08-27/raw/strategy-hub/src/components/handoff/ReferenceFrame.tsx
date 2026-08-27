import { useState } from "react";
import { Link } from "@tanstack/react-router";

export function ReferenceFrame({
  title,
  src,
  sourcePath,
}: {
  title: string;
  src: string;
  sourcePath: string;
}) {
  const [viewport, setViewport] = useState<"desktop" | "mobile">("desktop");
  const width = viewport === "desktop" ? 1280 : 390;
  const height = viewport === "desktop" ? 900 : 800;

  return (
    <div className="space-y-4">
      <header className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-neutral-200 bg-white p-4">
        <div>
          <h1 className="text-lg font-semibold">{title}</h1>
          <p className="font-mono text-xs text-neutral-500">{sourcePath}</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="inline-flex rounded-sm border border-neutral-300 text-xs">
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
          <a
            href={src}
            target="_blank"
            rel="noreferrer"
            className="rounded-sm border border-neutral-300 px-3 py-1.5 text-xs hover:bg-neutral-50"
          >
            Open standalone
          </a>
          <Link
            to="/handoff/doc/$slug"
            params={{ slug: encodeURIComponent(sourcePath) }}
            className="rounded-sm border border-neutral-300 px-3 py-1.5 text-xs hover:bg-neutral-50"
          >
            View source
          </Link>
        </div>
      </header>

      <div className="overflow-auto rounded-lg border border-neutral-200 bg-neutral-100 p-3">
        <iframe
          key={viewport}
          src={src}
          title={title}
          style={{ width, height, border: 0, background: "white" }}
          className="mx-auto block"
        />
      </div>
    </div>
  );
}

