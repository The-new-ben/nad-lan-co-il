// S8 — Editorial magazine row of three guides.
import { HE } from "@/lib/nadlan-copy";

export function MagazineSection() {
  const c = HE.magazine;

  return (
    <section className="bg-paper hairline-t">
      <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
        <div className="flex items-end justify-between gap-4">
          <div>
            <p className="kicker">{c.kicker}</p>
            <h2 className="mt-3" style={{ fontFamily: "var(--font-serif-he)" }}>{c.title}</h2>
          </div>
          <a href="/guides" className="hidden text-sm text-gold hover:underline sm:inline">
            לכל המדריכים ←
          </a>
        </div>

        <div className="mt-10 grid gap-8 md:grid-cols-3">
          {c.items.map((post, i) => (
            <article key={post.id} className={i > 0 ? "md:border-e md:border-hairline md:pe-8" : ""}>
              <p className="kicker">{post.eyebrow}</p>
              <h3 className="mt-3 text-xl leading-snug" style={{ fontFamily: "var(--font-serif-he)", fontWeight: 600 }}>
                <a href={`/guides#${post.id}`} className="hover:text-gold">{post.title}</a>
              </h3>
              <p className="mt-3 text-sm text-muted-ink">{post.excerpt}</p>
              <a href={`/guides#${post.id}`} className="mt-4 inline-block text-sm text-gold hover:underline">
                לקריאה ←
              </a>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

