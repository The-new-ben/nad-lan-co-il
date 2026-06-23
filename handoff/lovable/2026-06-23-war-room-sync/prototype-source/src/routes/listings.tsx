import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import { useLang } from "@/lib/lang-context";
import { projects, rankProjects } from "@/lib/projects.mock";
import { MagazineCard } from "@/components/nadlan/MagazineCard";

export const Route = createFileRoute("/listings")({
  head: () => ({
    meta: [
      { title: "פרויקטים / Nadlan3D" },
      { name: "description", content: "כל הפרויקטים החדשים עם סימון ברור למיקומים בתשלום ומיון לפי שלמות מידע, עדכניות והתאמה לאזור." },
      { property: "og:title", content: "Projects / Nadlan3D" },
      { property: "og:description", content: "Projects ranked with clear paid-placement labels and visible asset status." },
      { property: "og:url", content: "/listings" },
    ],
    links: [
      { rel: "canonical", href: "/listings" },
      { rel: "alternate", hrefLang: "he", href: "/listings" },
      { rel: "alternate", hrefLang: "en", href: "/listings?lang=en" },
    ],
  }),
  component: Listings,
});

function Listings() {
  const { t, lang } = useLang();
  const [city, setCity] = useState<string>("all");
  const [rooms, setRooms] = useState<string>("all");
  const [completeOnly, setCompleteOnly] = useState(false);

  const cities = useMemo(() => {
    const seen = new Set<string>();
    return projects.flatMap((p) => {
      const key = lang === "he" ? p.city_he : p.city_en;
      if (seen.has(key)) return [];
      seen.add(key);
      return [key];
    });
  }, [lang]);

  const filtered = useMemo(() => {
    let r = projects;
    if (city !== "all") r = r.filter((p) => (lang === "he" ? p.city_he : p.city_en) === city);
    if (rooms !== "all") r = r.filter((p) => p.rooms.includes(Number(rooms)));
    if (completeOnly) r = r.filter((p) => p.completeness >= 0.75);
    return rankProjects(r);
  }, [city, rooms, completeOnly, lang]);

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <div className="flex items-baseline justify-between gap-4">
        <h1 className="text-3xl sm:text-4xl">{t("listings.title")}</h1>
        <span className="text-sm text-muted-foreground">
          {filtered.length} {t("listings.count")}
        </span>
      </div>

      {/* Filter bar */}
      <div className="hairline mt-6 grid grid-cols-2 gap-3 bg-card p-3 sm:flex sm:flex-wrap sm:items-center">
        <label className="text-xs">
          <span className="mb-1 block uppercase tracking-wider text-muted-foreground">{t("filter.city")}</span>
          <select
            value={city}
            onChange={(e) => setCity(e.target.value)}
            className="hairline w-full rounded-sm bg-background px-2 py-1.5 text-sm sm:w-auto"
          >
            <option value="all">{t("filter.all")}</option>
            {cities.map((c) => <option key={c} value={c}>{c}</option>)}
          </select>
        </label>
        <label className="text-xs">
          <span className="mb-1 block uppercase tracking-wider text-muted-foreground">{t("filter.rooms")}</span>
          <select
            value={rooms}
            onChange={(e) => setRooms(e.target.value)}
            className="hairline w-full rounded-sm bg-background px-2 py-1.5 text-sm sm:w-auto"
          >
            <option value="all">{t("filter.all")}</option>
            {[3, 4, 5, 6].map((n) => <option key={n} value={n}>{n}</option>)}
          </select>
        </label>
        <label className="col-span-2 mt-2 flex items-center gap-2 text-sm sm:col-span-1 sm:ms-auto sm:mt-0">
          <input
            type="checkbox"
            checked={completeOnly}
            onChange={(e) => setCompleteOnly(e.target.checked)}
            className="h-4 w-4 accent-foreground"
          />
          <span className="text-muted-foreground">{t("filter.completeness")}</span>
        </label>
      </div>

      {filtered.length === 0 ? (
        <p className="hairline mt-10 bg-card p-10 text-center text-sm text-muted-foreground">
          {t("listings.empty")}
        </p>
      ) : (
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((p) => <MagazineCard key={p.id} project={p} />)}
        </div>
      )}

      <aside className="hairline mt-12 bg-card p-5 text-xs text-muted-foreground">
        <strong className="text-foreground">{lang === "he" ? "שקיפות דירוג:" : "Ranking transparency:"}</strong>{" "}
        {lang === "he"
          ? "חלק מהמיקומים הם בתשלום ומסומנים כמודעה או כמקודם. שאר הסדר נקבע לפי שלמות המידע, עדכניות והתאמה לאזור."
          : "Some placements are paid and labelled as ads. The rest of the order uses available information, freshness, and location fit."}
      </aside>
    </div>
  );
}
