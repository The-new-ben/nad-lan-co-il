// S4 — Rentals band, white card with gold frame.
import { HE } from "@/lib/nadlan-copy";
import rentalsImage from "@/assets/sketch-rentals-dashboard.jpg";

export function RentalsSection() {
  const c = HE.rentals;

  return (
    <section className="bg-paper">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
        <div
          className="rounded-2xl bg-card p-8 sm:p-12"
          style={{ border: "1.5px solid var(--color-gold)" }}
        >
          <div className="grid gap-10 lg:grid-cols-[1fr_1.1fr] lg:items-center">
            <div>
              <p className="kicker">{c.kicker}</p>
              <h2 className="mt-3" style={{ fontFamily: "var(--font-serif-he)" }}>
                {c.title}
              </h2>
              <p className="mt-3 text-sm text-muted-ink">{c.sub}</p>

              <div className="mt-6 grid gap-3">
                {c.steps.map((s) => (
                  <div key={s.n} className="flex gap-4 rounded-xl bg-band p-4">
                    <span className="chip !border-gold !bg-paper text-gold">{s.n}</span>
                    <div>
                      <div className="text-sm font-semibold">{s.title}</div>
                      <div className="mt-1 text-xs text-muted-ink">{s.body}</div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-6 flex flex-wrap items-center gap-4">
                <a href="/my-rentals" className="btn-terracotta hover:btn-terracotta-hover">
                  {c.cta}
                </a>
                <span className="text-xs text-muted-ink">{c.note}</span>
              </div>
            </div>

            <div className="hairline overflow-hidden rounded-xl bg-band">
              <img
                src={rentalsImage}
                alt="דירות מסומנות על מודל בניין ועל מפת העיר"
                className="h-full w-full object-contain"
                loading="lazy"
                width={1408}
                height={1008}
              />
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

