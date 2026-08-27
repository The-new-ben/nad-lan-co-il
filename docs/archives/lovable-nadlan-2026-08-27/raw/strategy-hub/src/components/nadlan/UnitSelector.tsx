import type { Project, Unit } from "@/lib/projects.mock";
import { useLang } from "@/lib/lang-context";
import { useState } from "react";

interface Props {
  project: Project;
}

export function UnitSelector({ project }: Props) {
  const { t, lang } = useLang();
  const [selected, setSelected] = useState<Unit | null>(null);

  const fmt = new Intl.NumberFormat(lang === "he" ? "he-IL" : "en-IL", {
    style: "currency",
    currency: "ILS",
    maximumFractionDigits: 0,
  });

  return (
    <section className="hairline bg-card">
      <header className="hairline-b flex items-baseline justify-between px-4 py-3 sm:px-5">
        <h3 className="text-base">{t("showroom.units")}</h3>
        <span className="text-xs text-muted-foreground">{project.units.length} {t("showroom.units")}</span>
      </header>
      <ul className="divide-y divide-border">
        {project.units.map((u) => (
          <li key={u.id}>
            <button
              type="button"
              onClick={() => setSelected(u)}
              className="grid w-full grid-cols-[auto_1fr_auto] items-center gap-3 px-4 py-3 text-start hover:bg-secondary sm:px-5"
            >
              <span className="font-mono text-xs text-muted-foreground">
                {lang === "he" ? `קומה ${u.floor}` : `Floor ${u.floor}`}
              </span>
              <span className="text-sm">
                {u.rooms} {lang === "he" ? "חדרים" : "rooms"} / {u.sqm}m²
              </span>
              <span className="text-end text-sm font-medium">{fmt.format(u.priceILS)}</span>
            </button>
          </li>
        ))}
      </ul>

      {selected && (
        <UnitDrawer unit={selected} project={project} onClose={() => setSelected(null)} />
      )}
    </section>
  );
}

function UnitDrawer({ unit, project, onClose }: { unit: Unit; project: Project; onClose: () => void }) {
  const { t, lang } = useLang();
  const fmt = new Intl.NumberFormat(lang === "he" ? "he-IL" : "en-IL", {
    style: "currency",
    currency: "ILS",
    maximumFractionDigits: 0,
  });

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center bg-foreground/40 sm:items-center" onClick={onClose}>
      <div
        className="hairline w-full max-w-md bg-background p-5 sm:rounded-md"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-wider text-muted-foreground">
              {lang === "he" ? project.name_he : project.name_en} / {lang === "he" ? `קומה ${unit.floor}` : `Floor ${unit.floor}`}
            </p>
            <h4 className="mt-1 text-xl">
              {unit.rooms} {lang === "he" ? "חדרים" : "rooms"} / {unit.sqm}m²
            </h4>
            <p className="mt-1 text-lg font-medium text-foreground">{fmt.format(unit.priceILS)}</p>
          </div>
          <button onClick={onClose} className="hairline rounded-sm px-2 py-1 text-xs">✕</button>
        </div>

        <div className="watermark-ai hairline mt-4 aspect-[4/3] overflow-hidden bg-card">
          <svg viewBox="0 0 200 150" className="h-full w-full text-muted-foreground">
            <rect x="10" y="10" width="180" height="130" fill="none" stroke="currentColor" strokeWidth="0.8" />
            <line x1="80" y1="10" x2="80" y2="140" stroke="currentColor" strokeWidth="0.6" />
            <line x1="10" y1="75" x2="190" y2="75" stroke="currentColor" strokeWidth="0.6" />
            <text x="40" y="50" fontSize="6" fill="currentColor">{lang === "he" ? "סלון" : "LIVING"}</text>
            <text x="120" y="50" fontSize="6" fill="currentColor">{lang === "he" ? "חדר 1" : "BED 1"}</text>
            <text x="40" y="110" fontSize="6" fill="currentColor">{lang === "he" ? "מטבח" : "KIT"}</text>
            <text x="120" y="110" fontSize="6" fill="currentColor">{lang === "he" ? "חדר 2" : "BED 2"}</text>
          </svg>
          <div className="watermark-ai-overlay">{t("watermark.ai")}</div>
        </div>

        <p className="mt-3 text-xs text-muted-foreground">
          {lang === "he"
            ? "התוכנית להמחשה בלבד. הקבלן עדיין לא העלה תוכנית רשמית."
            : "Plan is illustrative only. Developer has not uploaded an official plan."}
        </p>

        <div className="mt-4 grid grid-cols-2 gap-2">
          <button className="rounded-sm bg-foreground px-3 py-2 text-sm text-background hover:bg-foreground/90">
            {t("cta.contactSeller")}
          </button>
          <button className="hairline rounded-sm px-3 py-2 text-sm hover:bg-secondary">
            {t("cta.whatsapp")}
          </button>
        </div>
        <button className="mt-2 w-full text-center text-xs text-muted-foreground underline-offset-2 hover:underline">
          {t("cta.uploadPlan")}
        </button>
      </div>
    </div>
  );
}

