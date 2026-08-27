import { createFileRoute } from "@tanstack/react-router";
import { EN } from "@/lib/nadlan-copy";
import heroImage from "@/assets/hero-tel-aviv-shoreline.jpg";
import { useLang } from "@/lib/lang-context";
import { useEffect } from "react";
import { Search } from "lucide-react";

export const Route = createFileRoute("/en")({
  head: () => ({
    meta: [
      { title: "NadLan — Find an apartment, check the price, know the area" },
      { name: "description", content: "Every project on NadLan is a living 3D model: floors, apartments, sunlight and the view from the window — before you sign." },
      { property: "og:title", content: "NadLan — Find an apartment, check the price, know the area" },
    ],
  }),
  component: EnHome,
});

function EnHome() {
  const { setLang } = useLang();
  useEffect(() => {
    setLang("en");
  }, [setLang]);

  const c = EN.hero;

  return (
    <section className="relative isolate overflow-hidden">
      <img
        src={heroImage}
        alt="Aerial view of the Tel Aviv shoreline at golden hour"
        width={1920}
        height={1088}
        className="absolute inset-0 -z-10 h-full w-full object-cover"
      />
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-ink/15 via-ink/20 to-ink/50" />

      <div className="mx-auto max-w-6xl px-4 py-24 sm:px-6 sm:py-32 lg:py-40">
        <div className="max-w-2xl rounded-2xl border border-white/10 bg-theater/70 p-6 text-paper backdrop-blur-md sm:p-8 stage-shadow">
          <p className="kicker text-gold">{c.kicker}</p>
          <h1 className="mt-4 text-paper" style={{ fontFamily: "var(--font-serif-en)" }}>
            {c.title}
          </h1>
          <p className="mt-4 text-sm text-paper/80 sm:text-base">{c.sub}</p>

          <div className="mt-6 flex flex-wrap gap-2">
            {c.tabs.map((tab) => (
              <button
                key={tab}
                type="button"
                className="rounded-full border border-paper/25 px-4 py-1.5 text-xs font-semibold text-paper/85 hover:bg-paper/10"
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="mt-4 flex flex-col gap-2 sm:flex-row">
            <div className="flex flex-1 items-center gap-2 rounded-xl border border-paper/20 bg-paper/10 px-4 py-3">
              <Search className="h-4 w-4 text-paper/70" aria-hidden />
              <input
                type="search"
                placeholder={c.placeholder}
                className="w-full bg-transparent text-sm text-paper placeholder:text-paper/50 focus:outline-none"
                aria-label={c.placeholder}
              />
            </div>
            <button type="submit" className="btn-terracotta hover:btn-terracotta-hover">
              {c.search}
            </button>
          </div>

          <p className="mt-5 text-xs text-paper/65">{c.trust}</p>
        </div>
      </div>
    </section>
  );
}

