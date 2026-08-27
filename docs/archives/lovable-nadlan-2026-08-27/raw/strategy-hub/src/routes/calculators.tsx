import { createFileRoute } from "@tanstack/react-router";
import { HE } from "@/lib/nadlan-copy";
import { Calculator, Coins, Scale, Home, Building2 } from "lucide-react";

const ICONS = [Coins, Scale, Home, Building2];

export const Route = createFileRoute("/calculators")({
  head: () => ({
    meta: [
      { title: "מחשבונים · נדל״ן" },
      { name: "description", content: "מחשבוני משכנתא, מס רכישה, שווי נכס, קנייה מול שכירות ובדיקת התחדשות." },
    ],
  }),
  component: CalculatorsPage,
});

function CalculatorsPage() {
  const c = HE.tools;
  return (
    <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
      <p className="kicker">{c.kicker}</p>
      <h1 className="mt-3">{c.title}</h1>

      <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div className="rounded-2xl bg-band p-6" style={{ border: "1.5px solid var(--color-gold)" }}>
          <Calculator className="h-8 w-8 text-gold" aria-hidden />
          <h2 className="mt-3 text-xl">{c.lead.title}</h2>
          <p className="mt-2 text-sm text-muted-ink">{c.lead.body}</p>
        </div>
        {c.rest.map((t, i) => {
          const Icon = ICONS[i] ?? Calculator;
          return (
            <div key={t.title} className="hairline rounded-2xl bg-card p-6">
              <Icon className="h-6 w-6 text-gold" aria-hidden />
              <h2 className="mt-3 text-lg">{t.title}</h2>
              <p className="mt-1 text-sm text-muted-ink">{t.body}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}

