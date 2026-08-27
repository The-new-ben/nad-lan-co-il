// S5 — Urban renewal band (band ground).
import { HE } from "@/lib/nadlan-copy";
import renewalImage from "@/assets/sketch-urban-renewal.jpg";

export function UrbanRenewalSection() {
  const c = HE.renewal;

  return (
    <section className="bg-band">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
        <div className="grid gap-10 lg:grid-cols-[1.1fr_1fr] lg:items-center">
          <div className="hairline overflow-hidden rounded-2xl bg-paper">
            <img
              src={renewalImage}
              alt="בניין ישן והבניין החדש המוצע מאחוריו"
              className="h-full w-full object-contain"
              loading="lazy"
              width={1408}
              height={912}
            />
          </div>

          <div>
            <p className="kicker">{c.kicker}</p>
            <h2 className="mt-3" style={{ fontFamily: "var(--font-serif-he)" }}>
              {c.title}
            </h2>
            <p className="mt-3 text-sm text-muted-ink">{c.sub}</p>

            <ol className="mt-6 grid gap-3">
              {c.steps.map((s) => (
                <li key={s.n} className="hairline flex gap-4 rounded-xl bg-paper p-4">
                  <span className="chip !border-gold !bg-band text-gold">{s.n}</span>
                  <div>
                    <div className="text-sm font-semibold">{s.title}</div>
                    <div className="mt-1 text-xs text-muted-ink">{s.body}</div>
                  </div>
                </li>
              ))}
            </ol>

            <div className="mt-6 flex flex-wrap gap-3">
              <a href="/my-renewal" className="btn-terracotta hover:btn-terracotta-hover">
                {c.ctaCheck}
              </a>
              <a href="/urban-renewal" className="btn-gold-outline">{c.ctaDemo}</a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

