import { createFileRoute, Link, notFound } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";
import { projects, rankProjects } from "@/lib/projects.mock";
import { MagazineCard } from "@/components/nadlan/MagazineCard";

const CITIES: Record<string, { he: string; en: string }> = {
  "tel-aviv": { he: "תל אביב", en: "Tel Aviv" },
  haifa: { he: "חיפה", en: "Haifa" },
  jerusalem: { he: "ירושלים", en: "Jerusalem" },
  ashdod: { he: "אשדוד", en: "Ashdod" },
  netanya: { he: "נתניה", en: "Netanya" },
  "kiryat-yam": { he: "קריית ים", en: "Kiryat Yam" },
};

export const Route = createFileRoute("/cities/$city")({
  loader: ({ params }) => {
    const city = CITIES[params.city];
    if (!city) throw notFound();
    return { city, slug: params.city };
  },
  head: ({ params, loaderData }) => ({
    meta: [
      { title: `${loaderData?.city.en ?? params.city} / Nadlan3D` },
      { name: "description", content: `פרויקטים חדשים ב-${loaderData?.city.he ?? params.city} עם חוויה חזותית ומידע ברור לרוכשים.` },
      { property: "og:title", content: `${loaderData?.city.en ?? params.city} new developments / Nadlan3D` },
      { property: "og:url", content: `/cities/${params.city}` },
    ],
    links: [
      { rel: "canonical", href: `/cities/${params.city}` },
    ],
  }),
  notFoundComponent: () => (
    <div className="mx-auto max-w-2xl px-4 py-20 text-center">
      <h1 className="text-3xl">City not yet covered</h1>
      <Link to="/listings" className="mt-6 inline-block hairline rounded-sm px-4 py-2 text-sm">All projects</Link>
    </div>
  ),
  component: CityPage,
});

function CityPage() {
  const { city } = Route.useLoaderData();
  const { t, lang } = useLang();
  const name = lang === "he" ? city.he : city.en;
  const inCity = rankProjects(
    projects.filter((p) => (lang === "he" ? p.city_he : p.city_en) === name)
  );

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6">
      <nav className="text-xs text-muted-foreground">
        <Link to="/" className="hover:text-foreground">{t("nav.home")}</Link>
        <span className="mx-2">/</span>
        <span>{t("nav.cities")}</span>
      </nav>
      <h1 className="mt-3 text-3xl sm:text-4xl">{name}</h1>
      <p className="mt-3 max-w-2xl text-sm text-muted-foreground">
        {lang === "he"
          ? `כל הפרויקטים החדשים ב-${name}, מדורגים בשקיפות.`
          : `Every new development in ${name}, transparently ranked.`}
      </p>

      <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {inCity.map((p) => <MagazineCard key={p.id} project={p} />)}
      </div>

      {inCity.length === 0 && (
        <p className="hairline mt-8 bg-card p-8 text-center text-sm text-muted-foreground">
          {lang === "he" ? "אין עדיין פרויקטים בעיר הזו." : "No listings here yet."}
        </p>
      )}
    </div>
  );
}
