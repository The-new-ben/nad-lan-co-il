// S6 — Listings grid. Ink-sketch building plates are never cropped (object-contain).
import { HE } from "@/lib/nadlan-copy";
import tlv from "@/assets/sketch-listing-tlv-bauhaus.jpg";
import jlm from "@/assets/sketch-listing-jlm.jpg";
import haifa from "@/assets/sketch-listing-haifa.jpg";
import rg from "@/assets/sketch-listing-rg.jpg";

const IMG: Record<string, string> = {
  "tlv-lev": tlv,
  "jlm-rehavia": jlm,
  "haifa-carmel": haifa,
  "rg-bavli": rg,
};

export function ListingsGridSection() {
  const c = HE.listings;

  return (
    <section className="bg-paper">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="kicker">{c.kicker}</p>
            <h2 className="mt-3" style={{ fontFamily: "var(--font-serif-he)" }}>{c.title}</h2>
            <p className="mt-2 text-sm text-muted-ink">{c.sub}</p>
          </div>
          <a href="/listings" className="hidden text-sm text-gold hover:underline sm:inline">
            {c.viewAll} ←
          </a>
        </div>

        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {c.items.map((item) => (
            <a
              key={item.id}
              href={`/listing/${item.id}`}
              className="hairline group block overflow-hidden rounded-2xl bg-card transition-transform hover:-translate-y-0.5 hover:border-gold"
            >
              <div className="aspect-[4/3] bg-band">
                <img
                  src={IMG[item.id]!}
                  alt={item.title}
                  className="h-full w-full object-contain"
                  loading="lazy"
                  width={1200}
                  height={912}
                />
              </div>
              <div className="p-5">
                <p className="text-xs text-muted-ink">{item.city}</p>
                <h3 className="mt-1 text-base leading-snug">{item.title}</h3>
                <div className="mt-3 flex items-baseline justify-between">
                  <span className="text-base font-semibold text-ink" style={{ direction: "ltr" }}>
                    {item.price}
                  </span>
                  <span className="text-xs text-muted-ink">{item.area}</span>
                </div>
              </div>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

