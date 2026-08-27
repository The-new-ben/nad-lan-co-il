import { createFileRoute } from "@tanstack/react-router";
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

export const Route = createFileRoute("/listing/$id")({
  head: () => ({
    meta: [
      { title: "דירה · נדל״ן" },
      { name: "description", content: "פרטי הדירה, מיקום בבניין ובעיר." },
    ],
  }),
  component: ListingPage,
});

function ListingPage() {
  const { id } = Route.useParams();
  const item = HE.listings.items.find((x) => x.id === id) ?? HE.listings.items[0]!;

  return (
    <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-24">
      <div className="grid gap-10 lg:grid-cols-[1.2fr_1fr]">
        <div className="hairline overflow-hidden rounded-2xl bg-band">
          <img src={IMG[item.id] ?? tlv} alt={item.title} className="h-full w-full object-contain" />
        </div>
        <div>
          <p className="kicker">{item.city}</p>
          <h1 className="mt-3">{item.title}</h1>
          <div className="mt-4 flex items-baseline gap-4">
            <span className="text-2xl font-semibold" style={{ direction: "ltr" }}>{item.price}</span>
            <span className="text-sm text-muted-ink">{item.area}</span>
          </div>
          <div className="mt-6 flex flex-wrap gap-3">
            <button className="btn-terracotta hover:btn-terracotta-hover">בקשת שיחה</button>
            <button className="btn-gold-outline">שמירה</button>
          </div>
          <p className="mt-6 text-xs text-muted-ink">איור להמחשה של הבניין. תצלומים אמיתיים בבקשה מהמוכר.</p>
        </div>
      </div>
    </section>
  );
}

