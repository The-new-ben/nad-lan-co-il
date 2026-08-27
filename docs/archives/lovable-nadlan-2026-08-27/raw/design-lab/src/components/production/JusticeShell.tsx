import { Link } from "@tanstack/react-router";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";
import { ImplDrawer, type Impl } from "./ProductionShell";

export type { Impl };

export const justiceNav: { label: string; to: string; hash?: string }[] = [
  { label: "עזרה עם AI", to: "/production/justice/legal-ai-desk" },
  { label: "סימולציה משפטית", to: "/production/justice/legal-simulation" },
  { label: "תחומי משפט", to: "/production/justice", hash: "j-intents" },
  { label: "מדריכים וכלים", to: "/production/justice", hash: "j-intents" },
  { label: "מצאו עורך דין", to: "/production/justice", hash: "j-fork" },
  { label: "לעורכי דין", to: "/production/justice", hash: "j-fork" },
];

export const justiceRoutes: { label: string; to: string }[] = [
  { label: "בית המוצר", to: "/production/justice" },
  { label: "סימולציה משפטית", to: "/production/justice/legal-simulation" },
  { label: "שולחן AI", to: "/production/justice/legal-ai-desk" },
];

export function JusticeHeader({
  primaryCta = "מצאו את המסלול שלכם",
  primaryHref = "#intake",
}: {
  primaryCta?: string;
  primaryHref?: string;
}) {
  const [open, setOpen] = useState(false);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    panelRef.current?.querySelector<HTMLElement>("a, button")?.focus();
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        setOpen(false);
        buttonRef.current?.focus();
      }
    };
    document.addEventListener("keydown", onKey);
    return () => document.removeEventListener("keydown", onKey);
  }, [open]);

  const itemCls =
    "tap inline-flex items-center whitespace-nowrap rounded-md px-3 py-2 text-sm font-semibold hover:bg-secondary hover:text-secondary-foreground";

  return (
    <header className="sticky top-0 z-30 w-full border-b border-border bg-background/95 backdrop-blur">
      <div className="lab-container flex min-w-0 items-center gap-2 py-3">
        <Link
          to="/production/justice"
          className="tap display flex min-w-0 shrink items-center gap-2 truncate text-lg"
        >
          <span
            aria-hidden="true"
            className="inline-block h-5 w-5 shrink-0 rounded-[3px] border-2 border-primary"
          />
          jus-tice
        </Link>

        <nav aria-label="ניווט ראשי" className="hidden min-w-0 xl:block">
          <ul className="flex items-center gap-0.5">
            {justiceNav.map((item) => (
              <li key={item.label}>
                <Link to={item.to} {...(item.hash ? { hash: item.hash } : {})} className={itemCls}>
                  {item.label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <div className="ms-auto flex shrink-0 items-center gap-2">
          <a
            href={primaryHref}
            className="tap inline-flex min-h-11 items-center whitespace-nowrap rounded-md bg-primary px-3 py-2 text-sm font-bold text-primary-foreground hover:opacity-90 sm:px-4"
          >
            {primaryCta}
          </a>
          <button
            ref={buttonRef}
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            aria-controls="justice-mobile-menu"
            aria-label={open ? "סגירת תפריט" : "פתיחת תפריט"}
            className="tap inline-flex min-h-11 min-w-11 items-center justify-center rounded-md border border-border px-3 py-2 xl:hidden"
          >
            <span aria-hidden="true" className="text-lg leading-none">
              {open ? "✕" : "☰"}
            </span>
          </button>
        </div>
      </div>

      {open ? (
        <div
          id="justice-mobile-menu"
          ref={panelRef}
          className="border-t border-border bg-card text-card-foreground xl:hidden"
        >
          <nav aria-label="ניווט ראשי במובייל" className="lab-container py-3">
            <ul className="grid gap-1">
              {justiceNav.map((item) => (
                <li key={item.label}>
                  <Link
                    to={item.to}
                    {...(item.hash ? { hash: item.hash } : {})}
                    onClick={() => setOpen(false)}
                    className="tap flex min-h-11 items-center rounded-md px-3 py-3 text-base font-semibold hover:bg-secondary"
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      ) : null}
    </header>
  );
}

const footerCols: { title: string; items: string[] }[] = [
  { title: "מוצר", items: ["שולחן AI", "סימולציה משפטית", "מחשבונים", "מסמכים"] },
  { title: "תחומי משפט", items: ["דיני משפחה", "דין פלילי", "דיני עבודה", "נזיקין"] },
  { title: "שקיפות", items: ["שיטת העריכה", "מקורות ועדכונים", "פרטיות ואבטחה", "מגבלות המוצר"] },
  { title: "אנשי מקצוע", items: ["הצטרפות עורכי דין", "מרחב עבודה", "פניות מותאמות"] },
];

export function JusticeFooter() {
  return (
    <footer className="border-t border-border bg-surface py-12 text-surface-foreground">
      <div className="lab-container">
        <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {footerCols.map((c) => (
            <nav key={c.title} aria-label={c.title}>
              <h2 className="text-sm font-bold">{c.title}</h2>
              <ul className="mt-3 space-y-2 text-sm text-muted-foreground">
                {c.items.map((i) => (
                  <li key={i}>
                    <a href="#" className="underline-offset-4 hover:underline">
                      {i}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          ))}
        </div>
        <p className="mt-10 max-w-3xl text-xs leading-relaxed text-muted-foreground">
          אב טיפוס פנימי. התכנים הם מידע כללי ואינם ייעוץ משפטי ואינם יוצרים יחסי עורך
          דין–לקוח. אין הבטחה לתוצאה משפטית. פרופילים מקצועיים המסומנים ״פרופיל דמו״ הם
          רשומות זרע להמחשה בלבד — ללא אימות, ללא זמינות וללא דירוגים.
        </p>
      </div>
    </footer>
  );
}

export function JusticeShell({
  route,
  impl,
  children,
  headerPrimaryCta,
  headerPrimaryHref,
}: {
  route: string;
  impl: Impl;
  children: ReactNode;
  headerPrimaryCta?: string;
  headerPrimaryHref?: string;
}) {
  return (
    <div className="theme-prod-justice">
      <div className="min-h-screen bg-background text-foreground">
        <div className="w-full border-b border-dashed border-border bg-surface text-surface-foreground">
          <div className="lab-container flex min-w-0 flex-wrap items-center gap-2 py-2">
            <Link
              to="/"
              className="tap inline-flex shrink-0 items-center rounded-md px-2 py-2 text-[0.7rem] font-bold uppercase tracking-wide"
            >
              מעבדה · פנימי
            </Link>
            <nav aria-label="מסלולי חבילת Justice" className="w-full min-w-0 lg:w-auto lg:flex-1">
              <ul className="no-scrollbar -mx-1 flex snap-x snap-mandatory items-center gap-1 overflow-x-auto px-1 py-1 lg:flex-wrap lg:overflow-visible">
                {justiceRoutes.map((r) => (
                  <li key={r.to} className="shrink-0 snap-start">
                    <Link
                      to={r.to}
                      activeOptions={{ exact: true }}
                      activeProps={{
                        className: cn(
                          "tap inline-flex items-center whitespace-nowrap rounded-md px-3 py-2 text-xs font-bold",
                          "bg-primary text-primary-foreground",
                        ),
                        "aria-current": "page",
                      }}
                      inactiveProps={{
                        className:
                          "tap inline-flex items-center whitespace-nowrap rounded-md border border-border bg-card px-3 py-2 text-xs font-semibold text-card-foreground hover:bg-secondary",
                      }}
                    >
                      {r.label}
                    </Link>
                  </li>
                ))}
                <li className="shrink-0 snap-start">
                  <Link
                    to="/production/nadlan"
                    className="tap inline-flex items-center whitespace-nowrap rounded-md border border-dashed border-border px-3 py-2 text-xs font-semibold text-muted-foreground hover:bg-secondary"
                  >
                    חבילת נדל״ן
                  </Link>
                </li>
              </ul>
            </nav>
          </div>
        </div>

        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:absolute focus:z-50 focus:m-2 focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground"
        >
          דילוג לתוכן המרכזי
        </a>

        <JusticeHeader
          {...(headerPrimaryCta ? { primaryCta: headerPrimaryCta } : {})}
          {...(headerPrimaryHref ? { primaryHref: headerPrimaryHref } : {})}
        />
        {children}
        <JusticeFooter />
        <ImplDrawer impl={impl} route={route} />
      </div>
    </div>
  );
}

/* ---------------- shared small pieces ---------------- */

export function Notice({
  tone = "info",
  title,
  children,
}: {
  tone?: "info" | "legal";
  title: string;
  children: ReactNode;
}) {
  return (
    <aside
      className={cn(
        "rounded-md border-s-4 bg-card p-4 text-sm leading-relaxed text-card-foreground",
        tone === "legal" ? "border-s-highlight" : "border-s-primary",
      )}
    >
      <p className="font-bold">{title}</p>
      <div className="mt-1 text-muted-foreground">{children}</div>
    </aside>
  );
}

export function StateBadge({
  state,
}: {
  state: "demo" | "empty" | "verified" | "pending";
}) {
  const map = {
    demo: { t: "פרופיל דמו", c: "border-dashed border-border bg-secondary text-secondary-foreground" },
    empty: { t: "אין עדיין נתונים", c: "border-border bg-card text-muted-foreground" },
    pending: { t: "ממתין לאימות", c: "border-highlight/40 bg-card text-highlight" },
    verified: { t: "מאומת", c: "border-primary/40 bg-accent text-accent-foreground" },
  }[state];
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-3 py-1 text-xs font-bold",
        map.c,
      )}
    >
      {map.t}
    </span>
  );
}

