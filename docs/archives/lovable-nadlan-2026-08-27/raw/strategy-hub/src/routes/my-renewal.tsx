import { createFileRoute } from "@tanstack/react-router";
import { HE } from "@/lib/nadlan-copy";
import renewalImage from "@/assets/sketch-urban-renewal.jpg";

const CONSENT_COLORS: Record<string, string> = {
  success: "var(--color-success)",
  warning: "var(--color-warning)",
  danger: "var(--color-danger)",
};

export const Route = createFileRoute("/my-renewal")({
  head: () => ({
    meta: [
      { title: "חדר התחדשות · נדל״ן" },
      { name: "description", content: "חדר פרויקט לבניין שלכם — מודל תלת־ממדי, צבעי הסכמה, סטפר של 10 שלבים." },
    ],
  }),
  component: MyRenewalPage,
});

function MyRenewalPage() {
  const c = HE.myRenewal;
  return (
    <>
      <section className="bg-paper">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
          <p className="kicker">{c.kicker}</p>
          <h1 className="mt-3 max-w-3xl">{c.title}</h1>
          <p className="mt-4 max-w-2xl text-muted-ink">{c.sub}</p>

          <div className="mt-12 grid gap-8 lg:grid-cols-[1.4fr_1fr]">
            <div className="hairline relative overflow-hidden rounded-2xl bg-band">
              <img src={renewalImage} alt="מודל תלת־ממדי של הבניין" className="h-full w-full object-contain" />
              <div className="absolute inset-x-4 bottom-4 flex flex-wrap gap-2">
                {c.consent.map((s) => (
                  <span key={s.name} className="chip !bg-paper">
                    <span
                      className="h-2 w-2 rounded-full"
                      style={{ backgroundColor: CONSENT_COLORS[s.color] }}
                      aria-hidden
                    />
                    {s.name} · <span className="text-muted-ink">{s.count}</span>
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h2 className="text-lg">10 שלבים גלויים</h2>
              <ol className="mt-4 grid gap-2">
                {c.stepper.map((step, i) => (
                  <li key={step} className="hairline flex items-center gap-3 rounded-lg bg-card p-3">
                    <span
                      className="grid h-7 w-7 place-items-center rounded-full text-xs font-semibold"
                      style={{
                        backgroundColor: i < 4 ? "var(--color-success)" : "var(--color-band)",
                        color: i < 4 ? "#fff" : "var(--color-muted-ink)",
                      }}
                    >
                      {i + 1}
                    </span>
                    <span className="text-sm">{step}</span>
                  </li>
                ))}
              </ol>
            </div>
          </div>

          <p className="mt-8 text-xs text-muted-ink">נתוני דוגמה — מוצגים לצורך המחשה בלבד.</p>
        </div>
      </section>
    </>
  );
}

