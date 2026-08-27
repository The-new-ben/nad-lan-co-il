import { createFileRoute, notFound, Link } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";
import { projectBySlug } from "@/lib/projects.mock";
import { ShowroomViewer } from "@/components/nadlan/ShowroomViewer";
import { UnitSelector } from "@/components/nadlan/UnitSelector";

export const Route = createFileRoute("/showroom/$projectId")({
  loader: ({ params }) => {
    const project = projectBySlug(params.projectId);
    if (!project) throw notFound();
    return { project };
  },
  head: ({ params, loaderData }) => {
    const name = loaderData?.project.name_en ?? params.projectId;
    return {
      meta: [
        { title: `${name} - Project tour - Nadlan3D` },
        { name: "description", content: loaderData?.project.tagline_en ?? "Visual project tour on Nadlan3D." },
        { property: "og:title", content: `${name} - Nadlan3D project tour` },
        { property: "og:description", content: loaderData?.project.tagline_en ?? "" },
        { property: "og:url", content: `/showroom/${params.projectId}` },
        { property: "og:type", content: "product" },
        { property: "og:image", content: loaderData?.project.hero_image ?? "" },
      ],
      links: [
        { rel: "canonical", href: `/showroom/${params.projectId}` },
        { rel: "alternate", hrefLang: "he", href: `/showroom/${params.projectId}` },
        { rel: "alternate", hrefLang: "en", href: `/showroom/${params.projectId}?lang=en` },
      ],
    };
  },
  notFoundComponent: () => (
    <div className="mx-auto max-w-2xl px-4 py-20 text-center">
      <h1 className="text-3xl">Project tour not found</h1>
      <p className="mt-3 text-muted-foreground">This project doesn't exist yet.</p>
      <Link to="/listings" className="mt-6 inline-block hairline rounded-sm px-4 py-2 text-sm">
        View all projects
      </Link>
    </div>
  ),
  errorComponent: ({ error, reset }) => (
    <div className="mx-auto max-w-2xl px-4 py-20 text-center">
      <h1 className="text-2xl">Couldn't load this project tour</h1>
      <pre className="mt-3 text-xs text-muted-foreground">{error.message}</pre>
      <button onClick={reset} className="mt-6 hairline rounded-sm px-4 py-2 text-sm">Try again</button>
    </div>
  ),
  component: Showroom,
});

const JOURNEY = ["journey.1", "journey.2", "journey.3", "journey.4"] as const;

function Showroom() {
  const { project } = Route.useLoaderData();
  const { t, lang } = useLang();
  const name = lang === "he" ? project.name_he : project.name_en;
  const city = lang === "he" ? project.city_he : project.city_en;
  const tagline = lang === "he" ? project.tagline_he : project.tagline_en;

  return (
    <div className="mx-auto max-w-6xl px-4 pb-24 sm:px-6">
      {/* Breadcrumbs */}
      <nav className="mt-4 flex items-center gap-2 text-xs text-muted-foreground">
        <Link to="/" className="hover:text-foreground">{t("nav.home")}</Link>
        <span>/</span>
        <Link to="/listings" className="hover:text-foreground">{t("nav.listings")}</Link>
        <span>/</span>
        <span className="text-foreground">{name}</span>
      </nav>

      <header className="mt-4 flex items-end justify-between gap-4">
        <div className="min-w-0">
          <p className="text-xs uppercase tracking-wider text-muted-foreground">{city} / {project.developer}</p>
          <h1 className="mt-1 truncate text-3xl sm:text-4xl">{name}</h1>
          <p className="mt-2 max-w-2xl text-sm text-muted-foreground">{tagline}</p>
        </div>
      </header>

      {/* Viewer + units */}
      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_360px]">
        <ShowroomViewer project={project} />
        <UnitSelector project={project} />
      </div>

      {/* Journey */}
      <section className="hairline-t mt-12 pt-8">
        <h2 className="text-xl">{t("showroom.journey")}</h2>
        <ol className="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
          {JOURNEY.map((k, i) => (
            <li key={k} className="hairline bg-card p-4">
              <span className="text-xs font-mono text-gold">0{i + 1}</span>
              <p className="mt-2 text-sm">{t(k)}</p>
            </li>
          ))}
        </ol>
      </section>

      {/* Sticky CTA dock */}
      <div className="hairline-t fixed inset-x-0 bottom-0 z-30 bg-background/95 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center gap-2 px-4 py-3 sm:px-6">
          <p className="hidden flex-1 truncate text-sm text-muted-foreground sm:block">
            {name} / {city}
          </p>
          <button className="hairline rounded-sm px-3 py-2 text-sm hover:bg-secondary">{t("cta.whatsapp")}</button>
          <button className="rounded-sm bg-accent px-3 py-2 text-sm text-accent-foreground hover:opacity-90">
            {t("cta.contactSeller")}
          </button>
        </div>
      </div>
    </div>
  );
}

