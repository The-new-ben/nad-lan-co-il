import { createFileRoute } from "@tanstack/react-router";
import { HE } from "@/lib/nadlan-copy";
import { RentalsSection } from "@/components/sections/RentalsSection";
import rentalsImage from "@/assets/sketch-rentals-dashboard.jpg";

const HEALTH_STYLES: Record<string, { bg: string; fg: string }> = {
  contract: { bg: "var(--color-success)", fg: "#FFFFFF" },
  rent: { bg: "var(--color-success)", fg: "#FFFFFF" },
  security: { bg: "var(--color-gold)", fg: "#FFFFFF" },
  repairs: { bg: "var(--color-warning)", fg: "#FFFFFF" },
  tax: { bg: "var(--color-band)", fg: "var(--color-ink)" },
  renewal: { bg: "var(--color-band)", fg: "var(--color-ink)" },
};

const MONTHS = ["ינואר", "פברואר", "מרץ", "אפריל", "מאי", "יוני", "יולי", "אוגוסט", "ספטמבר", "אוקטובר", "נובמבר", "דצמבר"];

export const Route = createFileRoute("/my-rentals")({
  head: () => ({
    meta: [
      { title: "ניהול השכרות · נדל״ן" },
      { name: "description", content: "פורטפוליו נחיתה למשכירים פרטיים: מפה, בניין, דירה — עם חוזה, בטוחות, תשלומים ותזכורות." },
    ],
  }),
  component: MyRentalsPage,
});

function MyRentalsPage() {
  const c = HE.myRentals;
  return (
    <>
      <section className="bg-paper hairline-b">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-6 sm:py-24 lg:grid-cols-[1fr_1.1fr] lg:items-center">
          <div>
            <p className="kicker">{c.kicker}</p>
            <h1 className="mt-3">{c.title}</h1>
            <p className="mt-4 text-muted-ink">{c.sub}</p>
            <div className="mt-6 flex flex-wrap gap-3">
              <a href="#demo" className="btn-terracotta hover:btn-terracotta-hover">מתחילים לנהל, חינם</a>
              <a href="#demo" className="btn-gold-outline">צפייה בהדגמה</a>
            </div>
          </div>
          <div className="hairline overflow-hidden rounded-2xl bg-band">
            <img src={rentalsImage} alt="דירות מסומנות על מודל בניין ועל מפה" className="h-full w-full object-contain" />
          </div>
        </div>
      </section>

      <RentalsSection />

      {/* Deep demo frame */}
      <section id="demo" className="bg-band">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
          <p className="kicker">הדגמה חיה</p>
          <h2 className="mt-3">תיק הדירה — כל הפרטים בכרטיסייה אחת</h2>

          <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {c.healthCards.map((card) => {
              const style = HEALTH_STYLES[card.key]!;
              return (
                <div key={card.key} className="hairline rounded-xl bg-paper p-5">
                  <div className="flex items-center justify-between">
                    <h3 className="text-base">{card.title}</h3>
                    <span
                      className="rounded-full px-2.5 py-1 text-[11px] font-semibold"
                      style={{ backgroundColor: style.bg, color: style.fg }}
                    >
                      פעיל
                    </span>
                  </div>
                  <p className="mt-3 text-sm text-muted-ink">{card.status}</p>
                </div>
              );
            })}
          </div>

          {/* Ledger grid */}
          <div className="mt-10 hairline overflow-hidden rounded-xl bg-paper">
            <div className="hairline-b flex items-center justify-between px-5 py-3">
              <h3 className="text-sm font-semibold">{c.ledgerTitle}</h3>
              <span className="text-xs text-muted-ink">₪ · שקלים</span>
            </div>
            <div className="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-12">
              {MONTHS.map((m, i) => (
                <div key={m} className="hairline-t hairline-b border-x border-hairline p-3 text-center">
                  <div className="text-[11px] text-muted-ink">{m}</div>
                  <div className="mt-1 text-sm font-semibold" style={{ direction: "ltr" }}>
                    {i < 8 ? "6,800" : "—"}
                  </div>
                  <div
                    className="mx-auto mt-2 h-1.5 w-full rounded-full"
                    style={{ backgroundColor: i < 8 ? "var(--color-success)" : "var(--color-hairline)" }}
                    aria-hidden
                  />
                </div>
              ))}
            </div>
          </div>

          <p className="mt-6 text-xs text-muted-ink">{c.demoNote}</p>
        </div>
      </section>
    </>
  );
}

