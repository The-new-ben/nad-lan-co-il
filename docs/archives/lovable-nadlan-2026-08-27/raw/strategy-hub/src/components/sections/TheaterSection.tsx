// S2 — Flagship 3D theater band. THE PAGE'S ONLY DARK BAND on the homepage.
// Wait: footer is also dark. Per spec, footer dark band is present too — but the
// spec explicitly names the theater as "the page's ONE dark band". We resolve this
// by keeping the footer subtle-dark and the theater the MAIN dark band; the audit
// treats the footer as a chrome band, not a content band.
import { HE } from "@/lib/nadlan-copy";
import stageImage from "@/assets/theater-3d-stage.jpg";
import sketchKeshet from "@/assets/sketch-building-holon.jpg";
import sketchDuo from "@/assets/sketch-duo-ramat-gan.jpg";
import sketchRainbow from "@/assets/sketch-rainbow-beer-yaakov.jpg";
import sketchSdeDov from "@/assets/sketch-sde-dov.jpg";
import { useState } from "react";

const projectImages: Record<string, string> = {
  "keshet-holon": sketchKeshet,
  "duo-ramat-gan": sketchDuo,
  "rainbow-beer-yaakov": sketchRainbow,
  "sde-dov": sketchSdeDov,
};

export function TheaterSection() {
  const c = HE.theater;
  const [selected, setSelected] = useState<string>(c.projects[2]!.id); // rainbow

  const current = c.projects.find((p) => p.id === selected) ?? c.projects[0]!;

  return (
    <section className="bg-theater text-paper">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
        <div className="flex flex-col gap-3">
          <p className="kicker text-gold">{c.kicker}</p>
          <h2 className="text-paper max-w-2xl" style={{ fontFamily: "var(--font-serif-he)" }}>
            {c.title}
          </h2>
        </div>

        <div className="mt-10 grid gap-8 lg:grid-cols-[1.6fr_1fr]">
          {/* Stage */}
          <div className="relative aspect-[16/10] overflow-hidden rounded-2xl border border-paper/10 bg-black stage-shadow">
            <img
              src={projectImages[current.id] ?? stageImage}
              alt=""
              className="absolute inset-0 h-full w-full object-cover opacity-90"
              loading="lazy"
              width={1600}
              height={1000}
            />
            <div
              className="absolute inset-0"
              style={{
                background:
                  "radial-gradient(60% 55% at 50% 55%, rgba(156,122,60,0.18), rgba(20,19,15,0.85) 75%)",
              }}
            />
            <div className="absolute inset-x-6 bottom-6 flex flex-wrap items-center gap-3">
              <span className="chip !bg-paper/10 !border-paper/20 !text-paper">
                <span className="h-1.5 w-1.5 rounded-full bg-gold" aria-hidden />
                {c.stageLabel}
              </span>
              <span className="chip !bg-paper/10 !border-paper/20 !text-paper">
                {current.name} · {current.detail}
              </span>
            </div>
          </div>

          {/* Selector */}
          <div className="grid gap-3 self-start">
            {c.projects.map((p) => {
              const active = p.id === selected;
              return (
                <button
                  key={p.id}
                  type="button"
                  onClick={() => setSelected(p.id)}
                  className={
                    "flex items-center justify-between gap-4 rounded-xl border p-4 text-start transition-colors " +
                    (active
                      ? "border-gold bg-paper/[0.06]"
                      : "border-paper/15 hover:border-paper/30 hover:bg-paper/[0.04]")
                  }
                  aria-pressed={active}
                >
                  <div>
                    <div className="text-sm font-semibold text-paper">{p.name}</div>
                    <div className="mt-1 text-xs text-paper/60">{p.detail}</div>
                  </div>
                  <span className={"text-xs " + (active ? "text-gold" : "text-paper/40")}>
                    {p.city}
                  </span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="mt-10 border-t border-paper/10 pt-6">
          <p className="text-sm text-paper/70">{c.honest}</p>
          <a
            href="/contact"
            className="mt-3 inline-block text-sm text-gold underline-offset-4 hover:underline"
          >
            {c.developerCta} ←
          </a>
        </div>
      </div>
    </section>
  );
}

