import { createFileRoute, Link } from "@tanstack/react-router";
import { HE } from "@/lib/nadlan-copy";
import stageImage from "@/assets/theater-3d-stage.jpg";
import sketch1 from "@/assets/sketch-building-holon.jpg";
import sketch2 from "@/assets/sketch-duo-ramat-gan.jpg";
import sketch3 from "@/assets/sketch-rainbow-beer-yaakov.jpg";
import sketch4 from "@/assets/sketch-sde-dov.jpg";
import { useState } from "react";

const IMG: Record<string, string> = {
  "keshet-holon": sketch1,
  "duo-ramat-gan": sketch2,
  "rainbow-beer-yaakov": sketch3,
  "sde-dov": sketch4,
};

export const Route = createFileRoute("/project/$slug")({
  head: ({ params }) => ({
    meta: [
      { title: `${params.slug} · נדל״ן` },
      { name: "description", content: "מודל תלת־ממדי חי של הפרויקט. קומות, דירות, שמש ונוף." },
    ],
  }),
  component: ProjectPage,
});

function ProjectPage() {
  const { slug } = Route.useParams();
  const project = HE.theater.projects.find((p) => p.id === slug) ?? HE.theater.projects[0]!;
  const c = HE.project;
  const [tab, setTab] = useState<keyof typeof c.tabs>("apartments");

  return (
    <>
      {/* Dark 3D stage hero - THE page's one dark band */}
      <section className="bg-theater text-paper">
        <div className="mx-auto grid max-w-6xl gap-8 px-4 py-14 sm:px-6 sm:py-20 lg:grid-cols-[1.6fr_1fr]">
          <div className="relative aspect-[16/10] overflow-hidden rounded-2xl bg-black stage-shadow">
            <img src={IMG[project.id] ?? stageImage} alt="" className="absolute inset-0 h-full w-full object-cover opacity-90" />
            <div
              className="absolute inset-0"
              style={{ background: "radial-gradient(60% 55% at 50% 55%, rgba(156,122,60,0.18), rgba(20,19,15,0.85) 75%)" }}
            />
            <div className="absolute inset-x-6 bottom-6">
              <span className="chip !bg-paper/10 !border-paper/20 !text-paper">
                <span className="h-1.5 w-1.5 rounded-full bg-gold" aria-hidden /> {HE.theater.stageLabel}
              </span>
            </div>
          </div>

          <div className="self-center">
            <p className="kicker text-gold">{c.kicker}</p>
            <h1 className="mt-3 text-paper" style={{ fontFamily: "var(--font-serif-he)" }}>
              {project.name}
            </h1>
            <p className="mt-2 text-sm text-paper/70">{project.city} · {project.detail}</p>

            <dl className="mt-6 grid grid-cols-2 gap-3">
              {[
                { k: c.facts.units, v: project.detail.split("·")[0]!.trim() },
                { k: c.facts.rooms, v: "3–5" },
                { k: c.facts.floors, v: "12" },
                { k: c.facts.status, v: "בשיווק" },
              ].map((f) => (
                <div key={f.k} className="rounded-xl border border-paper/15 bg-paper/[0.04] p-3">
                  <dt className="text-xs text-paper/55">{f.k}</dt>
                  <dd className="mt-1 text-sm font-semibold text-paper">{f.v}</dd>
                </div>
              ))}
            </dl>

            <div className="mt-6 flex flex-wrap gap-3">
              <button type="button" className="btn-terracotta hover:btn-terracotta-hover">{c.offerCta}</button>
              <button type="button" className="btn-gold-outline">{c.tourCta}</button>
            </div>
            <p className="mt-4 text-xs text-paper/50">{c.illustrative}</p>
          </div>
        </div>
      </section>

      {/* Tabs */}
      <section className="bg-paper hairline-b">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="flex flex-wrap gap-1 py-3">
            {(Object.keys(c.tabs) as Array<keyof typeof c.tabs>).map((k) => (
              <button
                key={k}
                type="button"
                onClick={() => setTab(k)}
                className={
                  "rounded-full px-4 py-1.5 text-sm transition-colors " +
                  (tab === k ? "bg-ink text-paper" : "text-ink hover:bg-band")
                }
              >
                {c.tabs[k]}
              </button>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-12 sm:px-6 sm:py-16">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="hairline rounded-xl bg-card p-5">
              <p className="text-xs text-muted-ink">קומה {i + 3}</p>
              <div className="mt-1 text-lg font-semibold">דירה {i + 1}0{i}</div>
              <div className="mt-1 text-xs text-muted-ink">4 חדרים · 108 מ״ר</div>
              <div className="mt-3 flex items-center justify-between">
                <span className="text-sm font-semibold" style={{ direction: "ltr" }}>₪2,890,000</span>
                <span className="chip">שמש · דרום</span>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-10">
          <Link to="/projects" className="text-sm text-gold hover:underline">→ חזרה לרשימת הפרויקטים</Link>
        </div>
      </section>
    </>
  );
}

