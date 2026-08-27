import { createFileRoute, Link } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";
import { projects, rankProjects } from "@/lib/projects.mock";
import { MagazineCard } from "@/components/nadlan/MagazineCard";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Nadlan3D - נדל״ן שרואים לפני שקונים" },
      { name: "description", content: "סיור תלת-ממד לכל פרויקט נדל״ן. מציגים רק מה שקיים ומסמנים בבירור מה להמחשה." },
      { property: "og:title", content: "Nadlan3D - Real Estate, Rendered Real" },
      { property: "og:description", content: "Visual project tours with clear asset status and no invented plans." },
      { property: "og:url", content: "/" },
    ],
    links: [
      { rel: "canonical", href: "/" },
      { rel: "alternate", hrefLang: "he", href: "/" },
      { rel: "alternate", hrefLang: "en", href: "/?lang=en" },
    ],
  }),
  component: Index,
});

function Index() {
  const { t, lang } = useLang();
  const featured = rankProjects(projects).slice(0, 3);

  return (
    <div>
      {/* Hero */}
      <section className="hairline-b">
        <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-20">
          <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
            {lang === "he" ? "נדל״ן / ישראל / 2026" : "Real Estate / Israel / 2026"}
          </p>
          <h1 className="mt-4 text-3xl leading-tight sm:text-5xl md:text-6xl">{t("home.heroTitle")}</h1>
          <p className="mt-5 max-w-2xl text-base text-muted-foreground sm:text-lg">{t("home.heroSub")}</p>
          <div className="mt-7 flex flex-wrap gap-3">
            <Link
              to="/listings"
              className="rounded-sm bg-foreground px-5 py-3 text-sm font-medium text-background hover:bg-foreground/90"
            >
              {t("home.viewAll")}
            </Link>
            <Link
              to="/showroom/$projectId"
              params={{ projectId: "rainbow-tlv" }}
              className="hairline rounded-sm px-5 py-3 text-sm hover:bg-secondary"
            >
              {t("cta.viewShowroom")} - {lang === "he" ? "מגדל הקשת" : "Rainbow Tower"}
            </Link>
          </div>
        </div>
      </section>

      {/* Value strip */}
      <section className="hairline-b">
        <div className="mx-auto grid max-w-6xl gap-8 px-4 py-12 sm:grid-cols-3 sm:px-6">
          {[
            { t: "home.valueA", d: "home.valueAdesc" },
            { t: "home.valueB", d: "home.valueBdesc" },
            { t: "home.valueC", d: "home.valueCdesc" },
          ].map((v, i) => (
            <div key={v.t}>
              <span className="text-xs font-mono text-gold">0{i + 1}</span>
              <h3 className="mt-2 text-lg">{t(v.t)}</h3>
              <p className="mt-2 text-sm text-muted-foreground">{t(v.d)}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Selected projects */}
      <section>
        <div className="mx-auto max-w-6xl px-4 py-12 sm:px-6">
          <div className="flex items-baseline justify-between">
            <h2 className="text-2xl sm:text-3xl">{t("home.featured")}</h2>
            <Link to="/listings" className="text-sm text-muted-foreground hover:text-foreground">
              {t("home.viewAll")} →
            </Link>
          </div>
          <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {featured.map((p) => <MagazineCard key={p.id} project={p} />)}
          </div>
        </div>
      </section>
    </div>
  );
}

