// S3 — Live map band (light, cream). SVG-based stylized Israel outline with terracotta pins.
import { HE } from "@/lib/nadlan-copy";

const CITY_POS: Record<string, { x: number; y: number }> = {
  "תל אביב": { x: 130, y: 260 },
  "רמת גן": { x: 148, y: 258 },
  "ירושלים": { x: 210, y: 300 },
  "חיפה": { x: 175, y: 165 },
  "באר שבע": { x: 195, y: 400 },
  "נתניה": { x: 135, y: 220 },
  "ראשון לציון": { x: 135, y: 275 },
  "חולון": { x: 132, y: 272 },
};

export function MapSection() {
  const c = HE.map;

  return (
    <section className="bg-paper hairline-b hairline-t">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
        <div className="flex flex-col gap-3">
          <p className="kicker">{c.kicker}</p>
          <h2 style={{ fontFamily: "var(--font-serif-he)" }}>{c.title}</h2>
          <p className="text-sm text-muted-ink">{c.sub}</p>
        </div>

        <div className="mt-10 grid gap-8 lg:grid-cols-[1.2fr_1fr]">
          <div className="hairline overflow-hidden rounded-2xl bg-band">
            <svg viewBox="0 0 340 500" className="h-full w-full" role="img" aria-label={c.title}>
              <path
                d="M155 45 L200 55 L215 100 L200 140 L190 175 L200 220 L220 260 L235 305 L225 355 L215 400 L200 445 L180 465 L165 455 L155 425 L145 395 L135 355 L120 315 L108 275 L100 235 L95 195 L100 150 L115 110 L130 75 Z"
                fill="#EFEAE0"
                stroke="#D9D2C4"
                strokeWidth="1.5"
              />
              {Object.entries(CITY_POS).map(([name, p]) => (
                <g key={name}>
                  <circle cx={p.x} cy={p.y} r="8" fill="#C2563A" fillOpacity="0.2" />
                  <circle cx={p.x} cy={p.y} r="4" fill="#C2563A" />
                </g>
              ))}
            </svg>
          </div>

          <div className="flex flex-wrap content-start gap-2">
            {c.cities.map((city) => (
              <span key={city.name} className="chip hover:border-gold cursor-pointer">
                <span className="h-1.5 w-1.5 rounded-full bg-terracotta" aria-hidden />
                {city.name}
                <span className="text-muted-ink">· {city.count}</span>
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

