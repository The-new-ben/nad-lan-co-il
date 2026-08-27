import { createFileRoute, Link } from "@tanstack/react-router";
import { HE } from "@/lib/nadlan-copy";
import sketch1 from "@/assets/sketch-building-holon.jpg";
import sketch2 from "@/assets/sketch-duo-ramat-gan.jpg";
import sketch3 from "@/assets/sketch-rainbow-beer-yaakov.jpg";
import sketch4 from "@/assets/sketch-sde-dov.jpg";

const IMG: Record<string, string> = {
  "keshet-holon": sketch1,
  "duo-ramat-gan": sketch2,
  "rainbow-beer-yaakov": sketch3,
  "sde-dov": sketch4,
};

export const Route = createFileRoute("/projects")({
  head: () => ({
    meta: [
      { title: "פרויקטים חדשים · נדל״ן" },
      { name: "description", content: "כל הפרויקטים החדשים בישראל, עם מודל תלת־ממדי חי לכל בניין." },
    ],
  }),
  component: ProjectsPage,
});

function ProjectsPage() {
  return (
    <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
      <p className="kicker">פרויקטים חדשים</p>
      <h1 className="mt-3">כל הפרויקטים החדשים בישראל</h1>
      <p className="mt-3 text-muted-ink">בחרו פרויקט כדי להיכנס לסיור התלת־ממדי.</p>

      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {HE.theater.projects.map((p) => (
          <Link
            key={p.id}
            to="/project/$slug"
            params={{ slug: p.id }}
            className="hairline group block overflow-hidden rounded-2xl bg-card transition-transform hover:-translate-y-0.5 hover:border-gold"
          >
            <div className="aspect-[4/3] bg-band">
              <img src={IMG[p.id]!} alt={p.name} className="h-full w-full object-contain" loading="lazy" />
            </div>
            <div className="p-5">
              <p className="text-xs text-muted-ink">{p.city}</p>
              <h3 className="mt-1 text-lg">{p.name}</h3>
              <p className="mt-2 text-xs text-muted-ink">{p.detail}</p>
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}

