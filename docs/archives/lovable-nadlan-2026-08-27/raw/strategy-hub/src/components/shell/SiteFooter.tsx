import { Link } from "@tanstack/react-router";
import { useLang } from "@/lib/lang-context";
import { HE, EN } from "@/lib/nadlan-copy";

export function SiteFooter() {
  const { lang } = useLang();
  const isHe = lang === "he";
  const c = isHe ? HE : EN;

  // The ONE dark band on every page — --theater.
  return (
    <footer className="mt-24 bg-theater text-paper">
      <div className="mx-auto grid max-w-6xl gap-10 px-4 py-14 sm:px-6 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <div className="text-2xl" style={{ fontFamily: "var(--font-serif-he)", fontWeight: 800 }}>
            {c.brand}
          </div>
          <p className="mt-3 text-sm text-paper/70">{c.tagline}</p>
        </div>

        <div>
          <h4 className="kicker text-paper/90">{c.footer.product}</h4>
          <ul className="mt-4 space-y-2 text-sm text-paper/75">
            <li><Link to="/projects" className="hover:text-gold">{c.nav.projects}</Link></li>
            <li><Link to="/listings" className="hover:text-gold">{c.nav.listings}</Link></li>
            <li><Link to="/professionals" className="hover:text-gold">{c.nav.professionals}</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="kicker text-paper/90">{c.footer.solutions}</h4>
          <ul className="mt-4 space-y-2 text-sm text-paper/75">
            <li><Link to="/urban-renewal" className="hover:text-gold">{c.nav.urbanRenewal}</Link></li>
            <li><Link to="/my-renewal" className="hover:text-gold">{c.footer.myRenewal}</Link></li>
            <li><Link to="/my-rentals" className="hover:text-gold">{c.footer.myRentals}</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="kicker text-paper/90">{c.footer.tools}</h4>
          <ul className="mt-4 space-y-2 text-sm text-paper/75">
            <li><Link to="/calculators" className="hover:text-gold">{c.footer.calculators}</Link></li>
            <li><Link to="/glossary" className="hover:text-gold">{c.footer.glossary}</Link></li>
            <li><Link to="/guides" className="hover:text-gold">{c.footer.guides}</Link></li>
            <li><Link to="/about" className="hover:text-gold">{c.footer.about}</Link></li>
            <li><Link to="/contact" className="hover:text-gold">{c.footer.contact}</Link></li>
          </ul>
        </div>
      </div>

      <div className="border-t border-paper/10">
        <div className="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-5 text-xs text-paper/55 sm:flex-row sm:items-center sm:justify-between sm:px-6">
          <span>{c.footer.rights}</span>
          <span className="max-w-2xl">{c.footer.disclaim}</span>
        </div>
      </div>
    </footer>
  );
}

