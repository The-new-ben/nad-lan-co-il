import { Link } from "@tanstack/react-router";
import type { Project } from "@/lib/projects.mock";
import { useLang } from "@/lib/lang-context";
import { useState } from "react";

interface Props {
  project: Project;
}

const tierBadge: Record<Project["paid_tier"], { key: string; classes: string }> = {
  featured: { key: "badge.featured", classes: "bg-accent text-accent-foreground" },
  promoted: { key: "badge.promoted", classes: "bg-foreground text-background" },
  standard: { key: "badge.standard", classes: "hairline bg-card text-muted-foreground" },
};

const assetLabelKey: Record<Project["asset_state"], string> = {
  "real-glb": "asset.short.model",
  "facade-svg": "asset.short.visual",
  empty: "asset.short.pending",
};

export function MagazineCard({ project }: Props) {
  const { lang, t } = useLang();
  const [tab, setTab] = useState<"facade" | "floor">("facade");
  const name = lang === "he" ? project.name_he : project.name_en;
  const city = lang === "he" ? project.city_he : project.city_en;
  const tagline = lang === "he" ? project.tagline_he : project.tagline_en;
  const tier = tierBadge[project.paid_tier];

  const priceFormatter = new Intl.NumberFormat(lang === "he" ? "he-IL" : "en-IL", {
    style: "currency",
    currency: "ILS",
    maximumFractionDigits: 0,
  });

  return (
    <article className="group hairline overflow-hidden bg-card transition hover:shadow-[0_8px_24px_-12px_rgba(27,26,23,0.18)]">
      <div className="relative aspect-[4/3] overflow-hidden bg-secondary">
        {tab === "facade" ? (
          <img
            src={project.hero_image}
            alt={name}
            loading="lazy"
            className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.02]"
          />
        ) : (
          <div className="watermark-ai flex h-full w-full items-center justify-center bg-card">
            <svg viewBox="0 0 200 150" className="h-3/4 w-3/4 text-muted-foreground">
              <rect x="10" y="10" width="180" height="130" fill="none" stroke="currentColor" strokeWidth="0.8" />
              <line x1="80" y1="10" x2="80" y2="140" stroke="currentColor" strokeWidth="0.6" />
              <line x1="10" y1="75" x2="190" y2="75" stroke="currentColor" strokeWidth="0.6" />
              <text x="100" y="80" textAnchor="middle" fontSize="6" fill="currentColor">
                {lang === "he" ? "תכנית" : "PLAN"}
              </text>
            </svg>
            <div className="watermark-ai-overlay">{t("watermark.ai")}</div>
          </div>
        )}
        {project.paid_tier !== "standard" && (
          <div className="absolute start-3 top-3 flex gap-2">
            <span className={`rounded-sm px-2 py-0.5 text-[10px] font-medium uppercase tracking-wider ${tier.classes}`}>
              {t(tier.key)}
            </span>
          </div>
        )}
        <div className="absolute end-3 top-3 flex hairline overflow-hidden bg-background/90 text-[10px]">
          <button
            type="button"
            onClick={() => setTab("facade")}
            className={`px-2 py-1 ${tab === "facade" ? "bg-foreground text-background" : "text-muted-foreground"}`}
          >
            {lang === "he" ? "חזות" : "Facade"}
          </button>
          <button
            type="button"
            onClick={() => setTab("floor")}
            className={`px-2 py-1 ${tab === "floor" ? "bg-foreground text-background" : "text-muted-foreground"}`}
          >
            {lang === "he" ? "תוכנית" : "Plan"}
          </button>
        </div>
      </div>

      <div className="p-4 sm:p-5">
        <div className="flex items-baseline justify-between gap-3">
          <h3 className="truncate text-lg leading-tight">{name}</h3>
          <span className="shrink-0 text-xs uppercase tracking-wider text-muted-foreground">{city}</span>
        </div>
        <p className="mt-2 line-clamp-2 text-sm text-muted-foreground">{tagline}</p>

        <dl className="hairline-t mt-4 grid grid-cols-3 gap-2 pt-3 text-xs">
          <div>
            <dt className="text-muted-foreground">{lang === "he" ? "החל מ" : "From"}</dt>
            <dd className="mt-0.5 font-medium text-foreground">{priceFormatter.format(project.priceFromILS)}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">{t("filter.rooms")}</dt>
            <dd className="mt-0.5 font-medium text-foreground">{project.rooms.join("/")}</dd>
          </div>
          <div>
            <dt className="text-muted-foreground">{lang === "he" ? "שלמות" : "Complete"}</dt>
            <dd className="mt-0.5 font-medium text-foreground">{Math.round(project.completeness * 100)}%</dd>
          </div>
        </dl>

        <div className="mt-4 flex items-center gap-3">
          <Link
            to="/showroom/$projectId"
            params={{ projectId: project.slug }}
            className="flex-1 rounded-sm bg-foreground px-3 py-2 text-center text-sm font-medium text-background hover:bg-foreground/90"
          >
            {t("cta.viewShowroom")}
          </Link>
          <span
            className="text-xs text-muted-foreground"
            title={
              project.asset_state === "real-glb"
                ? t("showroom.assetReal")
                : project.asset_state === "facade-svg"
                  ? t("showroom.assetFacade")
                  : t("showroom.assetEmpty")
            }
          >
            {t(assetLabelKey[project.asset_state])}
          </span>
        </div>
      </div>
    </article>
  );
}

