// S7 — Tools row: lead card on band ground with gold border, 4 supporting tools.
import { HE } from "@/lib/nadlan-copy";
import { Calculator, Coins, Scale, Home, Building2 } from "lucide-react";

const ICONS = [Coins, Scale, Home, Building2];

export function ToolsSection() {
  const c = HE.tools;

  return (
    <section className="bg-band">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
        <div className="flex flex-col gap-3">
          <p className="kicker">{c.kicker}</p>
          <h2 style={{ fontFamily: "var(--font-serif-he)" }}>{c.title}</h2>
        </div>

        <div className="mt-8 grid gap-5 lg:grid-cols-[1.3fr_2fr]">
          <a
            href="/calculators"
            className="group flex flex-col justify-between rounded-2xl bg-paper p-8"
            style={{ border: "1.5px solid var(--color-gold)" }}
          >
            <div>
              <Calculator className="h-8 w-8 text-gold" aria-hidden />
              <h3 className="mt-4 text-xl" style={{ fontFamily: "var(--font-serif-he)" }}>{c.lead.title}</h3>
              <p className="mt-2 text-sm text-muted-ink">{c.lead.body}</p>
            </div>
            <span className="mt-6 text-sm text-gold group-hover:underline">התחלה ←</span>
          </a>

          <div className="grid gap-4 sm:grid-cols-2">
            {c.rest.map((t, i) => {
              const Icon = ICONS[i] ?? Calculator;
              return (
                <a
                  key={t.title}
                  href="/calculators"
                  className="hairline group flex flex-col rounded-xl bg-paper p-5 transition-colors hover:border-gold"
                >
                  <Icon className="h-5 w-5 text-gold" aria-hidden />
                  <div className="mt-3 text-sm font-semibold">{t.title}</div>
                  <div className="mt-1 text-xs text-muted-ink">{t.body}</div>
                </a>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}

