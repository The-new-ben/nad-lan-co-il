import { useEffect, useRef, useState } from "react";
import type { Project } from "@/lib/projects.mock";
import { useLang } from "@/lib/lang-context";

interface Props {
  project: Project;
}

// Buyer-facing visual viewer. It never claims a model is live unless the file loads.
export function ShowroomViewer({ project }: Props) {
  const { t, lang } = useLang();
  const ref = useRef<HTMLDivElement>(null);
  const [mvReady, setMvReady] = useState(false);
  const [modelFailed, setModelFailed] = useState(false);

  useEffect(() => {
    setMvReady(false);
    setModelFailed(false);
    if (project.asset_state !== "real-glb") return;
    let cancelled = false;
    const mvUrl = "https://unpkg.com/@google/model-viewer@4.0.0/dist/model-viewer.min.js";

    async function loadModelViewer() {
      try {
        if (project.model_url) {
          const res = await fetch(project.model_url, { method: "HEAD" });
          if (!res.ok) throw new Error("model asset is missing");
        }
        await import(/* @vite-ignore */ /* webpackIgnore: true */ mvUrl);
        if (!cancelled) setMvReady(true);
      } catch {
        if (!cancelled) setModelFailed(true);
      }
    }

    loadModelViewer();
    return () => { cancelled = true; };
  }, [project.asset_state, project.model_url]);

  const stateLabel =
    project.asset_state === "real-glb" && modelFailed ? t("asset.stage.modelPending")
    : project.asset_state === "real-glb" && !mvReady ? t("asset.loading")
    : project.asset_state === "real-glb" ? t("showroom.assetReal")
    : project.asset_state === "facade-svg" ? t("showroom.assetFacade")
    : t("showroom.assetEmpty");
  const statusLabel =
    project.asset_state === "real-glb" && modelFailed ? t("asset.stage.modelPending")
    : project.asset_state === "real-glb" && mvReady ? t("asset.stage.model")
    : project.asset_state === "real-glb" ? t("asset.loading")
    : project.asset_state === "facade-svg" ? t("asset.stage.visual")
    : t("asset.stage.pending");
  const canShowModel = project.asset_state === "real-glb" && mvReady && !modelFailed;

  return (
    <div className="hairline relative overflow-hidden bg-card">
      <div ref={ref} className="aspect-[16/10] w-full sm:aspect-[16/9]">
        {canShowModel && (
          /* @ts-expect-error - custom element */
          <model-viewer
            src={project.model_url}
            camera-controls
            auto-rotate
            shadow-intensity="0.6"
            exposure="1.0"
            style={{ width: "100%", height: "100%", background: "transparent" }}
            onError={() => setModelFailed(true)}
          />
        )}
        {project.asset_state === "real-glb" && !canShowModel && (
          <FacadeSVG
            label={lang === "he" ? project.name_he : project.name_en}
            stageLabel={modelFailed ? t("asset.stage.modelPending") : t("asset.loading")}
            loading={!modelFailed}
          />
        )}
        {project.asset_state === "facade-svg" && (
          <FacadeSVG label={lang === "he" ? project.name_he : project.name_en} stageLabel={t("asset.schematic")} />
        )}
        {project.asset_state === "empty" && (
          <div className="flex h-full w-full flex-col items-center justify-center gap-3 p-6 text-center">
            <div className="hairline grid h-16 w-16 place-items-center rounded-sm text-muted-foreground">
              <svg viewBox="0 0 24 24" className="h-7 w-7" fill="none" stroke="currentColor" strokeWidth="1">
                <path d="M3 21h18M5 21V8l7-4 7 4v13M9 12h2M13 12h2M9 16h2M13 16h2" />
              </svg>
            </div>
            <p className="text-sm text-muted-foreground">{t("showroom.assetEmpty")}</p>
            <button className="hairline mt-2 rounded-sm px-3 py-2 text-xs text-foreground hover:bg-secondary">
              {t("cta.uploadPlan")}
            </button>
          </div>
        )}
      </div>
      <div className="hairline-t flex items-center justify-between gap-2 px-4 py-2 text-xs text-muted-foreground">
        <span>{stateLabel}</span>
        <span className="uppercase tracking-wider">{statusLabel}</span>
      </div>
    </div>
  );
}

function FacadeSVG({ label, loading = false, stageLabel }: { label: string; loading?: boolean; stageLabel: string }) {
  return (
    <div className="relative h-full w-full bg-gradient-to-b from-secondary to-card">
      <svg viewBox="0 0 320 200" className="h-full w-full" preserveAspectRatio="xMidYMid meet">
        <defs>
          <linearGradient id="bld" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="oklch(0.55 0.04 60)" />
            <stop offset="100%" stopColor="oklch(0.35 0.04 60)" />
          </linearGradient>
        </defs>
        <rect x="100" y="40" width="120" height="140" fill="url(#bld)" opacity="0.9" />
        <polygon points="100,40 160,20 220,40" fill="oklch(0.45 0.04 60)" />
        {Array.from({ length: 7 }).map((_, row) =>
          Array.from({ length: 4 }).map((_, col) => (
            <rect
              key={`${row}-${col}`}
              x={110 + col * 26}
              y={55 + row * 17}
              width={18}
              height={11}
              fill="oklch(0.95 0.04 85 / 0.78)"
              stroke="oklch(0.25 0.02 60 / 0.4)"
              strokeWidth="0.4"
            />
          ))
        )}
        <rect x="148" y="160" width="24" height="20" fill="oklch(0.25 0.02 60)" />
      </svg>
      <div className="pointer-events-none absolute inset-0 flex items-end justify-between p-3 text-[10px] uppercase tracking-wider text-muted-foreground">
        <span>{label}</span>
        <span>{loading ? stageLabel : stageLabel}</span>
      </div>
    </div>
  );
}
